import random, sys, os, math
from typing import Tuple, Optional

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.entities import Character, Enemy, Item, Room, Level, Corridor
from rogue_game.domain.enums import EnemyType, ItemType, ItemSubtype
from rogue_game import config


class CombatSystem:
    @staticmethod
    def calculate_hit_chance(attacker: Character, defender: Enemy) -> float:
        base = 0.5 + (attacker.get_effective_dexterity() - defender.dexterity) * 0.02
        return max(0.1, min(0.95, base))

    @staticmethod
    def calculate_enemy_hit_chance(attacker: Enemy, defender: Character) -> float:
        base = 0.5 + (attacker.dexterity - defender.get_effective_dexterity()) * 0.02
        return max(0.1, min(0.95, base))

    @staticmethod
    def calculate_damage(strength: int, weapon: Optional[Item] = None) -> int:
        base = strength + random.randint(1, 6)
        weapon_bonus = weapon.strength_bonus if weapon else 0
        return max(1, base + weapon_bonus)

    @staticmethod
    def player_attacks_enemy(player: Character, enemy: Enemy) -> Tuple[bool, int]:
        # Mimic: reveal on first contact
        if enemy.enemy_type == EnemyType.MIMIC and enemy.is_disguised:
            enemy.is_disguised = False
            return False, 0   # surprise – miss on reveal

        # Vampire: first attack always misses
        if enemy.enemy_type == EnemyType.VAMPIRE and not enemy.has_fought_player:
            enemy.has_fought_player = True
            return False, 0

        if random.random() > CombatSystem.calculate_hit_chance(player, enemy):
            return False, 0

        damage = CombatSystem.calculate_damage(player.get_effective_strength(),
                                               weapon=player.current_weapon)
        enemy.take_damage(damage)
        return True, damage

    @staticmethod
    def enemy_attacks_player(enemy: Enemy, player: Character) -> Tuple[bool, int]:
        if enemy.sleep_duration > 0:
            enemy.sleep_duration -= 1
            return False, 0

        if random.random() > CombatSystem.calculate_enemy_hit_chance(enemy, player):
            return False, 0

        damage = CombatSystem.calculate_damage(enemy.strength)
        player.take_damage(damage)

        if enemy.enemy_type == EnemyType.VAMPIRE:
            steal = min(config.VAMPIRE_STEALTH_DAMAGE, player.max_health - 1)
            player.max_health -= steal
            player.health = min(player.health, player.max_health)
            enemy.health += steal

        elif enemy.enemy_type == EnemyType.SNAKE_MAGE:
            if random.random() < config.SNAKE_MAGE_SLEEP_CHANCE:
                player.active_elixirs[ItemSubtype.STRENGTH] = (1, 0)

        return True, damage

    @staticmethod
    def calculate_treasure_reward(enemy: Enemy) -> int:
        base = enemy.max_health + enemy.strength + enemy.dexterity + enemy.hostility
        return max(1, random.randint(int(base * 0.5), int(base * 1.5)))


class LevelDifficulty:
    @staticmethod
    def get_enemy_count(level: int, modifier: float = 1.0) -> int:
        base = min(3 + level // 3, 12)
        return max(1, int(base * modifier))

    @staticmethod
    def get_item_droprate(level: int, modifier: float = 1.0) -> float:
        # Higher modifier (harder) → fewer items
        base = max(0.1, 1.0 - level * config.ITEM_DROP_RATE_DECREASE)
        return max(0.05, base / modifier)

    @staticmethod
    def scale_enemy_stats(enemy_type: EnemyType, level: int,
                          modifier: float = 1.0) -> Tuple[int, int, int]:
        base_stats = {
            EnemyType.ZOMBIE:     (40, 5,  8),
            EnemyType.VAMPIRE:    (35, 9,  6),
            EnemyType.GHOST:      (20, 10, 3),
            EnemyType.OGRE:       (60, 4,  12),
            EnemyType.SNAKE_MAGE: (25, 12, 5),
            EnemyType.MIMIC:      (30, 9,  4),   # Task 8
        }
        health, dex, strength = base_stats.get(enemy_type, (30, 8, 6))
        scale = config.ENEMY_STAT_SCALE_FACTOR   # 1.15
        lhf = 1.0 + (level - 1) * (scale - 1.0)
        lsf = 1.0 + (level - 1) * (scale - 1.0) * 0.67
        return int(health * lhf * modifier), dex, int(strength * lsf)


class GameRules:
    TOTAL_LEVELS = 21

    @staticmethod
    def create_random_item(level: int) -> Optional[Item]:
        weights = {
            ItemType.FOOD:   0.4,
            ItemType.ELIXIR: 0.3,
            ItemType.SCROLL: 0.2,
            ItemType.WEAPON: 0.1,
        }
        item_type = random.choices(list(weights), weights=list(weights.values()))[0]

        if item_type == ItemType.FOOD:
            return Item(item_type=ItemType.FOOD,
                        subtype=ItemSubtype.FOOD,
                        health_value=random.randint(20, 50))

        if item_type == ItemType.ELIXIR:
            subtype = random.choice([ItemSubtype.HEALTH,
                                     ItemSubtype.DEXTERITY,
                                     ItemSubtype.STRENGTH])
            bonus = random.randint(3, 8)
            return Item(item_type=ItemType.ELIXIR, subtype=subtype,
                        is_temporary=True,
                        max_health_bonus=bonus if subtype == ItemSubtype.HEALTH else 0,
                        dexterity_bonus=bonus if subtype == ItemSubtype.DEXTERITY else 0,
                        strength_bonus=bonus if subtype == ItemSubtype.STRENGTH else 0)

        if item_type == ItemType.SCROLL:
            subtype = random.choice([ItemSubtype.HEALTH,
                                     ItemSubtype.DEXTERITY,
                                     ItemSubtype.STRENGTH])
            bonus = random.randint(1, 3)
            return Item(item_type=ItemType.SCROLL, subtype=subtype,
                        is_temporary=False,
                        max_health_bonus=bonus if subtype == ItemSubtype.HEALTH else 0,
                        dexterity_bonus=bonus if subtype == ItemSubtype.DEXTERITY else 0,
                        strength_bonus=bonus if subtype == ItemSubtype.STRENGTH else 0)

        # WEAPON
        wt = random.choice([ItemSubtype.SWORD, ItemSubtype.AXE,
                             ItemSubtype.BOW,   ItemSubtype.STAFF])
        return Item(item_type=ItemType.WEAPON, subtype=wt,
                    strength_bonus=random.randint(5, 15))
