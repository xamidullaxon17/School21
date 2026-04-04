"""Flask route/controller for game operations."""
from flask import Blueprint, request, jsonify
from domain.service import GameService
from web.model.current_game_web import CurrentGameWeb
from web.mapper.game_mapper_web import GameMapperWeb


def create_game_routes(game_service: GameService) -> Blueprint:
    """Create Flask routes for game operations.
    
    Args:
        game_service: The game service instance
        
    Returns:
        A Flask Blueprint with game routes
    """
    game_bp = Blueprint('game', __name__)
    
    @game_bp.route('/game/<game_id>', methods=['POST'])
    def make_move(game_id: str):
        """Handle a game move.
        
        POST /game/{game_id}
        
        Accepts a current game with a user-updated game board and returns
        a current game with a computer-updated game board.
        
        Args:
            game_id: The ID of the game
            
        Request JSON:
            {
                "gameId": "uuid-string",
                "board": [[1, 0, 0], [0, 2, 0], [0, 0, 1]]
            }
            
        Returns:
            JSON response with updated game or error
        """
        try:
            # Parse request data
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Invalid request: JSON body is empty'
                }), 400
            
            # Create web model from request
            web_game = CurrentGameWeb.from_dict(data)
            
            # Verify game ID matches
            if web_game.get_game_id() != game_id:
                return jsonify({
                    'error': 'Invalid request: game ID mismatch'
                }), 400
            
            # Convert to domain model
            domain_game = GameMapperWeb.web_to_domain_game(web_game)
            
            # Validate the board
            if not game_service.validate_game_board(domain_game):
                return jsonify({
                    'error': 'Invalid game board: board validation failed'
                }), 400
            
            # Check if game has already ended
            if game_service.is_game_ended(domain_game):
                return jsonify({
                    'error': 'Game has already ended'
                }), 400
            
            # Get computer's next move
            result_game = game_service.get_next_move(domain_game)
            
            # Convert back to web model
            web_result = GameMapperWeb.domain_to_web_game(result_game)
            
            # Return the result
            return jsonify(web_result.to_dict()), 200
            
        except Exception as e:
            return jsonify({
                'error': f'Internal server error: {str(e)}'
            }), 500
    
    return game_bp
