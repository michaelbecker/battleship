#!/usr/bin/python3
#############################################################################
#
#                   Battleship
#
#   Implemention of the Battleship game.
#
#   We are going to try and use the standard coding style:
#   https://peps.python.org/pep-0008/
#
#   Since this is a learning exercise, we're going to be more verbose with
#   our comments than normal.
#
#   Rules:
#   https://www.hasbro.com/common/instruct/battleship.pdf
#
#   TODO:
#   - Break into Modules
#   - logging for debug - https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
#
#############################################################################
import argparse
import sys
import random
from constants import *
from print_board import print_board


def get_ship_name(ship_id):
    if ship_id == "C":
        return "Carrier"
    if ship_id == "B":
        return "Battleship"
    if ship_id == "R":
        return "Cruiser"
    if ship_id == "S":
        return "Submarine"
    if ship_id == "D":
        return "Destroyer"
    return "UNKNOWN SHIP!"


def place_ship(b, ship):
    """ Place all 5 ships on a board randomly. """

    def _place_ship_horizontal(b, ship):
        """ Handle ships that lie horizontally """
        range_end = NUM_COLS - ship['length']
        start_col = random.randint(0, range_end)
        row = random.randint(0, NUM_ROWS - 1)
        for col in range(start_col, start_col + ship['length']):
            if b[row][col] != " ":
                return False
        for col in range(start_col, start_col + ship['length']):
            b[row][col] = ship["symbol"]
        return True


    def _place_ship_vertical(b, ship):
        """ Handle ships that lie vertically """
        range_end = NUM_ROWS - ship['length']
        start_row = random.randint(0, range_end)
        col = random.randint(0, NUM_COLS - 1)
        for row in range(start_row, start_row + ship['length']):
            if b[row][col] != " ":
                return False
        for row in range(start_row, start_row + ship['length']):
            b[row][col] = ship["symbol"]
        return True


    success = False

    while not success:
        is_horizontal = random.randint(0,1)

        if is_horizontal:
            success = _place_ship_horizontal(b, ship)
        else:
            success = _place_ship_vertical(b, ship)


def is_sunk(b, ship):
    for row in range(0,NUM_ROWS):
        for col in range(0, NUM_COLS):
            if b[row][col] == ship:
                return False
    return True


def get_binary_coordinates(c1, c2):
    """ Translate from UI coordinates to internal coordinates."""
    if not isinstance(c1, str):
        sys.exit("get_binary_coordinates: c1 - Invalid type")

    if not isinstance(c2, str):
        sys.exit("get_binary_coordinates: c2 - Invalid type")

    row = ord(c1) - ord("A")
    col = int(c2) - 1
    return row, col


def get_string_coordinates(c1, c2):
    """ Translate from internal coordinates to UI coordinates."""
    if not isinstance(c1, int):
        sys.exit("get_string_coordinates: c1 - Invalid type")

    if not isinstance(c2, int):
        sys.exit("get_string_coordinates: c2 - Invalid type")

    row = chr(c1 + ord("A"))
    col = str(c2 + 1)
    return row, col


def process_defense(b, c1, c2):
    """ Handle getting coordinates from our opponents."""
    # Translate from UI coordinates to internal coordinates.
    row, col = get_binary_coordinates(c1, c2)

    if b[row][col] == " ":
        b[row][col] = MISS
        return "MISS"

    elif b[row][col] == MISS:
        return "ERROR - DUP"

    elif b[row][col] == HIT:
        return "ERROR - DUP"

    else:
        ship = b[row][col]
        b[row][col] = HIT

        if is_sunk(b, ship):
            return "HIT, SUNK " + get_ship_name(ship)
        else:
            return "HIT"


def place_all_ships(b):
    """ Place all the ships we have. """
    place_ship(b, CARRIER);
    place_ship(b, BATTLESHIP);
    place_ship(b, CRUISER);
    place_ship(b, SUBMARINE);
    place_ship(b, DESTROYER);


player = "unknown"


def BuildBoard():
    """Create a board, which is a list of lists and return it."""
    b = []
    for row in range(0,NUM_ROWS):
        x = []
        for col in range(0, NUM_COLS):
            x.append(" ")
        b.append(x)
    return b


# Actually "make" the boards we will use.
my_board = BuildBoard()
opponent_board = BuildBoard()


def check_args():
    """Verify the input to the script is ok before using it."""

    # the global keyword lets us change a global var.
    global player
    global print_board

    if args.player == "p1":
        player = PLAYER1
    elif args.player == "p2":
        player = PLAYER2
    else:
        print("Unknown player")
        sys.exit(-1)

    if args.letters_on_top:
        print_board = print_board_letters_on_top


def offence_guess(b):
    row, col = offence_guess.guess[0], offence_guess.guess[1]

    row = row + 1
    if row >= NUM_ROWS:
        row = 0
    col = col + 1
    if col >= NUM_COLS:
        col = 0

    offence_guess.guess = (row, col)
    return get_string_coordinates(row, col)

offence_guess.guess = (5, 5)


def offence_result(b, result):
    row, col = offence_guess.guess[0], offence_guess.guess[1]

    if result == "MISS":
        b[row][col] = MISS
    else:
        b[row][col] = HIT
        



################################ MAIN SCRIPT ################################


# Use the python library tools to get our inputs.
parser = argparse.ArgumentParser()
parser.add_argument("player")
parser.add_argument("--letters-on-top",
                    help="Swaps labeling of rows and columns",
                    action="store_true")
args = parser.parse_args()

check_args()

print(player)
print("")
print_board(my_board)

place_all_ships(my_board)



while True:
    print(player)
    print("")
    print_board(my_board)

    c = input("Enter coordinates [A1]-[J10]: ")
    c1 = c[0:1]
    c2 = c[1:]
    c1 = c1.upper()
    if not 'A' <= c1 <= 'J':
        print("Invalid coordinate")
        continue
    if not 1 <= int(c2) <= 10:
        print("Invalid coordinate")
        continue

    print("(" + c1 + ", " + str(c2) + ")")

    result = process_defense(my_board, c1, c2)
    print(result)

    c1, c2 = offence_guess(opponent_board)

    while True:
        result = input(str(c1) + str(c2) + ": [HIT/MISS]? ")
        result = result.upper()

        if result == "MISS" or "HIT" in result:
            offence_result(opponent_board, result)
            print_board(opponent_board)
            break
        else:
            print("Unknown response, please try again.")



