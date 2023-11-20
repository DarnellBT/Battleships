"""
Contains the function:
index
"""

from flask import Flask, render_template
from components import components

app = Flask(__name__)

BOARD_SIZE: int = 10
ships: dict[str, int] = components.create_battleships()

@app.route('/')
def index():
    """The main function injects elements for main.html."""
    return render_template('main.html', player_board=components.place_battleships(components.initialise_board(), ships))

@app.route('/placement')
def placement():
    """The placement function injects placement elemenets for placement.html"""
    return render_template('placement.html', board_size=BOARD_SIZE, ships=ships)

if __name__ == '__main__':
    app.run()
