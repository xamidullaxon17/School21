"""Implementation of game service with Minimax algorithm."""
from domain.service import GameService
from domain.model.current_game import CurrentGame
from domain.model.game_board import GameBoard


class GameServiceImpl(GameService):
    """Game service implementation using Minimax algorithm."""
    
    HUMAN = 1
    COMPUTER = 2
    EMPTY = 0
    
    def get_next_move(self, current_game: CurrentGame) -> CurrentGame:
        """Get the computer's next move using Minimax algorithm.
        
        Args:
            current_game: The current game state
            
        Returns:
            New game with computer's move applied
        """
        board = current_game.get_board().copy()
        
        # Find best move using minimax
        best_score = float('-inf')
        best_move = None
        
        empty_cells = board.get_empty_cells()
        for row, col in empty_cells:
            board.set_cell(row, col, self.COMPUTER)
            score = self._minimax(board, 0, False)
            board.set_cell(row, col, self.EMPTY)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        # Apply the best move
        if best_move:
            board.set_cell(best_move[0], best_move[1], self.COMPUTER)
        
        return CurrentGame(board, current_game.get_game_id())
    
    def validate_game_board(self, current_game: CurrentGame) -> bool:
        """Validate the game board.
        
        A valid board should:
        - Have only valid values (0, 1, 2)
        - Not have more than 9 moves
        - Have roughly equal or slightly more X moves than O moves
        
        Args:
            current_game: The game to validate
            
        Returns:
            True if valid, False otherwise
        """
        board = current_game.get_board()
        board_data = board.get_board()
        
        human_count = 0
        computer_count = 0
        
        for row in board_data:
            for cell in row:
                if cell == self.HUMAN:
                    human_count += 1
                elif cell == self.COMPUTER:
                    computer_count += 1
                elif cell != self.EMPTY:
                    return False  # Invalid cell value
        
        # Human should have moved same or one more time than computer
        if human_count < computer_count or human_count > computer_count + 1:
            return False
        
        # Check if both players have won (invalid state)
        if self._check_winner(board, self.HUMAN) and self._check_winner(board, self.COMPUTER):
            return False
        
        return True
    
    def is_game_ended(self, current_game: CurrentGame) -> bool:
        """Check if the game has ended.
        
        The game ends when:
        - One player has won
        - The board is full (draw)
        
        Args:
            current_game: The current game state
            
        Returns:
            True if the game has ended, False otherwise
        """
        board = current_game.get_board()
        
        # Check if anyone won
        if self._check_winner(board, self.HUMAN) or self._check_winner(board, self.COMPUTER):
            return True
        
        # Check if board is full (draw)
        return len(board.get_empty_cells()) == 0
    
    def _minimax(self, board: GameBoard, depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm implementation.
        
        Args:
            board: The game board
            depth: Current depth in the game tree
            is_maximizing: True if maximizing player (computer), False if minimizing (human)
            
        Returns:
            The score of the position
        """
        # Check terminal states
        if self._check_winner(board, self.COMPUTER):
            return 10 - depth
        if self._check_winner(board, self.HUMAN):
            return depth - 10
        if len(board.get_empty_cells()) == 0:
            return 0  # Draw
        
        if is_maximizing:
            best_score = float('-inf')
            for row, col in board.get_empty_cells():
                board.set_cell(row, col, self.COMPUTER)
                score = self._minimax(board, depth + 1, False)
                board.set_cell(row, col, self.EMPTY)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in board.get_empty_cells():
                board.set_cell(row, col, self.HUMAN)
                score = self._minimax(board, depth + 1, True)
                board.set_cell(row, col, self.EMPTY)
                best_score = min(best_score, score)
            return best_score
    
    def _check_winner(self, board: GameBoard, player: int) -> bool:
        """Check if a player has won.
        
        Args:
            board: The game board
            player: The player to check (1 for human, 2 for computer)
            
        Returns:
            True if the player has won, False otherwise
        """
        board_data = board.get_board()
        
        # Check rows
        for row in board_data:
            if all(cell == player for cell in row):
                return True
        
        # Check columns
        for col in range(3):
            if all(board_data[row][col] == player for row in range(3)):
                return True
        
        # Check diagonals
        if all(board_data[i][i] == player for i in range(3)):
            return True
        if all(board_data[i][2 - i] == player for i in range(3)):
            return True
        
        return False
