# 🎮 Tic-Tac-Toe Loyihasi 
---

## 📁 Umumiy Loyiha Strukturasi

```
src/
├── main.py               ← Dastur shu yerdan boshlanadi
├── requirements.txt      ← Kerakli kutubxonalar
├── domain/               ← O'yinning asosiy mantiqi
├── datasource/           ← Ma'lumotlarni saqlash
├── web/                  ← Internet orqali muloqot
├── di/                   ← Qismlarni bir-biriga bog'lash
└── templates/            ← HTML sahifalar
```

**Nega bu 4 ta qatlam?**
Har bir qatlam faqat o'z ishini qiladi. Masalan, saqlash qismi o'zgarsa — o'yin mantiqi o'zgarmaydi. Bu katta loyihalarda juda muhim.

---

## 🚀 `main.py` — Dasturning Bosh Fayli

```python
app = Flask(__name__)          # Flask ilovasini yaratadi
container = Container()        # Barcha qismlarni bog'laydi
game_service = container.get_game_service()  # Servisni oladi
game_routes = create_game_routes(game_service)  # Yo'llarni ro'yxatdan o'tkazadi
app.register_blueprint(game_routes)  # Flask ga ulaydi
app.run(debug=True, host='0.0.0.0', port=5000)  # Serverni ishga tushiradi
```

**Vazifasi:** Barcha qismlarni yig'ib, serverni `localhost:5000` da ishga tushiradi.

---

## 🧠 `domain/` — O'yinning Miyasi

Bu qatlam **biznes mantiqni** saqlaydi. Ya'ni o'yin qoidalari, Minimax algoritmi — bularning hammasi shu yerda.

---

### 📂 `domain/model/`

#### `game_board.py` — O'yin Taxtasi

```python
class GameBoard:
    # 0 = bo'sh katak
    # 1 = odam (X)
    # 2 = kompyuter (O)
    
    def __init__(self, board=None):
        # Agar board berilmasa — 3x3 bo'sh matritsa yaratadi
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
    
    def get_cell(self, row, col)   # Katakdan qiymat oladi
    def set_cell(self, row, col, value)  # Katakka qiymat yozadi
    def get_empty_cells()          # Barcha bo'sh kataklar ro'yxatini beradi
    def copy()                     # Taxtaning nusxasini yaratadi (asl o'zgarmaydi)
```

**Vazifasi:** O'yin taxtasini `[[0,1,0],[2,0,1],[0,0,2]]` kabi 3x3 matritsa sifatida saqlaydi.

---

#### `current_game.py` — Joriy O'yin

```python
class CurrentGame:
    def __init__(self, board: GameBoard, game_id=None):
        self.game_id = game_id or str(uuid.uuid4())  # Har o'yin uchun noyob ID
        self.board = board                            # O'yin taxtasi
```

**Vazifasi:** Bitta o'yinni ifodalaydi — uning ID si va taxtasi. UUID tufayli bir vaqtda ko'p o'yin ishlashi mumkin.

---

### 📂 `domain/service/`

#### `__init__.py` — Servis Interfeysi (Shartnoma)

```python
class GameService(ABC):
    @abstractmethod
    def get_next_move(self, current_game)    # Kompyuter keyingi yurishi
    
    @abstractmethod
    def validate_game_board(self, current_game)  # Taxtani tekshirish
    
    @abstractmethod
    def is_game_ended(self, current_game)    # O'yin tugadimi?
```

**Vazifasi:** Bu interfeys — ya'ni "shartnoma". Kim bu sinfni meros olsa, 3 ta metodning hammasini yozishi shart. Bu kelajakda boshqa implementatsiya yozishni osonlashtiradi.

---

#### `game_service_impl.py` — Minimax Algoritmi ⭐

Bu loyihaning eng muhim fayli!

```python
HUMAN    = 1   # Odam belgisi
COMPUTER = 2   # Kompyuter belgisi
EMPTY    = 0   # Bo'sh katak
```

**`get_next_move()` — Eng Yaxshi Yurishni Tanlash:**
```python
def get_next_move(self, current_game):
    best_score = float('-inf')
    best_move = None
    
    for row, col in board.get_empty_cells():
        board.set_cell(row, col, COMPUTER)     # Shu katakka yursa nima bo'ladi?
        score = self._minimax(board, 0, False) # Ball hisoblaydi
        board.set_cell(row, col, EMPTY)        # Qaytaradi (faqat sinab ko'rdi)
        
        if score > best_score:
            best_score = score
            best_move = (row, col)   # Eng yuqori ball = eng yaxshi yurish
    
    board.set_cell(best_move[0], best_move[1], COMPUTER)  # Asliga yozadi
```

**`_minimax()` — Rekursiv Algoritm:**
```python
def _minimax(self, board, depth, is_maximizing):
    if kompyuter_yutdi:  return 10 - depth  # Tezroq yutish yaxshiroq
    if odam_yutdi:       return depth - 10  # Yutqizish yomon
    if taxta_to'la:      return 0           # Durrang

    if is_maximizing:   # Kompyuter navbati — eng katta ball izlaydi
        best = -∞
        for bo'sh katak:
            kompyuter yuradi → minimax chaqiradi → qaytaradi
        return max(balllar)
    else:               # Odam navbati — eng kichik ball izlaydi
        best = +∞
        for bo'sh katak:
            odam yuradi → minimax chaqiradi → qaytaradi
        return min(balllar)
```

**Qanday ishlaydi (misol):**
```
Taxta:          Kompyuter barcha variantlarni ko'radi:
X . .           [0,1] ga yursa → ball: +7
. . .    →      [0,2] ga yursa → ball: +5
. . .           [1,1] ga yursa → ball: +10  ← ENG YAXSHI
                ...
                Natija: o'rtaga (1,1) yuradi ✅
```

**`validate_game_board()` — Tekshirish:**
```python
# 1. Barcha qiymatlar 0, 1, 2 dan iboratmi?
# 2. Odam soni >= kompyuter soni (odam birinchi yuradi)
# 3. Ikkalasi bir vaqtda yutolmaydi
```

**`is_game_ended()` — O'yin Tugadimi?**
```python
# Kimdir 3 ta qator/ustun/diagonal to'ldirsami → True
# Barcha 9 katak to'lganmi → True (durrang)
# Aks holda → False (o'yin davom etadi)
```

---

## 💾 `datasource/` — Ma'lumotlarni Saqlash

Bu qatlam o'yinlarni xotirada saqlaydi va oladi.

---

### 📂 `datasource/model/`

#### `game_board_ds.py` va `current_game_ds.py`

Domain modellarga o'xshash, lekin **saqlash qatlami uchun** alohida.

```python
class GameBoardDS:
    # Xuddi GameBoard ga o'xshash, lekin datasource qatlami uchun
    
class CurrentGameDS:
    # game_id + GameBoardDS
    def copy()  # Saqlashda asl ob'ekt o'zgarmasin uchun nusxa olinadi
```

**Nega alohida model?**  
Domain va datasource bir-biridan mustaqil bo'lishi uchun. Masalan, kelajakda database ga o'tsa — faqat datasource qatlami o'zgaradi.

---

### 📂 `datasource/mapper/`

#### `game_mapper.py` — Tarjimon

```python
class GameMapper:
    domain_to_datasource_board(domain_board)  # GameBoard → GameBoardDS
    domain_to_datasource_game(domain_game)    # CurrentGame → CurrentGameDS
```

**Vazifasi:** Domain modellarini datasource modellariga o'giradi. Masalan, `GameBoard` ni `GameBoardDS` ga aylantiradi.

---

### `datasource/storage.py` — Xavfsiz Xotira 🔒

```python
class GameStorage:
    def __init__(self):
        self._games = {}     # { "uuid-123": CurrentGameDS, ... }
        self._lock = Lock()  # Bir vaqtda ko'p so'rov kelsa xatolik bo'lmasin
    
    def save_game(self, game):
        with self._lock:           # Boshqa thread kuta tursin
            self._games[game.id] = game.copy()  # Nusxa saqlaydi
    
    def get_game(self, game_id):
        with self._lock:
            return self._games[game_id].copy()  # Nusxa qaytaradi
```

**Vazifasi:** Thread-safe — ya'ni bir vaqtda 100 ta o'yinchi o'ynasa ham ma'lumotlar aralashmaydi. `Lock()` bir vaqtda faqat bitta operatsiya bajarilishini ta'minlaydi.

---

### 📂 `datasource/repository/`

#### `game_repository.py` — Ombor

```python
class GameRepository:
    def __init__(self, storage: GameStorage):
        self._storage = storage
    
    def save_game(self, game)        # Storage ga saqlaydi
    def get_game(self, game_id)      # Storage dan oladi
    def delete_game(self, game_id)   # O'chiradi
    def game_exists(self, game_id)   # Mavjudligini tekshiradi
```

**Vazifasi:** Service va Storage o'rtasidagi vositachi. Service to'g'ridan-to'g'ri Storage ga murojaat qilmaydi — Repository orqali qiladi. Bu kelajakda Storage ni (masalan, database ga) almashtirishni osonlashtiradi.

---

### `datasource/service.py` — Repository bilan Ishlaydi

```python
class GameServiceWithRepository(GameService):
    def __init__(self, repository):
        self._repository = repository
        self._game_service = GameServiceImpl()  # Minimax shu yerda
    
    def get_next_move(self, current_game):
        result = self._game_service.get_next_move(current_game)  # Minimax
        self._repository.save_game(result)   # Natijani saqlaydi
        return result
    
    def validate_game_board(self, game):
        return self._game_service.validate_game_board(game)
    
    def is_game_ended(self, game):
        return self._game_service.is_game_ended(game)
```

**Vazifasi:** Minimax algoritmini ishlatib, natijani Repository orqali saqlaydi.

---

## 🌐 `web/` — Internet Orqali Muloqot

Bu qatlam tashqi dunyo bilan — brauzer yoki boshqa ilovalar bilan — muloqot qiladi.

---

### 📂 `web/model/`

#### `game_board_web.py` va `current_game_web.py`

```python
class GameBoardWeb:
    # JSON dan kelgan taxtani saqlaydi

class CurrentGameWeb:
    def to_dict(self):          # Python ob'ektini → JSON ga aylantiradi
    def from_dict(data):        # JSON ni → Python ob'ektiga aylantiradi
    
    # Misol:
    # JSON:   {"gameId": "abc", "board": [[1,0,0],[0,2,0],[0,0,0]]}
    # Python: CurrentGameWeb(game_id="abc", board=GameBoardWeb(...))
```

**Vazifasi:** JSON formatidagi ma'lumotlarni Python ob'ektlariga o'giradi va aksincha.

---

### 📂 `web/mapper/`

#### `game_mapper_web.py` — Web Tarjimon

```python
class GameMapperWeb:
    web_to_domain_board(web_board)    # GameBoardWeb → GameBoard
    domain_to_web_board(domain_board) # GameBoard → GameBoardWeb
    web_to_domain_game(web_game)      # CurrentGameWeb → CurrentGame
    domain_to_web_game(domain_game)   # CurrentGame → CurrentGameWeb
```

**Vazifasi:** Web modellari va Domain modellari o'rtasida tarjimon vazifasini bajaradi.

---

### 📂 `web/route/`

#### `game_controller.py` — So'rovlarni Qabul Qiladi

```python
@game_bp.route('/game/<game_id>', methods=['POST'])
def make_move(game_id):
    # 1. JSON keldi → tekshiradi (bo'shmi?)
    data = request.get_json()
    
    # 2. JSON → CurrentGameWeb ob'ektiga aylantiradi
    web_game = CurrentGameWeb.from_dict(data)
    
    # 3. game_id mos kelishini tekshiradi
    if web_game.game_id != game_id: return xato(400)
    
    # 4. Web → Domain modelga aylantiradi
    domain_game = GameMapperWeb.web_to_domain_game(web_game)
    
    # 5. Taxta to'g'riligini tekshiradi
    if not game_service.validate_game_board(domain_game): return xato(400)
    
    # 6. O'yin tugaganmi?
    if game_service.is_game_ended(domain_game): return xato(400)
    
    # 7. Kompyuter yuradi (Minimax)
    result = game_service.get_next_move(domain_game)
    
    # 8. Domain → Web modelga → JSON → javob qaytaradi
    return jsonify(GameMapperWeb.domain_to_web_game(result).to_dict()), 200
```

**Vazifasi:** `POST /game/{UUID}` so'rovini qabul qiladi, kompyuter yurishini hisoblaydi, javob qaytaradi. Xato bo'lsa — tavsif bilan xato kodi qaytaradi.

---

## 🔧 `di/` — Qismlarni Bog'lash

#### `container.py` — Dependency Injection

```python
class Container:
    # Singleton — butun dasturda faqat bitta nusxa bo'ladi
    _instance = None
    
    def get_game_storage(self):
        # Faqat bir marta yaratiladi, keyin shu nusxa qaytariladi
        if Container._game_storage is None:
            Container._game_storage = GameStorage()
        return Container._game_storage
    
    def get_game_repository(self):
        if Container._game_repository is None:
            storage = self.get_game_storage()   # Storage ni oladi
            Container._game_repository = GameRepository(storage)
        return Container._game_repository
    
    def get_game_service(self):
        if Container._game_service is None:
            repository = self.get_game_repository()  # Repository ni oladi
            Container._game_service = GameServiceWithRepository(repository)
        return Container._game_service
```

**Vazifasi:** Barcha qismlarni to'g'ri tartibda yaratib, bir-biriga bog'laydi:

```
Container
    └── GameStorage (bitta nusxa — Singleton)
            └── GameRepository (Storage ni ishlatadi)
                    └── GameServiceWithRepository (Repository ni ishlatadi)
                                └── GameServiceImpl (Minimax algoritmi)
```

---

## 🔄 Ma'lumot Oqimi — Butun Jarayon

```
Brauzer/Curl
    │
    │  POST /game/UUID  {"board": [[1,0,0],...]}
    ▼
game_controller.py       ← So'rovni qabul qiladi
    │
    │  JSON → CurrentGameWeb
    ▼
game_mapper_web.py       ← Web → Domain ga o'giradi
    │
    │  CurrentGameWeb → CurrentGame
    ▼
GameServiceWithRepository ← Validatsiya + Minimax
    │
    ├── validate_game_board()  → Taxta to'g'rimi?
    ├── is_game_ended()        → O'yin tugadimi?
    └── get_next_move()        → Minimax → eng yaxshi yurish
            │
            ▼
        GameRepository → GameStorage ga saqlaydi
    │
    │  CurrentGame (kompyuter yurishi qo'shilgan)
    ▼
game_mapper_web.py       ← Domain → Web ga o'giradi
    │
    │  {"board": [[1,0,2],...]}
    ▼
Brauzer/Curl             ← Javob qaytadi
```

---

## 📊 Qatlamlar Jadvali

| Qatlam | Papka | Vazifasi |
|--------|-------|----------|
| 🌐 Web | `web/` | JSON qabul qilish, javob qaytarish |
| 🧠 Domain | `domain/` | O'yin qoidalari, Minimax algoritmi |
| 💾 Datasource | `datasource/` | Ma'lumotlarni xotirada saqlash |
| 🔧 DI | `di/` | Barcha qismlarni bog'lash |

---

## 💡 Asosiy Tushunchalar

| Tushuncha | Nima | Qayerda |
|-----------|------|---------|
| **Minimax** | Kompyuter har doim eng yaxshi yurishni tanlaydigan algoritm | `game_service_impl.py` |
| **UUID** | Har o'yin uchun noyob ID (masalan: `550e8400-e29b-...`) | `current_game.py` |
| **Thread-safe** | Bir vaqtda ko'p o'yinchi o'ynasa ham ma'lumot aralashmasin | `storage.py` |
| **Singleton** | Container butun dasturda bir marta yaratiladi | `container.py` |
| **Mapper** | Bir model turini boshqasiga o'giruvchi sinf | `*_mapper*.py` |
| **Interface** | Qoidalar to'plami — amalga oshiruvchi barcha metodlarni yozishi shart | `domain/service/__init__.py` |
