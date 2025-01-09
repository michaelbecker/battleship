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
#############################################################################
import argparse
import sys


# Number of rows and columns in a board.
NUM_ROWS = 10
NUM_COLS = 10

# Save which player we are.
PLAYER1 = "Player 1"
PLAYER2 = "Player 2"
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

