from enum import Enum, auto


class ItemType(Enum):
    TREASURE = auto()
    FOOD = auto()
    ELIXIR = auto()
    SCROLL = auto()
    WEAPON = auto()
    KEY = auto()


class ItemSubtype(Enum):
    FOOD = auto()

    HEALTH = auto()
    DEXTERITY = auto()
    STRENGTH = auto()

    SWORD = auto()
    AXE = auto()
    BOW = auto()
    STAFF = auto()

    KEY_RED = auto()
    KEY_GREEN = auto()
    KEY_BLUE = auto()
    KEY_YELLOW = auto()


class EnemyType(Enum):
    ZOMBIE = auto()       # green z
    VAMPIRE = auto()      # red v
    GHOST = auto()        # white g
    OGRE = auto()         # yellow o
    SNAKE_MAGE = auto()   # white s
    MIMIC = auto()        # white m


class KeyColor(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()


class DoorState(Enum):
    CLOSED = auto()
    OPEN = auto()
    LOCKED = auto()


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PLAYING_3D = auto()
    INVENTORY = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTHEAST = (1, -1)
    NORTHWEST = (-1, -1)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (-1, 1)

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
