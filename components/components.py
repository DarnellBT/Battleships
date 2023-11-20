"""
Contains functions:
initialise_board
create_battleships
place_battleships
"""

# This is the type for board_state
Board = list[list[str | None]]

def initialise_board(size: int = 10) -> Board:
    """Initialises board."""
    board_state: Board = [[None for _ in range(size)] for _ in range(size)]
    return board_state

def create_battleships(filename: str = 'battleships.txt') -> dict[str, int]:
    """Creates battleships."""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    battleships: dict[str, int] = {key: int(size) for key, size in line.split(',') for line in lines}
    return battleships

def place_battleships():
    """Places battleships."""
