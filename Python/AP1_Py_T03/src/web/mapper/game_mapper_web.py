"""Mapper between domain and web models."""
from domain.model.game_board import GameBoard
from domain.model.current_game import CurrentGame
from web.model.game_board_web import GameBoardWeb
from web.model.current_game_web import CurrentGameWeb


class GameMapperWeb:
    """Maps between domain and web game models."""
    
    @staticmethod
    def domain_to_web_board(domain_board: GameBoard) -> GameBoardWeb:
        """Convert domain GameBoard to web GameBoardWeb.
        
        Args:
            domain_board: Domain layer GameBoard
            
        Returns:
            Web GameBoardWeb
        """
        return GameBoardWeb(domain_board.get_board())
    
    @staticmethod
    def web_to_domain_board(web_board: GameBoardWeb) -> GameBoard:
        """Convert web GameBoardWeb to domain GameBoard.
        
        Args:
            web_board: Web GameBoardWeb
            
        Returns:
            Domain GameBoard
        """
        return GameBoard(web_board.get_board())
    
    @staticmethod
    def domain_to_web_game(domain_game: CurrentGame) -> CurrentGameWeb:
        """Convert domain CurrentGame to web CurrentGameWeb.
        
        Args:
            domain_game: Domain layer CurrentGame
            
        Returns:
            Web CurrentGameWeb
        """
        web_board = GameMapperWeb.domain_to_web_board(domain_game.get_board())
        return CurrentGameWeb(domain_game.get_game_id(), web_board)
    
    @staticmethod
    def web_to_domain_game(web_game: CurrentGameWeb) -> CurrentGame:
        """Convert web CurrentGameWeb to domain CurrentGame.
        
        Args:
            web_game: Web CurrentGameWeb
            
        Returns:
            Domain CurrentGame
        """
        domain_board = GameMapperWeb.web_to_domain_board(web_game.get_board())
        return CurrentGame(domain_board, web_game.get_game_id())
