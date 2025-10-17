#!/home/perraseb/miniconda3/envs/ds_env/bin/python

import sys
from recipes import NutritionPredictor, NutritionFacts, RecipeRecommender, MenuGenerator

if len(sys.argv) < 2:
    # Empty run → show menu suggestion
    print("No ingredients provided.")
    print("If you want to search by ingredients: ./nutritionist.py ingredient1, ingredient2, ...\n")
    
    print("IV. DAILY MENU SUGGESTION")
    print("Generating a balanced daily menu based on our full recipe database...\n")

    menu_gen = MenuGenerator()
    menu_gen.generate_daily_menu(top_n_per_meal=5)
    sys.exit(0)  # exit after menu suggestion

# Otherwise: run normal ingredient-based pipeline
ingredients = [i.strip() for i in " ".join(sys.argv[1:]).split(',') if i.strip()]

predictor = NutritionPredictor()
facts = NutritionFacts()
recommender = RecipeRecommender()

# I. Forecast
print("\nI. OUR FORECAST")
try:
    label = predictor.predict(ingredients)
    forecast_text = {
        "bad": "You might find it tasty, but in our opinion, it is a bad idea to have a dish with that list of ingredients.",
        "so-so": "This dish might turn out okay, but don’t expect a miracle.",
        "great": "Nice! That looks like a tasty and promising combination!"
    }
    print(forecast_text[label])
    print("-------")
except ValueError as e:
    print(f"Prediction error: {e}")
    sys.exit(1)

# II. Nutrition Facts
print("\nII. NUTRITION FACTS")
print(facts.get_nutrition(ingredients))

# III. Top-3 Recipes
print("III. TOP-3 SIMILAR RECIPES:")
print(recommender.recommend(ingredients))