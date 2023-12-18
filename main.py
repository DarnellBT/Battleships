"""Attributes:
app: Flask
game_status: dict[str, bool]
player_attacked_cells: list[tuple[int, int]]
battleships: dict[str, int]
board: list[list[str | None]]

Function:
root
placement_interface
process_attack
"""

from io import TextIOWrapper
from flask import Flask, render_template, request, jsonify, Response, json
from components import create_battleships, initialise_board, place_battleships
from game_engine import attack
from mp_game_engine import (
    ai_attacked_cells,
    players,
    ai_placement,
    generate_attack,
    ai_attacked_sequence
)
from config import BOARD_SIZE

app: Flask
game_status: dict[str, bool]
player_attacked_cells: list[tuple[int, int]]
battleships: dict[str, int]
board: list[list[str | None]]
app = Flask(__name__)
game_status = {'game over': False, 'processing_attack': False}
player_attacked_cells = []
battleships = create_battleships()
board = initialise_board(BOARD_SIZE)

@app.route('/', methods=['GET'])
def root() -> str:
    """Returns template as str value of the `main.html` file if the request method is GET.
    """
    player_attacked_cells.clear()
    ai_attacked_cells.clear()
    battleships.update(create_battleships())
    game_status.update({'game over': False})
    return render_template(
        'main.html',
        player_board=place_battleships(board, battleships)
    )

@app.route('/placement', methods=['GET','POST'])
def placement_interface() -> tuple[Response, int] | str:
    """Returns tuple of a Response and int value which indicates ship placements from the web
    browser had been recieved if the request method is POST. Returns template as str value of the
    `placement.html` file if the request method is GET.
    """
    placement_json: TextIOWrapper
    response: tuple[Response, int]
    if request.method == 'POST':
        data = request.get_json()
        with open('placement.json', 'w', encoding='utf-8') as placement_json:
            placement_json.write(json.dumps(data, indent=4))
        ai_placement()
        players.update({'player': (place_battleships(board, battleships), battleships)})
        response = (jsonify({'message': 'Received'}), 200)
        return response
    battleships.update(create_battleships())
    return render_template('placement.html', board_size=BOARD_SIZE, ships=battleships)

@app.route('/attack', methods=['GET'])
def process_attack() -> Response:
    """Returns Response value if the request method is GET. Processes attacks between player and ai
    on web browser setup.
    """
    input_x: str | None
    input_y: str | None
    x_coordinate: int
    y_coordinate: int
    player_turn_coordinate: tuple[int, int]
    has_hit_ai: bool
    ai_turn_coordinate: tuple[int, int]
    game_status_processing: bool | None
    game_status_game_over: bool | None
    players_ai: tuple[list[list[str | None]], dict[str, int]] | None
    players_player: tuple[list[list[str | None]], dict[str, int]] | None
    game_status_processing = game_status.get('processing')
    game_status_game_over = game_status.get('game over')
    if game_status_processing or game_status_game_over:
        return Response(status=204)
    game_status.update({'processing': True})
    # Gets x and y coordinate of the cell the player clicked in the web browser.
    input_x = request.args.get('x')
    input_y = request.args.get('y')
    if input_x is None or input_y is None or game_status.get('game over'):
        game_status.update({'processing': False})
        return Response(status=204)
    x_coordinate = int(input_x)
    y_coordinate = int(input_y)
    player_turn_coordinate = (x_coordinate, y_coordinate)
    if player_turn_coordinate in player_attacked_cells:
        game_status.update({'processing': False})
        return Response(status=204)
    # Player attacks ai.
    has_hit_ai = attack(player_turn_coordinate, *players['ai'])
    player_attacked_cells.append(player_turn_coordinate)
    players_ai = players.get('ai')
    if players_ai is None:
        return Response(status=204)
    # Player wins if there are no more ai ships left.
    if not any(players_ai[1].values()):
        game_status.update({'game over': True})
        game_status.update({'processing': False})
        return jsonify({'hit': has_hit_ai, 'finished': 'Game over, player wins.'})
    players_player = players.get('player')
    if players_player is None:
        return Response(status=204)
    # Ai attacks player.
    ai_turn_coordinate = generate_attack()
    if attack(ai_turn_coordinate, *players_player):
        ai_attacked_sequence.update({ai_turn_coordinate: 'Hit'})
    else:
        ai_attacked_sequence.update({ai_turn_coordinate: 'Miss'})
    ai_attacked_cells.append(ai_turn_coordinate)
    # Ai wins if there are no more player ships left.
    if not any(players_player[1].values()):
        game_status.update({'game over': True})
        game_status.update({'processing': False})
        return jsonify({
            'hit': has_hit_ai,
            'AI_Turn': ai_turn_coordinate,
            'finished': 'Game over, ai wins.'
        })
    game_status.update({'processing': False})
    return jsonify({'hit': has_hit_ai, 'AI_Turn': ai_turn_coordinate})

if __name__ == '__main__':
    app.run()
