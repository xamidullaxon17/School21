"""Thread-safe storage for games."""
from threading import Lock
from typing import Optional
from datasource.model.current_game_ds import CurrentGameDS


class GameStorage:
    """Thread-safe storage for games."""
    
    def __init__(self):
        """Initialize the game storage."""
        self._games: dict = {}
        self._lock = Lock()
    
    def save_game(self, game: CurrentGameDS) -> None:
        """Save or update a game in storage.
        
        Thread-safe operation.
        
        Args:
            game: The CurrentGameDS object to save
        """
        with self._lock:
            game_copy = game.copy()
            self._games[game.get_game_id()] = game_copy
    
    def get_game(self, game_id: str) -> Optional[CurrentGameDS]:
        """Retrieve a game from storage by ID.
        
        Thread-safe operation.
        
        Args:
            game_id: The ID of the game to retrieve
            
        Returns:
            The CurrentGameDS object if found, None otherwise
        """
        with self._lock:
            if game_id in self._games:
                return self._games[game_id].copy()
            return None
        
    def delete_game(self, game_id: str) -> bool:
        with self._lock:
            if game_id in self._games:
                del self._games[game_id]
                return True
            return False

    def game_exists(self, game_id: str) -> bool:
        with self._lock:
            return game_id in self._games

