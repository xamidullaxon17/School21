"""Repository interface and implementation for games."""
from typing import Optional
from datasource.storage import GameStorage
from datasource.model.current_game_ds import CurrentGameDS

class GameRepository:
    """Repository for managing game data operations.
    Provides an interface between the service layer and the storage layer.
    """
    def __init__(self, storage: GameStorage):
        """Initialize the repository with a storage instance.
        Args:
            storage: The GameStorage instance to use
        """
        self._storage = storage
    
    def save_game(self, game: CurrentGameDS) -> None:
        """Save a game to storage.
        Args:
            game: The CurrentGameDS object to save
        """
        self._storage.save_game(game)
    
    def get_game(self, game_id: str) -> Optional[CurrentGameDS]:
        """Retrieve a game from storage by ID.
        Args:
            game_id: The ID of the game to retrieve
            
        Returns:
            The CurrentGameDS object if found, None otherwise
        """
        return self._storage.get_game(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game from storage.
        Args:
            game_id: The ID of the game to delete
            
        Returns:
            True if the game was deleted, False if it didn't exist
        """
        return self._storage.delete_game(game_id)
    
    def game_exists(self, game_id: str) -> bool:
        """Check if a game exists in storage.
        Args:
            game_id: The ID of the game to check
            
        Returns:
            True if the game exists
        """
        return self._storage.game_exists(game_id)
