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
#############################################################################
import argparse
import sys
import random


# Number of rows and columns in a board.
NUM_ROWS = 10
NUM_COLS = 10

# Player designations
PLAYER1 = "Player 1"
PLAYER2 = "Player 2"

# Ship types
CARRIER =    {'length': 5, 'symbol': "C"}
BATTLESHIP = {'length': 4, 'symbol': "B"}
CRUISER =    {'length': 3, 'symbol': "r"}
SUBMARINE =  {'length': 3, 'symbol': "S"}
DESTROYER =  {'length': 2, 'symbol': "D"}



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
    for i in range(0,NUM_ROWS):
        x = []
        for j in range(0, NUM_COLS):
            x.append(" ")
        b.append(x)
    return b


# Actually "make" the board we will use.
board = BuildBoard()


def print_board_letters_on_top(b):
    """Function to pretty print a board"""

    # Save the numeric value of the letter A.
    A_value = ord("A")

    def _print_divider():
        """ Helper funtion to print a divider row"""
        print("---", end="")
        for j in range(0, NUM_COLS):
            print("+---", end="")
        print("+")

    # Print the Column headers, A-J
    print("   ", end="")
    for j in range(0, NUM_COLS):
        # chr() turns a number into a character. This lets us walk through
        # the alphabet using numbers.
        print("| " + chr(A_value + j) + " ", end="")
    print("|")

    # Print each Row
    for i in range(0,NUM_ROWS):
        # First print the row divider...
        _print_divider()

        # Then print the row name, 1-10. Note that we need to handle
        # cases when the number is 1 vs 2 digits.
        if i >= 9:
            print(str(i+1) + " ", end="")
        else:
            print(" " + str(i+1) + " ", end="")

        # Finally print the Board row itself.
        for j in range(0, NUM_COLS):
            print("| " + str(b[i][j]) + " ", end="")
        print("|")

    # Once we've printed all of the Board, print a final Divider.
    _print_divider()


def print_board_numbers_on_top(b):
    """Function to pretty print a board"""

    # Save the numeric value of the letter A.
    A_value = ord("A")

    def _print_divider():
        """ Helper funtion to print a divider row"""
        print("---", end="")
        for j in range(0, NUM_COLS):
            print("+---", end="")
        print("+")

    # Print the Column headers, 1 - 10
    print("   ", end="")
    for j in range(0, NUM_COLS - 1):
        print("| " + str(j + 1) + " ", end="")
    print("| " + str(j + 2) + "|")

    # Print each Row
    for i in range(0,NUM_ROWS):
        # First print the row divider...
        _print_divider()

        # Then print the row name, A-J.
        # chr() turns a number into a character. This lets us walk through
        # the alphabet using numbers.
        print(" " + chr(A_value + i) + " ", end="")

        # Finally print the Board row itself.
        for j in range(0, NUM_COLS):
            print("| " + str(b[i][j]) + " ", end="")
        print("|")

    # Once we've printed all of the Board, print a final Divider.
    _print_divider()


# Set the default print function.
print_board = print_board_numbers_on_top


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
print_board(board)

place_all_ships(board)

print(player)
print("")
print_board(board)

