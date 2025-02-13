#!/usr/bin/python3
#############################################################################
#
#                   Battleship - Constants
#
#############################################################################

# Number of rows and columns in a board.
NUM_ROWS = 10
NUM_COLS = 10

# Player designations
PLAYER1 = "Player 1"
PLAYER2 = "Player 2"

# Ship types
CARRIER =    {'length': 5, 'symbol': "C"}
BATTLESHIP = {'length': 4, 'symbol': "B"}
CRUISER =    {'length': 3, 'symbol': "R"}
SUBMARINE =  {'length': 3, 'symbol': "S"}
DESTROYER =  {'length': 2, 'symbol': "D"}

# Marks for misses and hits.
MISS = "."
HIT = "X"


if __name__ == "__main__":
    print("Battleship Constants")
    print("NUM_ROWS:", NUM_ROWS)
    print("NUM_COLS:", NUM_COLS)
    print("PLAYER1:", PLAYER1)
    print("PLAYER2:", PLAYER2)
    print("CARRIER:", CARRIER)
    print("BATTLESHIP:", BATTLESHIP)
    print("CRUISER:", CRUISER)
    print("SUBMARINE:", SUBMARINE)
    print("DESTROYER:", DESTROYER)
    print("MISS:", MISS)
    print("HIT:", HIT)

