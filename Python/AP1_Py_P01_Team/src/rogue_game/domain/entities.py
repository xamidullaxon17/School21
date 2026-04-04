from __future__ import annotations
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
import math, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.enums import ItemType, ItemSubtype, EnemyType, KeyColor, DoorState
from rogue_game import config


# ---------------------------------------------------------------------------
# Door  (Bonus Task 6)
# ---------------------------------------------------------------------------
@dataclass
class Door:
    x: int
    y: int
    color: KeyColor
    state: DoorState = DoorState.LOCKED

    def is_passable(self) -> bool:
        return self.state == DoorState.OPEN


# ---------------------------------------------------------------------------
# Backpack
# ---------------------------------------------------------------------------
@dataclass
class Backpack:
    max_items_per_type: int = 9
    max_types: int = 10
    items: dict = field(default_factory=dict)  # {ItemSubtype: [Item, ...]}

    def add_item(self, item: Item) -> bool:
        if item.item_type == ItemType.TREASURE:
            key = ItemSubtype.HEALTH
            if key not in self.items:
                self.items[key] = []
            self.items[key].append(item)
            return True

        key = item.subtype
        if key is None:
            return False
        if key not in self.items:
            if len(self.items) >= self.max_types:
                return False
            self.items[key] = []

        if len(self.items[key]) >= self.max_items_per_type:
            return False

        self.items[key].append(item)
        return True

    def get_items_of_type(self, item_type: ItemSubtype) -> List[Item]:
        return self.items.get(item_type, [])

    def remove_item(self, item_type: ItemSubtype, index: int) -> Optional[Item]:
        if item_type not in self.items or index >= len(self.items[item_type]):
            return None
        return self.items[item_type].pop(index)

    def has_key(self, color: KeyColor) -> bool:
        subtype_map = {
            KeyColor.RED:    ItemSubtype.KEY_RED,
            KeyColor.GREEN:  ItemSubtype.KEY_GREEN,
            KeyColor.BLUE:   ItemSubtype.KEY_BLUE,
            KeyColor.YELLOW: ItemSubtype.KEY_YELLOW,
        }
        st = subtype_map.get(color)
        return bool(st and self.items.get(st))

    def consume_key(self, color: KeyColor) -> bool:
        subtype_map = {
            KeyColor.RED:    ItemSubtype.KEY_RED,
            KeyColor.GREEN:  ItemSubtype.KEY_GREEN,
            KeyColor.BLUE:   ItemSubtype.KEY_BLUE,
            KeyColor.YELLOW: ItemSubtype.KEY_YELLOW,
        }
        st = subtype_map.get(color)
        if st and self.items.get(st):
            self.items[st].pop(0)
            return True
        return False


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------
@dataclass
class Item:
    item_type: ItemType
    subtype: ItemSubtype = None
    x: int = 0
    y: int = 0
    health_value: int = 0
    max_health_bonus: int = 0
    dexterity_bonus: int = 0
    strength_bonus: int = 0
    value: int = 0
    is_temporary: bool = False

    def __post_init__(self):
        if self.item_type == ItemType.TREASURE:
            self.subtype = ItemSubtype.HEALTH

    def __repr__(self) -> str:
        if self.item_type == ItemType.TREASURE:
            return f"Treasure({self.value})"
        elif self.item_type == ItemType.FOOD:
            return f"Food(+{self.health_value} HP)"
        elif self.item_type == ItemType.WEAPON:
            name = self.subtype.name if self.subtype else "Weapon"
            return f"{name}(+{self.strength_bonus} STR)"
        elif self.item_type == ItemType.ELIXIR:
            sub = self.subtype.name if self.subtype else "?"
            return f"Elixir of {sub}"
        elif self.item_type == ItemType.SCROLL:
            sub = self.subtype.name if self.subtype else "?"
            return f"Scroll of {sub}"
        elif self.item_type == ItemType.KEY:
            color = self.subtype.name.replace("KEY_", "") if self.subtype else "?"
            return f"{color} Key"
        return "Item"


# ---------------------------------------------------------------------------
# Character
# ---------------------------------------------------------------------------
@dataclass
class Character:
    x: int = 0
    y: int = 0
    max_health: int = config.DEFAULT_MAX_HEALTH
    health: int = config.DEFAULT_HEALTH
    dexterity: int = config.DEFAULT_DEXTERITY
    strength: int = config.DEFAULT_STRENGTH
    current_weapon: Optional[Item] = None
    backpack: Backpack = field(default_factory=Backpack)
    active_elixirs: dict = field(default_factory=dict)  # {ItemSubtype: (duration, bonus)}

    # 3D mode (Task 9)
    view_angle: float = 0.0   # radians, east = 0
    view_x: float = 0.0       # float position for smooth 3D movement
    view_y: float = 0.0

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        self.health -= damage

    def heal(self, amount: int) -> None:
        self.health = min(self.health + amount, self.max_health)

    def increase_max_health(self, amount: int) -> None:
        self.max_health += amount
        self.health += amount

    def get_effective_dexterity(self) -> int:
        bonus = 0
        if ItemSubtype.DEXTERITY in self.active_elixirs:
            bonus = self.active_elixirs[ItemSubtype.DEXTERITY][1]
        return self.dexterity + bonus

    def get_effective_strength(self) -> int:
        bonus = self.strength
        if self.current_weapon:
            bonus += self.current_weapon.strength_bonus
        if ItemSubtype.STRENGTH in self.active_elixirs:
            bonus += self.active_elixirs[ItemSubtype.STRENGTH][1]
        return bonus

    def sync_view_pos(self):
        """Keep float view position in sync with tile position."""
        self.view_x = float(self.x) + 0.5
        self.view_y = float(self.y) + 0.5


# ---------------------------------------------------------------------------
# Enemy
# ---------------------------------------------------------------------------
@dataclass
class Enemy:
    enemy_type: EnemyType
    x: int = 0
    y: int = 0
    health: int = 50
    max_health: int = 50
    dexterity: int = 8
    strength: int = 8
    hostility: int = 5
    room_id: int = 0

    is_chasing: bool = False
    is_invisible: bool = False
    sleep_duration: int = 0
    last_attack_turn: int = -2
    has_attacked_this_combat: bool = False
    has_fought_player: bool = False   # for Vampire first-miss mechanic

    # Mimic-specific (Task 8)
    is_disguised: bool = False        # Mimic looks like an item
    disguise_item_type: str = "Food"  # what it looks like

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: int) -> None:
        self.health -= damage

    def get_display_char(self) -> str:
        if self.enemy_type == EnemyType.MIMIC and self.is_disguised:
            return '!'   # looks like an item
        chars = {
            EnemyType.ZOMBIE:     'z',
            EnemyType.VAMPIRE:    'v',
            EnemyType.GHOST:      'g',
            EnemyType.OGRE:       'o',
            EnemyType.SNAKE_MAGE: 's',
            EnemyType.MIMIC:      'm',
        }
        return chars.get(self.enemy_type, '?')

    def get_display_color(self) -> int:
        colors = {
            EnemyType.ZOMBIE:     2,   # green
            EnemyType.VAMPIRE:    1,   # red
            EnemyType.GHOST:      7,   # white
            EnemyType.OGRE:       3,   # yellow
            EnemyType.SNAKE_MAGE: 7,   # white
            EnemyType.MIMIC:      7,   # white
        }
        return colors.get(self.enemy_type, 7)


# ---------------------------------------------------------------------------
# Room
# ---------------------------------------------------------------------------
@dataclass
class Room:
    room_id: int
    grid_x: int
    grid_y: int
    x: int
    y: int
    width: int
    height: int
    enemies: List[Enemy] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    is_starting_room: bool = False
    is_exit_room: bool = False

    def contains_point(self, x: int, y: int) -> bool:
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)

    def is_walkable(self, x: int, y: int) -> bool:
        if not self.contains_point(x, y):
            return False
        lx = x - self.x
        ly = y - self.y
        is_wall = (lx == 0 or lx == self.width - 1 or
                   ly == 0 or ly == self.height - 1)
        return not is_wall


# ---------------------------------------------------------------------------
# Corridor
# ---------------------------------------------------------------------------
@dataclass
class Corridor:
    corridor_id: int
    room1_id: int
    room2_id: int
    tiles: List[Tuple[int, int]] = field(default_factory=list)

    def contains_point(self, x: int, y: int) -> bool:
        return (x, y) in self.tiles

    def is_walkable(self, x: int, y: int) -> bool:
        return self.contains_point(x, y)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
@dataclass
class Statistics:
    treasure_collected: int = 0
    level_reached: int = 1
    enemies_defeated: int = 0
    food_consumed: int = 0
    elixirs_used: int = 0
    scrolls_read: int = 0
    attacks_made: int = 0
    hits_taken: int = 0
    tiles_traversed: int = 0


# ---------------------------------------------------------------------------
# DifficultyTracker  (Bonus Task 7)
# ---------------------------------------------------------------------------
@dataclass
class DifficultyTracker:
    """Tracks performance metrics per level for dynamic difficulty."""
    damage_taken_this_level: int = 0
    kills_this_level: int = 0
    items_used_this_level: int = 0
    turns_this_level: int = 0
    difficulty_modifier: float = 1.0   # >1 harder, <1 easier

    def reset_for_new_level(self):
        self.damage_taken_this_level = 0
        self.kills_this_level = 0
        self.items_used_this_level = 0
        self.turns_this_level = 0

    def update_modifier(self, level: int):
        """Adjust difficulty modifier based on last level performance."""
        if self.turns_this_level == 0:
            return

        # Too easy: player took little damage and killed lots
        if self.damage_taken_this_level < 10 and self.kills_this_level >= 3:
            self.difficulty_modifier = min(2.0, self.difficulty_modifier + 0.15)
        # Too hard: player took a lot of damage and used many items
        elif self.damage_taken_this_level > 60 and self.items_used_this_level >= 2:
            self.difficulty_modifier = max(0.5, self.difficulty_modifier - 0.15)
        # Normal: nudge back toward 1.0
        else:
            if self.difficulty_modifier > 1.0:
                self.difficulty_modifier = max(1.0, self.difficulty_modifier - 0.05)
            elif self.difficulty_modifier < 1.0:
                self.difficulty_modifier = min(1.0, self.difficulty_modifier + 0.05)


# ---------------------------------------------------------------------------
# Level
# ---------------------------------------------------------------------------
@dataclass
class Level:
    level_number: int
    rooms: List[Room] = field(default_factory=list)
    corridors: List[Corridor] = field(default_factory=list)
    room_connections: dict = field(default_factory=dict)
    starting_room_id: int = 0
    exit_room_id: int = 0
    doors: List[Door] = field(default_factory=list)          # Task 6

    def get_room(self, room_id: int) -> Optional[Room]:
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None

    def get_door_at(self, x: int, y: int) -> Optional[Door]:
        for door in self.doors:
            if door.x == x and door.y == y:
                return door
        return None

    def is_walkable(self, x: int, y: int) -> bool:
        # Locked doors block movement
        door = self.get_door_at(x, y)
        if door is not None:
            return door.is_passable()

        for corridor in self.corridors:
            if corridor.contains_point(x, y):
                return True

        for room in self.rooms:
            if room.contains_point(x, y):
                return room.is_walkable(x, y)

        return False

    def is_wall(self, x: int, y: int) -> bool:
        """Used by 3D renderer."""
        door = self.get_door_at(x, y)
        if door is not None and not door.is_passable():
            return True
        for corridor in self.corridors:
            if corridor.contains_point(x, y):
                return False
        for room in self.rooms:
            if room.contains_point(x, y):
                lx = x - room.x
                ly = y - room.y
                is_wall = (lx == 0 or lx == room.width - 1 or
                           ly == 0 or ly == room.height - 1)
                return is_wall
        return True   # outside everything → wall

    def get_location(self, x: int, y: int) -> Optional[Room]:
        for room in self.rooms:
            if room.contains_point(x, y):
                return room
        return None


# ---------------------------------------------------------------------------
# GameSession
# ---------------------------------------------------------------------------
@dataclass
class GameSession:
    current_level_number: int = 1
    character: Character = field(default_factory=Character)
    current_level: Optional[Level] = None
    levels: dict = field(default_factory=dict)
    statistics: Statistics = field(default_factory=Statistics)
    difficulty: DifficultyTracker = field(default_factory=DifficultyTracker)
    is_new_game: bool = True
    seed: Optional[int] = None

    def is_running(self) -> bool:
        return self.character.is_alive()

    def has_completed_all_levels(self) -> bool:
        return self.current_level_number > 21

    def advance_to_next_level(self) -> None:
        self.current_level_number += 1
        self.statistics.level_reached = self.current_level_number
