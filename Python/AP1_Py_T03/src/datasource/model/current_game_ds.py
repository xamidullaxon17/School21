"""Datasource model for current game."""
from datasource.model.game_board_ds import GameBoardDS


class CurrentGameDS:
    """Datasource representation of current game.
    
    This is the data storage model for the database/storage layer.
    """
    
    def __init__(self, game_id: str, board: GameBoardDS):
        """Initialize a datasource current game.
        
        Args:
            game_id: Unique identifier for the game (UUID string)
            board: The GameBoardDS instance
        """
        self.game_id = game_id
        self.board = board
    
    def get_game_id(self) -> str:
        """Get the game ID."""
        return self.game_id
    
    def get_board(self) -> GameBoardDS:
        """Get the game board."""
        return self.board
    
    def copy(self) -> 'CurrentGameDS':
        """Create a copy of the current game."""
        return CurrentGameDS(self.game_id, self.board.copy())
