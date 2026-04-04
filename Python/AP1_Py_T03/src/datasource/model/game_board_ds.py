"""Datasource model for game board."""
from typing import List


class GameBoardDS:
    """Datasource representation of game board.
    
    This is the data storage model for the database/storage layer.
    """
    
    def __init__(self, board: List[List[int]] = None):
        """Initialize the datasource game board.
        
        Args:
            board: 3x3 matrix of integers
        """
        if board is None:
            self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self.board = [row[:] for row in board]
    
    def get_board(self) -> List[List[int]]:
        """Get the board as a nested list."""
        return [row[:] for row in self.board]
    
    def copy(self) -> 'GameBoardDS':
        """Create a copy of the board."""
        return GameBoardDS(self.board)
