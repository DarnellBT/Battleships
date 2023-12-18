"""Config module contains the following attributes:
`BOARD_SIZE` being an int value that determines how many cells make up a side length of the
battleships board.
`DEFAULT_FILENAME` being a str value that determines the filename of the file containing the
battleships' names and battleships' lengths each seperated by a comma and each battlechip on a new
line.
`DIFFICULTY` being a str value that determines the difficulty of the ai the player plays against.
The options are `'Normal'` and `'Easy'`.
ITERATION_LIMIT being an int value that determines the maximum number of attepts for a valid
random battleship placement that can happen when setting up the ai's board.
"""
BOARD_SIZE: int
DEFAULT_FILENAME: str
DIFFICULTY: str
ITERATION_LIMIT: int
BOARD_SIZE = 10
BATTLESHIPS_FILENAME = 'battleships.txt'
DIFFICULTY = 'Normal'
ITERATION_LIMIT = 100
