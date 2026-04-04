import json
import os
import sys
from typing import List, Dict, Optional
from pathlib import Path

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from rogue_game.domain.entities import (
    GameSession, Character, Item, Backpack
)
from rogue_game.domain.enums import ItemType, ItemSubtype


class SaveManager:
    """Handles saving and loading game progress"""
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.current_save_file = self.save_dir / "current_game.json"
        self.leaderboard_file = self.save_dir / "leaderboard.json"
    
    def save_game(self, session: GameSession) -> bool:
        """Save current game state to file"""
        try:
            data = self._serialize_game_session(session)
            with open(self.current_save_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self) -> Optional[GameSession]:
        """Load game state from file"""
        if not self.current_save_file.exists():
            return None
        
        try:
            with open(self.current_save_file, 'r') as f:
                data = json.load(f)
            return self._deserialize_game_session(data)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def save_highscore(self, session: GameSession) -> None:
        """Save game statistics to leaderboard"""
        try:
            leaderboard = self._load_leaderboard()
            
            entry = {
                'level': session.statistics.level_reached,
                'treasure': session.statistics.treasure_collected,
                'enemies_defeated': session.statistics.enemies_defeated,
                'food_consumed': session.statistics.food_consumed,
                'elixirs_used': session.statistics.elixirs_used,
                'scrolls_read': session.statistics.scrolls_read,
                'attacks_made': session.statistics.attacks_made,
                'hits_taken': session.statistics.hits_taken,
                'tiles_traversed': session.statistics.tiles_traversed,
            }
            
            leaderboard.append(entry)
            
            # Sort by treasure and keep top 100
            leaderboard.sort(key=lambda x: x['treasure'], reverse=True)
            leaderboard = leaderboard[:100]
            
            with open(self.leaderboard_file, 'w') as f:
                json.dump(leaderboard, f, indent=2)
        except Exception as e:
            print(f"Error saving highscore: {e}")
    
    def get_leaderboard(self) -> List[Dict]:
        """Get leaderboard"""
        return self._load_leaderboard()
    
    def _load_leaderboard(self) -> List[Dict]:
        """Load leaderboard from file"""
        if not self.leaderboard_file.exists():
            return []
        
        try:
            with open(self.leaderboard_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _serialize_game_session(self, session: GameSession) -> dict:
        """Convert game session to JSON-serializable dict"""
        return {
            'current_level_number': session.current_level_number,
            'character': self._serialize_character(session.character),
            'statistics': {
                'treasure_collected': session.statistics.treasure_collected,
                'level_reached': session.statistics.level_reached,
                'enemies_defeated': session.statistics.enemies_defeated,
                'food_consumed': session.statistics.food_consumed,
                'elixirs_used': session.statistics.elixirs_used,
                'scrolls_read': session.statistics.scrolls_read,
                'attacks_made': session.statistics.attacks_made,
                'hits_taken': session.statistics.hits_taken,
                'tiles_traversed': session.statistics.tiles_traversed,
            },
            'seed': session.seed,
        }
    
    def _serialize_character(self, char: Character) -> dict:
        """Serialize character data"""
        weapon_data = None
        if char.current_weapon:
            weapon_data = self._serialize_item(char.current_weapon)
        
        return {
            'x': char.x,
            'y': char.y,
            'max_health': char.max_health,
            'health': char.health,
            'dexterity': char.dexterity,
            'strength': char.strength,
            'current_weapon': weapon_data,
            'backpack': self._serialize_backpack(char.backpack),
            'active_elixirs': {
                str(k): (v[0], v[1]) for k, v in char.active_elixirs.items()
            },
        }
    
    def _serialize_backpack(self, backpack: Backpack) -> dict:
        """Serialize backpack"""
        items_data = {}
        for subtype, items in backpack.items.items():
            items_data[str(subtype.name)] = [self._serialize_item(item) for item in items]
        return items_data
    
    def _serialize_item(self, item: Item) -> dict:
        """Serialize item"""
        return {
            'item_type': item.item_type.name,
            'subtype': item.subtype.name if item.subtype else None,
            'health_value': item.health_value,
            'max_health_bonus': item.max_health_bonus,
            'dexterity_bonus': item.dexterity_bonus,
            'strength_bonus': item.strength_bonus,
            'value': item.value,
            'is_temporary': item.is_temporary,
        }
    
    def _deserialize_game_session(self, data: dict) -> GameSession:
        """Convert JSON data to game session"""
        session = GameSession()
        session.current_level_number = data['current_level_number']
        session.character = self._deserialize_character(data['character'])
        session.seed = data.get('seed')
        
        # Restore statistics
        stats_data = data['statistics']
        session.statistics.treasure_collected = stats_data['treasure_collected']
        session.statistics.level_reached = stats_data['level_reached']
        session.statistics.enemies_defeated = stats_data['enemies_defeated']
        session.statistics.food_consumed = stats_data['food_consumed']
        session.statistics.elixirs_used = stats_data['elixirs_used']
        session.statistics.scrolls_read = stats_data['scrolls_read']
        session.statistics.attacks_made = stats_data['attacks_made']
        session.statistics.hits_taken = stats_data['hits_taken']
        session.statistics.tiles_traversed = stats_data['tiles_traversed']
        
        return session
    
    def _deserialize_character(self, data: dict) -> Character:
        """Deserialize character"""
        char = Character(
            x=data['x'],
            y=data['y'],
            max_health=data['max_health'],
            health=data['health'],
            dexterity=data['dexterity'],
            strength=data['strength'],
        )
        
        if data['current_weapon']:
            char.current_weapon = self._deserialize_item(data['current_weapon'])
        
        char.backpack = self._deserialize_backpack(data['backpack'])
        
        # Restore elixirs
        for subtype_str, (duration, bonus) in data.get('active_elixirs', {}).items():
            subtype = ItemSubtype[subtype_str]
            char.active_elixirs[subtype] = (duration, bonus)
        
        return char
    
    def _deserialize_backpack(self, data: dict) -> Backpack:
        """Deserialize backpack"""
        backpack = Backpack()
        for subtype_str, items_data in data.items():
            subtype = ItemSubtype[subtype_str]
            backpack.items[subtype] = [self._deserialize_item(item_data) for item_data in items_data]
        return backpack
    
    def _deserialize_item(self, data: dict) -> Item:
        """Deserialize item"""
        item_type = ItemType[data['item_type']]
        subtype = ItemSubtype[data['subtype']] if data['subtype'] else None
        
        return Item(
            item_type=item_type,
            subtype=subtype,
            health_value=data['health_value'],
            max_health_bonus=data['max_health_bonus'],
            dexterity_bonus=data['dexterity_bonus'],
            strength_bonus=data['strength_bonus'],
            value=data['value'],
            is_temporary=data['is_temporary'],
        )
