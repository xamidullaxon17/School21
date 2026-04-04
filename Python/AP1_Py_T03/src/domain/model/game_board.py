"""Domain model for game board."""
from typing import List


class GameBoard:
    """Represents the Tic-Tac-Toe game board as a 3x3 matrix.
    
    Values:
        0 - empty cell
        1 - human player (X)
        2 - computer player (O)
    """
    
    def __init__(self, board: List[List[int]] = None):
        """Initialize the game board.
        
        Args:
            board: 3x3 matrix of integers. If None, creates an empty board.
        """
        if board is None:
            self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self.board = [row[:] for row in board]
    
    def get_cell(self, row: int, col: int) -> int:
        """Get the value of a cell."""
        return self.board[row][col]
    
    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set the value of a cell."""
        self.board[row][col] = value
    
    def get_board(self) -> List[List[int]]:
        """Get a copy of the board."""
        return [row[:] for row in self.board]
    
    def get_empty_cells(self) -> List[tuple]:
        """Get all empty cells as list of (row, col) tuples."""
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells
    
    def copy(self) -> 'GameBoard':
        """Create a deep copy of the board."""
        return GameBoard(self.board)
