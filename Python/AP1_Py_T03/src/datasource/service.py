"""Service implementation using repository for data access."""
from domain.service import GameService
from domain.model.current_game import CurrentGame
from datasource.repository.game_repository import GameRepository
from datasource.mapper.game_mapper import GameMapper
from domain.service.game_service_impl import GameServiceImpl


class GameServiceWithRepository(GameService):
    """Game service implementation that uses repository for data access."""

    def __init__(self, repository: GameRepository):
        self._repository = repository
        self._game_service = GameServiceImpl()

    def get_next_move(self, current_game: CurrentGame) -> CurrentGame:
        result_game = self._game_service.get_next_move(current_game)
        ds_game = GameMapper.domain_to_datasource_game(result_game)
        self._repository.save_game(ds_game)
        return result_game

    def validate_game_board(self, current_game: CurrentGame) -> bool:
        """Validate the current game board.

        Checks:
        1. Only valid values (0, 1, 2) on the board.
        2. Move counts are balanced (human == computer or human == computer+1).
        3. Both players have not won simultaneously.
        4. Previously saved computer moves have NOT been altered by the user.
        """
        # Step 1: basic domain validation
        if not self._game_service.validate_game_board(current_game):
            return False

        # Step 2: compare with saved state — previous moves must be intact
        saved_ds = self._repository.get_game(current_game.get_game_id())
        if saved_ds is not None:
            saved_game = GameMapper.datasource_to_domain_game(saved_ds)
            saved_board = saved_game.get_board().get_board()
            current_board = current_game.get_board().get_board()
            for i in range(3):
                for j in range(3):
                    # Any previously placed piece must not be changed
                    if saved_board[i][j] != 0 and current_board[i][j] != saved_board[i][j]:
                        return False  # Previous move was altered!

        return True

    def is_game_ended(self, current_game: CurrentGame) -> bool:
        return self._game_service.is_game_ended(current_game)
