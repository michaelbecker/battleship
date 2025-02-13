#!/usr/bin/python3
#############################################################################
#
#                   Battleship - Print Board functions
#
#   Print boards to stdout.
#
#############################################################################
from constants import *


def _print_board_letters_on_top(b):
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


def _print_board_numbers_on_top(b):
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
print_board = _print_board_numbers_on_top


NUMBERS_ON_TOP = True
LETTERS_ON_TOP = False


def set_print_board(num_on_top):
    if num_on_top:
        print_board = _print_board_numbers_on_top
    else:
        print_board = _print_board_letters_on_top


if __name__ == "__main__":
    print("Battleship print_board")
    b = []
    for row in range(0,NUM_ROWS):
        x = []
        for col in range(0, NUM_COLS):
            x.append(" ")
        b.append(x)
    print_board(b)
    

