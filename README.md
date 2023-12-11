# Testing Documentation

---

This Battleships project uses the [https://docs.pytest.org/en/7.4.x/](pytest framework) to unit test each module.
The pytest framework requires Python 3.7+ or PyPy3 versions.

---

## Initialisation of Virtual Environment for Testing

+ To start testing modules a virtual environment can be created.
+ In this virtual environment pytest can be installed.

> The example below shows these using PowerShell.

```powershell
PS> python -m venv venv
PS> .\venv\Scripts\activate
(venv) PS> python -m pip install pytest
```

---

components

verticle_place(boat, length, row_start, column)
horizontal_place(boat, length, row, column_start)

```python
mssgs = []
def show(f):
    def wrapper(*args, **kwargs):
        mssg = f(*args, **kwargs)
        mssgs.append((f.__name__, mssg))
        return mssg
    return wrapper

boats = {
            "AC"    :   5,
            "Ba"    :   4,
            "Cr"    :   3,
            "Su"    :   3,
            "De"    :   2
        }
SIZE = 10
minimum_size = max(boats.values())
if SIZE < minimum_size:
    SIZE = minimum_size
board = [[None for column in range(SIZE)] for row in range(SIZE)]

#@show
def verticle_placement(boat_name, boat_length, row_start, column):
    """Places the top most part of a boat at a selected row."""
    if not 0 <= column <= SIZE - 1:
        return "The column not in the range [0 - %d]." % (SIZE - 1)
    if not 0 <= row_start <= SIZE - boat_length:
        return " The row is not in the range [0 - %d]." % (SIZE - boat_length)
    row_end = row_start + boat_length
    if any(None is not tile for tile in map(lambda board_row : board_row[column], board[row_start:row_end])):
        return "The placement of the %s collides with a boat that is already on the board." % boat_name
    for row in range(row_start, row_end):
        board[row][column] = boat_name

#@show
def horizontal_placement(boat_name, boat_length, row, column_start):
    """Places the left most part of a boat at a selected column."""
    if not 0 <= row <= SIZE - 1:
        return "The row not in the range [0 - %d]." % (SIZE - 1)
    if not 0 <= column_start <= SIZE - boat_length:
        return " The column is not in the range [0 - %d]." % (SIZE - boat_length)
    column_end = column_start + boat_length
    if any(None is not tile for tile in board[row][column_start:column_end]):
        return "The placement of the %s collides with a boat that is already on the board." % boat_name
    for column in range(column_start, column_end):
        board[row][column] = boat_name

def placement():
    """Places boats on the board"""
    # If there is not a placement on a full pass on the last boat then switch orientation of placement.
    # Bound the size of the board bigger or equal to the length of the longest boat.
    from random import randint
    # Orders boats from by length from shortest to longest boat.
    boats_not_placed = sorted(boats.items(), reverse=True, key=lambda x : x[1])
    # Iteration limit for placement algorithm.
    ITERATION_LIMIT = 100
    iteration_count = 0
    while boats_not_placed and iteration_count < ITERATION_LIMIT:
        iteration_count += 1
        row = randint(0, SIZE)
        column = randint(0, SIZE)
        is_verticle_placement = bool(randint(0, 2))
        if is_verticle_placement:
            if bool(verticle_placement(*boats_not_placed[0], row, column)):
                continue
        else:
            if bool(horizontal_placement(*boats_not_placed[0], row, column)):
                continue
        boats_not_placed.pop(0)
    #if iteration_count == 1000:
    #    print("The iteration limit of %d was reached." % ITERATION_LIMIT)
    #print(f"{iteration_count=}\n{boats_not_placed=}")

placement()
print(*board, *mssgs, sep='\n')
```
