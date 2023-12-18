"""game engine

Functions:
attack
cli_coordinates_input
simple_game_loop
"""

from components import create_battleships, initialise_board, place_battleships
from config import BOARD_SIZE

def attack(
        coordinate: tuple[int, int],
        board: list[list[str | None]],
        battleships: dict[str, int]
    ) -> bool:
    """Takes a cell coordinate to be attacked as tuple of two int values, a board to be attacked
    as list of list of str and None values, battleships as dict of str and int key-value pairs.
    Returns if the attack can be successfull as a bool.
    """
    ship_in_cell: str | None
    battleships_ship_in_cell: int | None
    # This checks if the attck is on the board.
    if not (0 <= coordinate[0] <= BOARD_SIZE - 1 and 0 <= coordinate[1] <= BOARD_SIZE - 1):
        return False
    ship_in_cell = board[coordinate[1]][coordinate[0]]
    # This checks if the cell is empty.
    if ship_in_cell is None:
        return False
    battleships_ship_in_cell = battleships.get(ship_in_cell)
    # This checks that `ship_in_cell` is a ship.
    if battleships_ship_in_cell is None:
        return False
    # This reduces the length of the attacked ship and changes the cell it is on to an empty cell.
    battleships.update({ship_in_cell: battleships_ship_in_cell - 1})
    board[coordinate[1]][coordinate[0]] = None
    return True

def cli_coordinates_input() -> tuple[int, int]:
    """Returns the coordinate that the player inputs.
    """
    input_x: str
    input_y: str
    x_coordinate: int
    y_coordinate: int
    coordinate: tuple[int, int]
    while True:
        input_x = ''
        input_y = ''
        # If the returned coordinate is the tuple of two int values `(-1, -1)` then the game quits.
        x_coordinate = -1
        y_coordinate = -1
        print('Please enter the coordinate of the cell to attack.',
              'You can enter q to quit coordinate input.', sep='\n')
        input_x = input('Please enter an x value: ')
        if input_x.isdigit():
            x_coordinate = int(input_x)
        elif input_x == 'q':
            if input('Please enter q again if you want to quit battleships: ') == 'q':
                break
            continue
        else:
            continue
        input_y = input('Please enter an y value: ')
        if input_y.isdigit():
            y_coordinate = int(input_y)
            break
        if input_y == 'q':
            if input('Please enter q again if you want to quit battleships: ') == 'q':
                x_coordinate = -1
                break
    coordinate = (x_coordinate, y_coordinate)
    return coordinate

def simple_game_loop() -> None:
    """This is a simple game loop contained in the command line that only allows for a player to
    attack battleships. This is useful for testing that player attacks work in iscolation.
    """
    battleships: dict[str, int]
    board: list[list[str | None]]
    coordinates: tuple[int, int]
    attacked_cells: list[tuple[int, int]]
    print('Welcome to Battleships.')
    # This creates the battleships and the board and places the battleships on the board.
    battleships = create_battleships()
    board = place_battleships(initialise_board(BOARD_SIZE), battleships)
    # The initial value for coordinate is `(BOARD_SIZE, BOARD_SIZE)` so that the conditions to
    # enter the while loop are satisfied.
    coordinates = (BOARD_SIZE, BOARD_SIZE)
    attacked_cells = []
    print('x coordinate are from 0 to', BOARD_SIZE - 1, 'from left to right.')
    print('y coordinate are from 0 to', BOARD_SIZE - 1, 'from top to bottom.')
    # The while loop condition checks if any of the battleships have a value more than 0. If so,
    # all battleships have sunken and the game can end.
    while any(battleships.values()):
        while (
            coordinates[0] >= BOARD_SIZE
            or coordinates[1] >= BOARD_SIZE
            or coordinates in attacked_cells
        ):
            coordinates = cli_coordinates_input()
        if coordinates == (-1, -1):
            print('You quit.')
            break
        attacked_cells.append(coordinates)
        if attack(coordinates, board, battleships):
            print('Hit.')
        else:
            print('Miss.')
    print('Game over.')

if __name__ == '__main__':
    simple_game_loop()
