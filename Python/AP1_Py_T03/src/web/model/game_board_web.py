"""Web model for game board."""
from typing import List


class GameBoardWeb:
    """Web representation of game board.
    
    This model is used for request/response serialization.
    """
    
    def __init__(self, board: List[List[int]] = None):
        """Initialize the web game board.
        
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
