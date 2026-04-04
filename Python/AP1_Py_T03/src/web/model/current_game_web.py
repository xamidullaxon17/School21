"""Web model for current game."""
from typing import Optional
from web.model.game_board_web import GameBoardWeb


class CurrentGameWeb:
    """Web representation of current game.
    
    This model is used for request/response serialization.
    """
    
    def __init__(self, game_id: str, board: GameBoardWeb):
        """Initialize a web current game.
        
        Args:
            game_id: Unique identifier for the game (UUID string)
            board: The GameBoardWeb instance
        """
        self.game_id = game_id
        self.board = board
    
    def get_game_id(self) -> str:
        """Get the game ID."""
        return self.game_id
    
    def get_board(self) -> GameBoardWeb:
        """Get the game board."""
        return self.board
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'gameId': self.game_id,
            'board': self.board.get_board()
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'CurrentGameWeb':
        """Create a CurrentGameWeb from dictionary."""
        game_id = data.get('gameId', '')
        board_data = data.get('board', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        board = GameBoardWeb(board_data)
        return CurrentGameWeb(game_id, board)
