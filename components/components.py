"""
Contains functions:
initialise_board
create_battleships
place_battleships
"""
from pathlib import Path

# This is the type for board_state
BoardState = list[list[str | None]]

def initialise_board(size: int = 10) -> BoardState:
    """Initialises board."""
    board_state: BoardState = []
    row: list[None]
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(None)
        board_state.append(row)
    return board_state

def create_battleships(filename: str = Path(__file__).parent.resolve() / 'battleships.txt') -> dict[str, int]:
    """Creates battleships."""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    battleships: dict[str, int] = dict()
    ship: str
    ship_size: str
    for line in lines:
        # Each line in 'filename' has it's newline character removed if it is present and then split by the comma in each line where the left of the comma is assigned to ship and the right of the comma is assigned to ship_size.
        ship, ship_size = line.replace('\n', '').split(',')
        battleships[ship] = int(ship_size)
    return battleships

def place_battleships(board_state: BoardState, ships: dict[str, int]) -> BoardState:
    """Places battleships for the AI"""
    new_board_state: BoardState = board_state
    board_size: int = len(new_board_state)
    for ship, ship_size in ships.items():
        # This is for a horizontal placement for each ship from the left.
        for row in range(board_size):
            if any([new_board_state[row][ship_column] is not None for ship_column in range(ship_size)]):
                continue
            # Once a clear row to place ships is found the ship is placed and then the loop is broken out of.
            for ship_column in range(ship_size):
                new_board_state[row][ship_column] = ship
            break
    print(new_board_state)
    return new_board_state
