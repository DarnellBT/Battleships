"""
Contains functions:
initialise_board
create_battleships
place_battleships
"""

# This is the type for board_state
Board = list[list[dict[str, int] | None]]

def initialise_board(size: int = 10) -> Board:
    """Initialises board."""
    board_state: Board = [[None for _ in range(size)] for _ in range(size)]
    return board_state

def create_battleships():
    """Creates battleships."""

def place_battleships():
    """Places battleships."""
