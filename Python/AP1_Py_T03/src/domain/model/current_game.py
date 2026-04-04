"""Domain model for current game."""
import uuid
from typing import Optional
from domain.model.game_board import GameBoard


class CurrentGame:
    """Represents a game in progress.
    
    Attributes:
        game_id: Unique identifier for the game (UUID)
        board: The current state of the game board
    """
    
    def __init__(self, board: GameBoard, game_id: Optional[str] = None):
        """Initialize a current game.
        
        Args:
            board: The GameBoard instance
            game_id: Optional UUID string. If None, generates a new UUID.
        """
        self.game_id = game_id if game_id else str(uuid.uuid4())
        self.board = board
    
    def get_game_id(self) -> str:
        """Get the game ID."""
        return self.game_id
    
    def get_board(self) -> GameBoard:
        """Get the game board."""
        return self.board
    
    def copy(self) -> 'CurrentGame':
        """Create a deep copy of the current game."""
        return CurrentGame(self.board.copy(), self.game_id)
