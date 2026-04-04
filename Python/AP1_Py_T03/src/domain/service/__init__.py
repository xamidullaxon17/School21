"""Domain service package."""
from abc import ABC, abstractmethod
from domain.model.current_game import CurrentGame


class GameService(ABC):
    """Interface for game service."""
    
    @abstractmethod
    def get_next_move(self, current_game: CurrentGame) -> CurrentGame:
        """Determine the next move in the current game using Minimax algorithm.
        
        Args:
            current_game: The current game state
            
        Returns:
            The game with the computer's move applied
        """
        pass
    
    @abstractmethod
    def validate_game_board(self, current_game: CurrentGame) -> bool:
        """Validate the current game board.
        
        Checks that previous moves have not been altered.
        
        Args:
            current_game: The game to validate
            
        Returns:
            True if the board is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def is_game_ended(self, current_game: CurrentGame) -> bool:
        """Check if the game has ended.
        
        Args:
            current_game: The current game state
            
        Returns:
            True if the game has ended, False otherwise
        """
        pass


__all__ = ['GameService']
