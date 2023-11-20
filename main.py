from flask import Flask, render_template
from components import components

app = Flask(__name__)

@app.route('/')
def index():
    """The main function injects elements for main.html."""
    return render_template('main.html', player_board=components.initialise_board())

if __name__ == '__main__':
    app.run()
