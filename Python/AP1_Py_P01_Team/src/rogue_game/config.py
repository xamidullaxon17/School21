"""O'yin sozlamalari va konstantalar"""

GAME_TITLE   = "Rogue 1980"
TOTAL_LEVELS = 21
GRID_SIZE    = 3

# Qahramon standart qiymatlari
DEFAULT_MAX_HEALTH = 100
DEFAULT_HEALTH     = 100
DEFAULT_DEXTERITY  = 10
DEFAULT_STRENGTH   = 10

# Ekran
USE_COLORS      = True
SHOW_FOG_OF_WAR = True
MAX_ITEMS_PER_TYPE = 9
MAX_ITEMS_TOTAL    = 99

# Mexanika
START_INVENTORY_SIZE      = 9
ENEMY_CHASING_RANGE       = 5
VAMPIRE_STEALTH_DAMAGE    = 2
SNAKE_MAGE_SLEEP_CHANCE   = 0.3
OGRE_DOUBLE_SPEED         = True

# Qiyinchilik
DIFFICULTY_INCREASE_INTERVAL = 3
ENEMY_STAT_SCALE_FACTOR      = 1.15   # har level uchun 15% o'sish
ITEM_DROP_RATE_DECREASE      = 0.035  # har level uchun 3.5% kamayish

# UI
MENU_WIDTH          = 50
MENU_HEIGHT         = 20
STATUS_PANEL_HEIGHT = 10

# 3D (Bonus Task 9)
FOV_DEGREES      = 60
MAX_RENDER_DEPTH = 30
TURN_SPEED_DEG   = 22   # daraja/bosish
MOVE_STEP_3D     = 0.5

# Doors (Bonus Task 6)
MAX_DOORS_PER_LEVEL = 3

# Dynamic difficulty (Bonus Task 7)
DIFFICULTY_EASY_THRESHOLD_DMG   = 10    # kamroq zarar olsa → qiyinroq
DIFFICULTY_HARD_THRESHOLD_DMG   = 60    # ko'p zarar olsa → osonroq
DIFFICULTY_MIN_MODIFIER         = 0.5
DIFFICULTY_MAX_MODIFIER         = 2.0
