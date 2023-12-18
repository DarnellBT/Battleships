"""mp_game_engine

Attributes:
ai_attacked_cells: list[tuple[int, int]]
ai_attacked_sequence: dict[tuple[int, int], str]
players: dict[str, tuple[list[list[str | None]], dict[str, int]]]
attack_direction: dict[str, str]

Functions:
generate_random_coordinate
check_adjacent_cell_on_board
get_adjacent_cell_coordinates
advance_directional_attack
generate_attack
ai_placement
ai_opponent_game_loop
"""

from random import randint, choice
from components import (
    horizontal_placement,
    vertical_placement,
    create_battleships,
    initialise_board,
    place_battleships
)
from game_engine import cli_coordinates_input, attack
from config import BOARD_SIZE, DIFFICULTY, ITERATION_LIMIT

ai_attacked_cells: list[tuple[int, int]]
ai_attacked_sequence: dict[tuple[int, int], str]
players: dict[str, tuple[list[list[str | None]], dict[str, int]]]
attack_direction: dict[str, str]
ai_attacked_cells = []
ai_attacked_sequence = {}
players = {'ai': ([], {}), 'player': ([], {})}
attack_direction = {'direction': ''}

def generate_random_coordinate() -> tuple[int, int]:
    """Returns a generated random coordinate as a tuple of two int values `attack_coordinate`.
    """
    x_coordinate: int
    y_coordinate: int
    attack_coordinate: tuple[int, int]
    while True:
        x_coordinate = randint(0, BOARD_SIZE - 1)
        y_coordinate = randint(0, BOARD_SIZE - 1)
        attack_coordinate = (x_coordinate, y_coordinate)
        if attack_coordinate not in ai_attacked_cells:
            ai_attacked_sequence[attack_coordinate] = ''
            break
    return attack_coordinate

def check_adjacent_cell_on_board(adjacent_cell: tuple[str, tuple[int, int]]) -> bool:
    """Takes an adjacent cell as a tuple of a str and tuple of two int values and returns if the
    adjacent is on the board or not as a bool value `is_on_board`. This is a helper function for
    `get_adjacent_cell_coordinates`.
    """
    is_within_x_range: bool
    is_within_y_range: bool
    is_on_board: bool
    is_within_x_range = 0 <= adjacent_cell[1][0] <= BOARD_SIZE - 1
    is_within_y_range = 0 <= adjacent_cell[1][1] <= BOARD_SIZE - 1
    is_on_board = is_within_x_range and is_within_y_range
    return is_on_board

def get_adjacent_cell_coordinates(
    cell_coordniate: tuple[int, int],
    excluded_directions: list[str] | None=None
) -> dict[str, tuple[int, int]]:
    """Takes a cell coordinate as a tuple of two int values and can take an argument
    `excluded_direction` of type list[str] with a default value of `[]`. This list can contain
    values of type str being `'left'`, `'right'`, `'up'` and `'down'` resulting in the
    corresponding cells being excluded from the final return value.returns a dict of str and
    tuple[int, int] key-value pairs. The keys are the directions relative to the cell coordinate
    taken by the function for each adjacent cell. The possible keys are str values being `'left'`,
    `'right'`, `'up'` and `'down'`. The values are the cells' coordinates as a tuple of two int
    values.
    """
    adjacent_cells: dict
    left_cell: tuple[int, int]
    right_cell: tuple[int, int]
    top_cell: tuple[int, int]
    bottom_cell: tuple[int, int]
    adjacent_cell: tuple[str, tuple[int, int]]
    players_player: tuple[list[list[str | None]], dict[str, int]] | None
    if excluded_directions is None:
        excluded_directions = []
    adjacent_cells = {}
    left_cell = (cell_coordniate[0] - 1, cell_coordniate[1])
    right_cell = (cell_coordniate[0] + 1, cell_coordniate[1])
    top_cell = (cell_coordniate[0], cell_coordniate[1] - 1)
    bottom_cell = (cell_coordniate[0], cell_coordniate[1] + 1)
    # Selects valid adjacent cells
    for adjacent_cell in filter(
        check_adjacent_cell_on_board,
        [('left', left_cell), ('right', right_cell), ('up', top_cell), ('down', bottom_cell)]
    ):
        players_player = players.get('player')
        if players_player is None:
            break
        if (
            adjacent_cell[0] not in excluded_directions
            and players_player[0][adjacent_cell[1][1]][adjacent_cell[1][0]] is not None
        ):
            adjacent_cells.update([adjacent_cell])
    return adjacent_cells

def advance_directional_attack(last_attack_coordinate: tuple[int, int]) -> tuple[int, int]:
    """Takes a cell coordinate as a tuple of two int values `last_attack_coordinate` and returns
    the next coordinate to be attacked as a tuple of two int values `attack_coordinate`.
    """
    attack_coordinate: tuple[int, int]
    if attack_direction.get('direction') == 'left':
        attack_coordinate = (last_attack_coordinate[0] - 1, last_attack_coordinate[1])
    elif attack_direction.get('direction') == 'right':
        attack_coordinate = (last_attack_coordinate[0] + 1, last_attack_coordinate[1])
    elif attack_direction.get('direction') == 'up':
        attack_coordinate = (last_attack_coordinate[0], last_attack_coordinate[1] - 1)
    elif attack_direction.get('direction') == 'down':
        attack_coordinate = (last_attack_coordinate[0], last_attack_coordinate[1] + 1)
    else:
        attack_coordinate = generate_random_coordinate()
    return attack_coordinate

def generate_attack() -> tuple[int, int]:
    """generate_attack"""
    adjacent_cells: dict[str, tuple[int, int]]
    attack_coordinate: tuple[int, int]
    direction: str
    first_attack_coordinate: tuple[int, int]
    first_attack_result: str
    last_attack_coordinate: tuple[int, int]
    # Easy only has random attacks
    if DIFFICULTY == 'Easy':
        ai_attacked_sequence.clear()
        attack_coordinate = generate_random_coordinate()
        return attack_coordinate
    # Normal attack sequence finds a ship and hits along the ship until an enttire contiguous row
    # has sank. Once the attack has reached the edge of a ship it goes back to its first hit and
    # hits in the opposite direction until it reaches an end.
    if DIFFICULTY == 'Normal':
        if len(ai_attacked_sequence) == 1:
            first_attack_coordinate, first_attack_result = list(ai_attacked_sequence.items())[0]
            if first_attack_result == 'Miss':
                ai_attacked_sequence.clear()
                attack_coordinate = generate_random_coordinate()
                return attack_coordinate
            if first_attack_result == 'Hit':
                adjacent_cells = get_adjacent_cell_coordinates(first_attack_coordinate)
                if len(adjacent_cells) > 0:
                    direction, attack_coordinate = choice(list(adjacent_cells.items()))
                    attack_direction.update({'direction': direction})
                    return attack_coordinate
            ai_attacked_sequence.clear()
            attack_coordinate = generate_random_coordinate()
            return attack_coordinate
        if len(ai_attacked_sequence) == 2:
            second_attack_coordinate, second_attack_result = list(ai_attacked_sequence.items())[1]
            if second_attack_result == 'Miss':
                adjacent_cells = get_adjacent_cell_coordinates(
                    list(ai_attacked_sequence.keys())[0],
                    # The attack direction will be defaulted as `'right'` in the case `None` is
                    # retruned from the get method.
                    [attack_direction.get('direction', 'right')]
                )
                if len(adjacent_cells) > 0:
                    direction, attack_coordinate = choice(list(adjacent_cells.items()))
                    attack_direction.update({'direction': direction})
                else:
                    ai_attacked_sequence.clear()
                    attack_coordinate = generate_random_coordinate()
            elif second_attack_result == 'Hit':
                attack_coordinate = advance_directional_attack(second_attack_coordinate)
            else:
                attack_coordinate = generate_random_coordinate()
            return attack_coordinate
        if len(ai_attacked_sequence) >= 3:
            if list(ai_attacked_sequence.values())[-1] == 'Miss':
                # checks for two previous misses, if so a ship is likely sunken
                if list(ai_attacked_sequence.values()).count('Miss') == 2:
                    ai_attacked_sequence.clear()
                    attack_coordinate = generate_random_coordinate()
                    return attack_coordinate
                first_attack_coordinate = list(ai_attacked_sequence.keys())[0]
                if attack_direction.get('direction') == 'left':
                    attack_direction.update({'direction': 'right'})
                elif attack_direction.get('direction') == 'right':
                    attack_direction.update({'direction': 'left'})
                elif attack_direction.get('direction') == 'up':
                    attack_direction.update({'direction': 'down'})
                elif attack_direction.get('direction') == 'down':
                    attack_direction.update({'direction': 'up'})
                attack_coordinate = advance_directional_attack(first_attack_coordinate)
                return attack_coordinate
            if list(ai_attacked_sequence.values())[-1] == 'Hit':
                last_attack_coordinate = list(ai_attacked_sequence.keys())[-1]
                if attack_direction.get('direction') == 'left':
                    attack_coordinate = (last_attack_coordinate[0] - 1, last_attack_coordinate[1])
                elif attack_direction.get('direction') == 'right':
                    attack_coordinate = (last_attack_coordinate[0] + 1, last_attack_coordinate[1])
                elif attack_direction.get('direction') == 'up':
                    attack_coordinate = (last_attack_coordinate[0], last_attack_coordinate[1] - 1)
                elif attack_direction.get('direction') == 'down':
                    attack_coordinate = (last_attack_coordinate[0], last_attack_coordinate[1] + 1)
                else:
                    attack_coordinate = generate_random_coordinate()
                return attack_coordinate
    ai_attacked_sequence.clear()
    attack_coordinate = generate_random_coordinate()
    return attack_coordinate

def ai_placement() -> None:
    """This determines the placement of each ai ship on the ai's board."""
    ai_board: list[list[str | None]]
    ai_battleships: dict[str, int]
    ships_not_placed: list[tuple[str, int]]
    iteration_count: int
    x_coordinate: int
    y_coordinate: int
    ai_board = initialise_board(BOARD_SIZE)
    ai_battleships = create_battleships()
    ships_not_placed = sorted(ai_battleships.items(), reverse=True, key=lambda ship: ship[1])
    iteration_count = 0
    # Chooses random placements for each ai ship.
    while len(ships_not_placed) > 0 and iteration_count < ITERATION_LIMIT:
        iteration_count += 1
        x_coordinate = randint(0, BOARD_SIZE - 1)
        y_coordinate = randint(0, BOARD_SIZE - 1)
        is_horizontal_placement = bool(randint(0, 1))
        if is_horizontal_placement:
            if horizontal_placement(ai_board, *ships_not_placed[0], x_coordinate, y_coordinate):
                continue
        else:
            if vertical_placement(ai_board, *ships_not_placed[0], x_coordinate, y_coordinate):
                continue
        ships_not_placed.pop(0)
    players.update({'ai': (ai_board, ai_battleships)})

def ai_opponent_game_loop() -> None:
    """This is a game loop with an ai opponent where you play Battleships within a command-line
    interface.
    """
    player_battleships: dict[str, int]
    coordinate: tuple[int, int]
    player_attacked_cells: list[tuple[int, int]]
    row: str
    players_player: tuple[list[list[str | None]], dict[str, int]] | None
    players_ai: tuple[list[list[str | None]], dict[str, int]] | None
    cell_size: int
    cell_row: list[str | None]
    ship_in_cell: str | None
    ai_attack_coordinate: tuple[int, int]
    ai_placement()
    player_battleships = create_battleships()
    players.update({'player': (
        place_battleships(initialise_board(BOARD_SIZE), player_battleships),
        player_battleships
    )})
    print('Welcome to Battleships.')
    player_attacked_cells = []
    print('x coordinate are from 0 to', BOARD_SIZE - 1, 'from left to right.')
    print('y coordinate are from 0 to', BOARD_SIZE - 1, 'from top to bottom.')
    while True:
        # Creates the player's board for them to see in the command-line.
        print('Player board: ')
        row = ''
        players_player = players.get('player')
        if players_player is None:
            print('The player does not exist.')
            break
        players_ai = players.get('player')
        if players_ai is None:
            print('The ai does not exist.')
            break
        cell_size = max(map(len, players_player[1].keys())) + 2
        for cell_row in players_player[0]:
            row = '|'
            for ship_in_cell in cell_row:
                if ship_in_cell is None:
                    row += ' ' * cell_size + '|'
                else:
                    row += ship_in_cell.center(cell_size) + '|'
            print('-' * len(row))
            print(row)
        print('-' * len(row))
        # The initial value for coordinate is `(BOARD_SIZE, BOARD_SIZE)` so that the conditions to
        # enter the while loop are satisfied.
        coordinate = (BOARD_SIZE, BOARD_SIZE)
        while (
            coordinate[0] >= BOARD_SIZE
            or coordinate[1] >= BOARD_SIZE
            or coordinate in player_attacked_cells
        ):
            coordinate = cli_coordinates_input()
        if coordinate == (-1, -1):
            print('You quit.')
            break
        player_attacked_cells.append(coordinate)
        if attack(coordinate, *players_ai):
            print('Hit.')
        else:
            print('Miss.')
        if not any(players_ai[1].values()):
            print('You win.')
            break
        # Generates new attack from ai.
        ai_attack_coordinate = generate_attack()
        ai_attacked_cells.append(ai_attack_coordinate)
        if attack(ai_attack_coordinate, *players_player):
            ai_attacked_sequence.update({ai_attack_coordinate: 'Hit'})
            print('You were hit.')
        else:
            ai_attacked_sequence.update({ai_attack_coordinate: 'Miss'})
            print('You were not hit.')
            continue
        if not any(players_player[1].values()):
            print('You lose.')
            break
    print('Game over.')

if __name__ == '__main__':
    ai_opponent_game_loop()
