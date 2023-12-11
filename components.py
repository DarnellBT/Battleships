""" components module: contains functions 
    initialise_board
    create_battleships
    place_battleships"""

from pathlib import Path
from random import randint

# This is the type for board_state
type BoardState = list[list[str | None]]
DEFAULT_FILENAME: Path = 'battleships.txt' #Path(__file__).parent.resolve() /
# Iteration limit for placement algorithm
ITERATION_LIMIT: int = 100

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

def create_battleships(filename: Path = DEFAULT_FILENAME) -> dict[str, int]:
    """Creates battleships."""
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    battleships: dict[str, int] = {}
    ship: str
    ship_size: str
    for line in lines:
        # Each line in 'filename' has it's newline character removed if it is present and then split
        # by the comma in each line where the left of the comma is assigned to ship and the right of
        # the comma is assigned to ship_size.
        ship, ship_size = line.replace('\n', '').split(',') # use strip?
        battleships[ship] = int(ship_size)
    return battleships

def verticle_placement(
        board_state: BoardState,
        ship_name: str, ship_length: int,
        column: int, row_start: int
    ) -> bool:
    """Places the top most part of a boat at a selected row."""
    has_verticle_placement_collision: bool = False
    if not 0 <= column <= len(board_state) - 1:
        has_verticle_placement_collision = True
        return has_verticle_placement_collision
    if not 0 <= row_start <= len(board_state) - ship_length:
        has_verticle_placement_collision = True
        return has_verticle_placement_collision
    row_end = row_start + ship_length
    row_range: map = map(lambda board_row : board_row[column], board_state[row_start:row_end])
    if any(None is not cell for cell in row_range):
        has_verticle_placement_collision = True
        return has_verticle_placement_collision
    for row in range(row_start, row_end):
        board_state[row][column] = ship_name
    return has_verticle_placement_collision

def horizontal_placement(
        board_state: BoardState,
        ship_name: str, ship_length: int,
        column_start: int,  row: int
    ) -> bool:
    """Places the left most part of a boat at a selected column."""
    has_horizontal_placement_collision: bool = False
    if not 0 <= column_start <= len(board_state) - ship_length:
        has_horizontal_placement_collision = True
        return has_horizontal_placement_collision
    if not 0 <= row <= len(board_state) - 1:
        has_horizontal_placement_collision = True
        return has_horizontal_placement_collision
    column_end = column_start + ship_length
    if any(None is not tile for tile in board_state[row][column_start:column_end]):
        has_horizontal_placement_collision = True
        return has_horizontal_placement_collision
    for column in range(column_start, column_end):
        board_state[row][column] = ship_name
    return has_horizontal_placement_collision

def place_battleships(board_state: BoardState, ships: dict[str, int]) -> BoardState:
    """Places battleships for the AI"""

    # Orders ships from by length from shortest to longest boat.
    ships_not_placed = sorted(ships.items(), reverse=True, key=lambda ship : ship[1])
    iteration_count: int = 0
    while ships_not_placed and iteration_count < ITERATION_LIMIT:
        iteration_count += 1
        cell_column: int = randint(0, len(board_state))
        cell_row: int = randint(0, len(board_state))
        is_verticle_placement = bool(randint(0, 2))
        if is_verticle_placement:
            if verticle_placement(board_state, *ships_not_placed[0], cell_column, cell_row):
                continue
        else:
            if horizontal_placement(board_state, *ships_not_placed[0], cell_column, cell_row):
                continue
        ships_not_placed.pop(0)
    return board_state
