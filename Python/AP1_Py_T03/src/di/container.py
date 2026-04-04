"""Dependency Injection Container."""
from datasource.storage import GameStorage
from datasource.repository.game_repository import GameRepository
from datasource.service import GameServiceWithRepository
from domain.service import GameService


class Container:
    """Dependency Injection container for managing dependencies."""
    
    _instance = None
    _game_storage = None
    _game_repository = None
    _game_service = None
    
    def __new__(cls):
        """Ensure the container is a singleton."""
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
        return cls._instance
    
    def get_game_storage(self) -> GameStorage:
        """Get or create the singleton GameStorage instance.
        
        The storage is thread-safe and maintains all game states.
        
        Returns:
            The singleton GameStorage instance
        """
        if Container._game_storage is None:
            Container._game_storage = GameStorage()
        return Container._game_storage
    
    def get_game_repository(self) -> GameRepository:
        """Get or create the singleton GameRepository instance.
        
        The repository depends on the storage and provides data access.
        
        Returns:
            The singleton GameRepository instance
        """
        if Container._game_repository is None:
            storage = self.get_game_storage()
            Container._game_repository = GameRepository(storage)
        return Container._game_repository
    
    def get_game_service(self) -> GameService:
        """Get or create the singleton GameService instance.
        
        Returns:
            The singleton GameService instance
        """
        if Container._game_service is None:
            repository = self.get_game_repository()
            Container._game_service = GameServiceWithRepository(repository)
        return Container._game_service



