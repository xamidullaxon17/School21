from flask import Flask, render_template, redirect, url_for
from di.container import Container
from web.route.game_controller import create_game_routes
from domain.model.game_board import GameBoard
from domain.model.current_game import CurrentGame
import uuid

app = Flask(__name__)

# DI Container orqali service olish
container = Container()
game_service = container.get_game_service()

# API route (POST /game/{UUID})
game_routes = create_game_routes(game_service)
app.register_blueprint(game_routes)

# HTML o'yinlar uchun xotira (game_id -> CurrentGame)
html_games = {}


def get_or_create_game(game_id):
    if game_id not in html_games:
        board = GameBoard()
        html_games[game_id] = CurrentGame(board, game_id)
    return html_games[game_id]


def get_winner_text(current_game):
    board_data = current_game.get_board().get_board()

    def check(player):
        for row in board_data:
            if all(c == player for c in row): return True
        for col in range(3):
            if all(board_data[r][col] == player for r in range(3)): return True
        if all(board_data[i][i] == player for i in range(3)): return True
        if all(board_data[i][2-i] == player for i in range(3)): return True
        return False

    if check(1): return "You Won! 🎉"
    if check(2): return "You Lose! 😢"
    if len(current_game.get_board().get_empty_cells()) == 0: return "Draw! 🤝"
    return ""


@app.route('/')
def home():
    game_id = str(uuid.uuid4())
    return redirect(url_for('play', game_id=game_id))


@app.route('/play/<game_id>')
def play(game_id):
    current_game = get_or_create_game(game_id)
    board = current_game.get_board().get_board()
    ended = game_service.is_game_ended(current_game)
    winner = get_winner_text(current_game)
    return render_template('myhome.html', board=board, game_id=game_id,
                           ended=ended, winner=winner)


@app.route('/mark/<game_id>/<int:i>/<int:j>')
def mark(game_id, i, j):
    current_game = get_or_create_game(game_id)

    if game_service.is_game_ended(current_game):
        return redirect(url_for('play', game_id=game_id))

    board = current_game.get_board()

    if board.get_cell(i, j) != 0:
        return redirect(url_for('play', game_id=game_id))

    # Foydalanuvchi yurishi (1 = X)
    board.set_cell(i, j, 1)

    # Kompyuter yurishi (Minimax)
    if not game_service.is_game_ended(current_game):
        current_game = game_service.get_next_move(current_game)
        html_games[game_id] = current_game

    return redirect(url_for('play', game_id=game_id))


@app.route('/reset/<game_id>')
def reset(game_id):
    board = GameBoard()
    html_games[game_id] = CurrentGame(board, game_id)
    return redirect(url_for('play', game_id=game_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)












# $id = "11111111-1111-1111-1111-111111111111"

# Invoke-RestMethod -Uri "http://localhost:5000/game/$id" `
#   -Method POST `
#   -ContentType "application/json" `
#   -Body '{"gameId":"11111111-1111-1111-1111-111111111111","board":[[1,0,0],[0,0,0],[0,0,0]]}'