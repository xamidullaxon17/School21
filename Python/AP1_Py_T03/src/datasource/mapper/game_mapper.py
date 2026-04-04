"""Mapper between domain and datasource models (both directions)."""
from domain.model.game_board import GameBoard
from domain.model.current_game import CurrentGame
from datasource.model.game_board_ds import GameBoardDS
from datasource.model.current_game_ds import CurrentGameDS


class GameMapper:
    """Maps between domain and datasource game models (domain<->datasource)."""

    # ---------- domain -> datasource ----------

    @staticmethod
    def domain_to_datasource_board(domain_board: GameBoard) -> GameBoardDS:
        return GameBoardDS(domain_board.get_board())

    @staticmethod
    def domain_to_datasource_game(domain_game: CurrentGame) -> CurrentGameDS:
        ds_board = GameMapper.domain_to_datasource_board(domain_game.get_board())
        return CurrentGameDS(domain_game.get_game_id(), ds_board)

    # ---------- datasource -> domain ----------

    @staticmethod
    def datasource_to_domain_board(ds_board: GameBoardDS) -> GameBoard:
        return GameBoard(ds_board.get_board())

    @staticmethod
    def datasource_to_domain_game(ds_game: CurrentGameDS) -> CurrentGame:
        domain_board = GameMapper.datasource_to_domain_board(ds_game.get_board())
        return CurrentGame(domain_board, ds_game.get_game_id())
