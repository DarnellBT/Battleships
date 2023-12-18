"""components

Functions: 
initialise_board
create_battleships
horizontal_placement
vertical_placement
place_battleships"""

from io import TextIOWrapper
from typing import Callable
from flask import json
from config import BOARD_SIZE, BATTLESHIPS_FILENAME

def initialise_board(size: int=BOARD_SIZE) -> list[list[str | None]]:
    """Takes `size` as an int value with default value `BOARD_SIZE`. Returns initialised board as a
    list of list of str or None values.
    """
    board: list[list[str | None]]
    board_row: list[str | None]
    board = []
    for _ in range(size):
        board_row = []
        for _ in range(size):
            board_row.append(None)
        board.append(board_row)
    return board

def create_battleships(filename: str=BATTLESHIPS_FILENAME) -> dict[str, int]:
    """Takes `filename` as a str value with default value `BATTLESHIPS_FILENAME`. Returns
    battleships as a dict of str and int key-value pairs.
    """
    file: TextIOWrapper
    lines: list[str]
    battleships: dict[str, int]
    ship_name: str
    ship_length: str
    # Each line in 'filename' has it's newline character removed if it is present and then split
    # by the comma in each line where the left of the comma is assigned to battleship and the
    # right of the comma is assigned to ship_size.
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    battleships = {}
    for line in lines:
        ship_name, ship_length = line.strip().split(',')
        battleships.update({ship_name: int(ship_length)})
    return battleships

def horizontal_placement(
        board: list[list[str | None]],
        ship_name: str,
        ship_length: int,
        x_coordinate_start: int,
        y_coordinate: int
    ) -> bool:
    """Takes `board` as list of list of str or None values, `ship_name` as a str value,
    `ship_length` as an int value, `x_coordinate_start` as an int value and `y_coordinate` as an
    int value. Returns if there was a collision during placement as a bool. Places the left most
    part of a boat at a selected x coordinate.
    """
    has_horizontal_placement_collision: bool
    x_coordinate_end: int
    x_coordinate: int
    cell: str | None
    has_horizontal_placement_collision = False
    # Checks if whole ship wil be on board.
    if not 0 <= x_coordinate_start <= len(board) - ship_length:
        has_horizontal_placement_collision = True
        return has_horizontal_placement_collision
    if not 0 <= y_coordinate <= len(board) - 1:
        has_horizontal_placement_collision = True
        return has_horizontal_placement_collision
    # Checks if there are collisions with other ships.
    x_coordinate_end = x_coordinate_start + ship_length
    for cell in board[y_coordinate][x_coordinate_start:x_coordinate_end]:
        if cell is not None:
            has_horizontal_placement_collision = True
            return has_horizontal_placement_collision
    # Places ship on board.
    for x_coordinate in range(x_coordinate_start, x_coordinate_end):
        board[y_coordinate][x_coordinate] = ship_name
    return has_horizontal_placement_collision

def vertical_placement(
        board: list[list[str | None]],
        ship_name: str,
        ship_length: int,
        x_coordinate: int,
        y_coordinate_start: int
    ) -> bool:
    """Takes `board` as list of list of str or None values, `ship_name` as a str value,
    `ship_length` as an int value, `x_coordinate` as an int value and `y_coordinate_start` as an
    int value. Returns if there was a collision during placement as a bool. Places the top most
    part of a boat at a selected y coordinate.
    """
    has_vertical_placement_collision: bool
    y_coordinate_end: int
    y_coordinate_range: list[str | None]
    y_coordinate: int
    has_vertical_placement_collision = False
    # Checks if whole ship wil be on board.
    if not 0 <= x_coordinate <= len(board) - 1:
        has_vertical_placement_collision = True
        return has_vertical_placement_collision
    if not 0 <= y_coordinate_start <= len(board) - ship_length:
        has_vertical_placement_collision = True
        return has_vertical_placement_collision
    # Checks if there are collisions with other ships.
    y_coordinate_end = y_coordinate_start + ship_length
    for y_coordinate_range in board[y_coordinate_start:y_coordinate_end]:
        if y_coordinate_range[x_coordinate] is not None:
            has_vertical_placement_collision = True
            return has_vertical_placement_collision
    # Places ship on board.
    for y_coordinate in range(y_coordinate_start, y_coordinate_end):
        board[y_coordinate][x_coordinate] = ship_name
    return has_vertical_placement_collision

def place_battleships(
        board: list[list[str | None]],
        ships: dict[str, int],
        algorithm: Callable[[], None] | None=None
    ) -> list[list[str | None]]:
    """Takes Places ships for player"""
    ship_name: str
    placement: list[str]
    x_coordinate: int
    y_coordinate: int
    cell_y_coordinate: int
    ship: tuple[str, int]
    if algorithm is not None:
        algorithm()
    else:
        try:
            with open('placement.json', 'r', encoding='utf-8') as placement_json:
                for ship_name, placement in json.load(placement_json).items():
                    x_coordinate = int(placement[0])
                    y_coordinate = int(placement[1])
                    if placement[2] == 'h':
                        horizontal_placement(
                            board,
                            ship_name,
                            ships[ship_name],
                            x_coordinate,
                            y_coordinate
                        )
                    elif placement[2] == 'v':
                        vertical_placement(
                            board,
                            ship_name,
                            ships[ship_name],
                            x_coordinate,
                            y_coordinate
                        )
                    else:
                        print('Invalid orientation')
        except FileNotFoundError:
            # This is the default placement for battleships is 'placement.json' is not found.
            for cell_y_coordinate, ship in enumerate(ships.items()):
                horizontal_placement(board, *ship, 0, cell_y_coordinate)
    return board
