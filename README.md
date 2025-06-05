# Battleships

## Battleships Setup

Before setting up Battleships you should have at least Python 3.12+ installed as this was the version used write Battleships. You should also have python as a PATH variable.

### Using the config.py module to alter battleship settings

There are four configs that can be altered within the config.py module which is found within the Battleships directory:

+ `BOARD_SIZE` - determines how many cells make up a side length of the battleships board. This is set to 10 by default.

+ `DEFAULT_FILENAME` - determines the filename of the file containing the battleships' names and battleships' lengths. This is set to `'battleships.txt'` by default.

+ `DIFFICULTY` - determines the difficulty of the ai the player plays against. This is set to `'Normal'` by default. (The options are `'Normal'` and `'Easy'`.)

+ `ITERATION_LIMIT` - determines the maximum number of attepts for a valid random battleship placement that can happen when setting up the ai's board. this is set to 100 by default.

### game_engine.py for debugging

The game_engine.py can be used for debugging purposes to test player attacking. To run this module you should be in the Battleships directory within a command-line interface and must enter the command:

```powershell
python game_engine.py
```

or

```powershell
python3 game_engine.py
```

Now after this the user is prompted to enter and x and y coordinate to attack. Once entered you would be shown if you missed a ship or if you hit a ship. This will continue until all ships are sunken. You can cancel a coordinate by entering `q` once and you can quit the game by entering `q` twice.

### mp_game_engine.py for playing against ai in the command line

The mp_game_engine.py can be used to play Battleships agaist an ai opponent in a command-line. To run this module you should be in the Battleships directory within a command-line interface and must enter the command:

```powershell
python mp_game_engine.py
```

or

```powershell
python3 mp_game_engine.py
```

Now after this the user is prompted to enter and x and y coordinate to attack. Once entered you would be shown if you missed a ship or if you hit a ship. This will the be followed by an ai attack on the player ships where the player and ai will take turns attacking. This will continue until all ai ships are sunken or all player ships are sunken. You can cancel a coordinate by entering `q` once and you can quit the game by entering `q` twice.

### main.py for playing against ai in a web browser

The main.py can be used to play Battleships agaist an ai opponent in a web browser GUI. To run this module you should be in the Battleships directory within a command-line interface and must enter the command:

```powershell
python main.py
```

or

```powershell
python3 main.py
```

Now after this you should enter [http://127.0.0.1:5000/placement]() into a web browser in order place your Battleships. The you should click on the green `Send Game` to begin playing the game. The player starts frist and the ai follows with their turn automatically. Clicking on a cell on the large board indicates a player attack where the cell will turn light-blue if the player misses a ship and turn red if the player hits a ship. A smaller board to the right of the large board represents the player board and shows where the ai has attacked where each cell will turn dark-blue if the ai misses your ship and turn red if the ai hits your ship. The game ends once either all ai ship are sunken or all player ships are sunken.
