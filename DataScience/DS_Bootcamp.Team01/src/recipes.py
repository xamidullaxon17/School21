import joblib
import numpy as np
import pandas as pd
import json
import random
import warnings

warnings.filterwarnings("ignore")

class NutritionPredictor:
    def __init__(self):
        self.model = joblib.load("model/stacking_catboost_xgb_model.joblib")
        self.scaler = joblib.load("model/scaler.save")
        self.encoder = joblib.load("model/label_encoder.save")

        with open("model/feature_list.json", 'r') as f:
            self.features = json.load(f)

    def vectorize_ingredients(self, input_ingredients):
        input_set = set(i.strip().lower() for i in input_ingredients)
        vec = np.zeros(len(self.features))
        matched = False
        
        for idx, feature in enumerate(self.features):
            if feature.lower() in input_set:
                vec[idx] = 1
                matched = True

        if not matched:
            raise ValueError("None of the ingredients were found in the feature database. Check the names.")

        return vec.reshape(1, -1)


    def predict(self, ingredients_list):
        # Проверка длины каждого ингредиента
        short_words = [word for word in ingredients_list if len(word.strip()) <= 2]
        if short_words:
            raise ValueError(f"None of the ingredients were found in the feature database. Check the names.")

        # Векторизация и предсказание
        X_input = self.vectorize_ingredients(ingredients_list)
        X_scaled = self.scaler.transform(X_input)

        y_pred = self.model.predict(X_scaled)
        class_label = self.encoder.inverse_transform(y_pred)[0]

        return class_label


class NutritionFacts:
    def __init__(self, csv_path="data/ingredient_nutrition_dv.csv"):
        self.df = pd.read_csv(csv_path)
        self.df['ingredient'] = self.df['ingredient'].str.strip().str.lower()
        self.df.set_index('ingredient', inplace=True)

    
    def get_nutrition(self, ingredients_list):
        input_set = set(i.strip().capitalize() for i in ingredients_list)
        result = []
        for item in input_set:
            ing = item.strip().lower()
            if ing in self.df.index:
                row = self.df.loc[ing]
                facts = [f"{nutrient} - {val}% of Daily Value"
                         for nutrient, val in row.items()
                         if pd.notna(val) and val != 0]
                if facts:
                    result.append(f"{item}\n" + "\n".join(facts))
                else:
                    result.append(f"{item}")
            else:
                result.append(f"{item}")
        return ("\n-------\n".join(result)+"\n------\n")


class RecipeRecommender:
    def __init__(self, csv_path="data/recipes_with_urls_cleaned.csv"):
        self.df = pd.read_csv(csv_path)
        self.df.fillna("", inplace=True)
        self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce').fillna(0.0)

    def recommend(self, ingredients_list, top_n=3):
        results = []

        ingredients = [i.strip().lower() for i in ingredients_list]

        for _, row in self.df.iterrows():
            score = 0
            title = row['title'].lower()
            query = row['searched_query'].lower()

            for ing in ingredients:
                if ing in title:
                    score += 2
                if ing in query:
                    score += 1

            if score > 0:
                results.append({
                    'title': row['title'],
                    'rating_value': row['rating'],
                    'rating_text': f"{row['rating']}" if row['rating'] > 0 else "No rating",
                    'url': row['url'],
                    'score': score
                })

        results_sorted = sorted(results, key=lambda x: (-x['score'], -x['rating_value']))

        seen = set()
        unique_results = []
        for r in results_sorted:
            key = (r['title'], r['url'])
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        top_results = unique_results[:top_n]

        formatted = []
        for r in top_results:
            formatted.append(f"- {r['title']}, rating: {r['rating_text']}, URL:\n{r['url']}")

        return ("\n------\n".join(formatted)+"\n------\n")
    


    
class MenuGenerator:
    def __init__(self, nutrition_path="data/ingredient_nutrition_dv_bld.csv", 
                 recipes_path="data/recipes_with_urls_cleaned.csv"):
        # Загружаем данные по нутриентам
        self.nutrition_df = pd.read_csv(nutrition_path)
        self.nutrition_df.fillna(0.0, inplace=True)

        # Преобразуем в словарь: ingredient → {nutrient: %DV, ..., breakfast/lunch/dinner: True/False}
        self.ingredient_data = {}
        for _, row in self.nutrition_df.iterrows():
            ingredient = row["ingredient"].strip().lower()
            nutrition_info = row.drop("ingredient").to_dict()
            self.ingredient_data[ingredient] = nutrition_info

        # Загружаем рецепты
        self.recipes_df = pd.read_csv(recipes_path)
        self.recipes_df.fillna("", inplace=True)
        self.recipes_df["rating"] = pd.to_numeric(self.recipes_df["rating"], errors="coerce").fillna(0.0)

        # Подготовим список всех нутриентов
        self.nutrient_columns = [
            col for col in self.nutrition_df.columns 
            if col not in ["ingredient", "breakfast", "lunch", "dinner"]
        ]
    
    def extract_ingredients_from_query(self, searched_query, title=""):
        """
        Объединяет searched_query и title, возвращает список известных ингредиентов
        """
        # Собираем слова из обоих полей
        raw_text = searched_query + "," + title
        words = [w.strip().lower() for w in raw_text.replace("-", " ").replace("(", "").replace(")", "").split(",")]
        parts = []
        for w in words:
            parts.extend(w.split())  # разбиваем по пробелам
        unique_words = set(w.strip() for w in parts if w.strip())

        # Фильтруем только известные ингредиенты
        return [w for w in unique_words if w in self.ingredient_data]

    def is_meal_ingredient(self, ingredient, meal_type):
        """
        Проверяет, используется ли ингредиент для заданного приёма пищи
        meal_type: 'breakfast', 'lunch', 'dinner'
        """
        if ingredient not in self.ingredient_data:
            return False
        return bool(self.ingredient_data[ingredient].get(meal_type, False))

    def evaluate_recipe(self, ingredients):
        total_dv = {nutr: 0.0 for nutr in self.nutrient_columns}
        for ing in ingredients:
            if ing not in self.ingredient_data:
                continue
            data = self.ingredient_data[ing]
            for nutr in self.nutrient_columns:
                total_dv[nutr] += data.get(nutr, 0.0)

        # Проверка: не превышает ли 100% по какому-либо нутриенту
        for v in total_dv.values():
            if v > 100.0:
                return None  # Пропускаем рецепт

        total_sum = sum(total_dv.values())
        return total_sum, total_dv
    
    def get_recipes_for_meal(self, meal_type, top_n=1):
        candidates = []

        for _, row in self.recipes_df.iterrows():
            ingredients = self.extract_ingredients_from_query(row["searched_query"], row["title"])

            if not ingredients:
                continue

            # Все ли ингредиенты подходят для этого приёма пищи?
            if not all(self.is_meal_ingredient(ing, meal_type) for ing in ingredients):
                continue

            result = self.evaluate_recipe(ingredients)
            if not result:
                continue

            total_score, dv_data = result

            candidates.append({
                "query": row["searched_query"],
                "rating": row["rating"],
                "ingredients": ingredients,
                "nutrients": dv_data,
                "url": row["url"],
                "total_dv": total_score
            })

        # Сортировка: сначала по рейтингу, потом по покрытию нутриентов
        sorted_candidates = sorted(candidates, key=lambda x: (-x["rating"], -x["total_dv"]))

        return sorted_candidates[:top_n] if len(sorted_candidates) > 0 else []

    def generate_daily_menu(self, top_n_per_meal=5):
        menu = {}

        for meal in ["breakfast", "lunch", "dinner"]:
            recipes = self.get_recipes_for_meal(meal, top_n=top_n_per_meal)
            if recipes:
                menu[meal] = random.choice(recipes)  # ← выбираем случайный из top_n
            else:
                menu[meal] = None

        for meal in ["breakfast", "lunch", "dinner"]:
            recipe = menu[meal]
            print(meal.upper())
            print("-" * 30)
            if recipe:
                print(f"{recipe['query']} (rating: {recipe['rating']})")
                print("Ingredients:")
                for ing in recipe["ingredients"]:
                    print(f"- {ing}")
                print("Nutrients:")
                for k, v in recipe["nutrients"].items():
                    if v > 0:
                        print(f"- {k}: {v:.1f}%")
                print("URL:", recipe["url"])
            else:
                print("No suitable recipe found.")
            print()


