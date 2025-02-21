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
import socket
from constants import *
from print_board import (print_board, set_print_board, NUMBERS_ON_TOP,
                         LETTERS_ON_TOP)


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


def process_defense(b, c1, c2):
    """ Handle getting coordinates from our opponents."""
    # Translate from UI coordinates to internal coordinates.
    row, col = get_binary_coordinates(c1, c2)

    if b[row][col] == " ":
        b[row][col] = MISS
        return "M"

    elif b[row][col] == MISS:
        print("Error - Dup request")
        return "E"

    elif b[row][col] == HIT:
        print("Error - Dup request")
        return "E"

    else:
        ship = b[row][col]
        b[row][col] = HIT

        if is_sunk(b, ship):
            return ship
        else:
            return "H"


def build_board():
    """Create a board, which is a list of lists and return it."""
    b = []
    for row in range(0,NUM_ROWS):
        x = []
        for col in range(0, NUM_COLS):
            x.append(" ")
        b.append(x)
    return b


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

    if result == "M":
        b[row][col] = MISS
    elif result == "H":
        b[row][col] = HIT
    else:
        print("UNKNOWN RESULT!")


def run_game_defense(coordinates):
    c1 = coordinates[0:1]
    c2 = coordinates[1:]
    c1 = c1.upper()
    if not 'A' <= c1 <= 'J':
        print("Invalid letter coordinate")
        return "E"
    if not 1 <= int(c2) <= 10:
        print("Invalid number coordinate")
        return "E"

    if args.verbose:
        print("(" + c1 + ", " + str(c2) + ")")

    result = process_defense(my_board, c1, c2)
    return result


def run_game_offense(c1, c2):
    try:
        result = input(str(c1) + str(c2) + ": [H/M]? ")
    except:
        print("\nExiting game")
        sys.exit(-1)
    return result


class GameState:
    GS_RUN_OFFENCE = 1
    GS_RUN_DEFENSE = 2

game_state = GameState.GS_RUN_OFFENCE


################################ MAIN SCRIPT ################################

# Actually "make" the boards we will use.
my_board = build_board()
opponent_board = build_board()
player = "unknown"


def print_my_board():
    if args.verbose:
        print("My Board")
        print_board(my_board)


def print_opponent_board():
    if args.verbose:
        print("Opponent Board")
        print_board(opponent_board)


def check_args():
    """Verify the input to the script is ok before using it."""

    # the global keyword lets us change a global var.
    global player
    global print_board

    args.player = args.player.upper()

    if args.player == "P1":
        player = PLAYER1
    elif args.player == "P2":
        player = PLAYER2
    else:
        print("Unknown player")
        sys.exit(-1)

    if args.letters_on_top:
        set_print_board(LETTERS_ON_TOP)
    else:
        set_print_board(NUMBERS_ON_TOP)



def run_local_game():
    """ """
    global game_state

    while True:

        print_my_board()

        match game_state:

            case GameState.GS_RUN_DEFENSE:
                try:
                    c = input("Enter coordinates [A1]-[J10]: ")
                except:
                    print("\nExiting game")
                    sys.exit(-1)

                #
                #   This will be called by the opponent computer.
                #
                result = run_game_defense(c)

                print(result)
                game_state = GameState.GS_RUN_OFFENCE

            case GameState.GS_RUN_OFFENCE:
                c1, c2 = offence_guess(opponent_board)

                while True:
                    #
                    #   We call this on the opponent computer.
                    #
                    try:
                        result = input(str(c1) + str(c2) + ": [H/M]? ")
                    except:
                        print("\nExiting game")
                        sys.exit(-1)

                    result = result.upper()
                    if result == "M" or "H" in result:
                        offence_result(opponent_board, result)
                        break
                    else:
                        print("Unknown response, please try again.")

                print_opponent_board()
                game_state = GameState.GS_RUN_DEFENSE

            case _:
                print("I'M LOST!!!!")


def run_network_game():
    """ """
    global game_state

    if game_state == GameState.GS_RUN_DEFENSE:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((args.ip, 50500))

        print("DEBUG - listen() - ", socket.gethostname())
        server.listen()

        print("DEBUG - accept()")
        (client, address) = server.accept()
        print("DEBUG - accept() RETURNED")
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.ip, 50500))

    while True:

        print_my_board()

        match game_state:

            case GameState.GS_RUN_DEFENSE:
                try:
                    #c = input("Enter coordinates [A1]-[J10]: ")
                    c = client.recv()
                except:
                    print("\nExiting game")
                    sys.exit(-1)

                #
                #   This will be called by the opponent computer.
                #
                result = run_game_defense(c)

                #print(result)
                client.send(result)
                game_state = GameState.GS_RUN_OFFENCE

            case GameState.GS_RUN_OFFENCE:
                c1, c2 = offence_guess(opponent_board)

                while True:
                    #
                    #   We call this on the opponent computer.
                    #
                    try:
                        #result = input(str(c1) + str(c2) + ": [H/M]? ")
                        result = client.recv()
                    except:
                        print("\nExiting game")
                        sys.exit(-1)

                    result = result.upper()
                    if result == "M" or "H" in result:
                        offence_result(opponent_board, result)
                        break
                    else:
                        print("Unknown response, please try again.")

                print_opponent_board()
                game_state = GameState.GS_RUN_DEFENSE

            case _:
                print("I'M LOST!!!!")



# Use the python library tools to get our inputs.
parser = argparse.ArgumentParser()
parser.add_argument("player")
parser.add_argument("--network",
                    help="If present, this is a network game.",
                    action="store_true")
parser.add_argument("--ip",
                    help="IP address if we are running a network game.")
parser.add_argument("--letters-on-top",
                    help="Swaps labeling of rows and columns",
                    action="store_true")
parser.add_argument("--verbose",
                    help="Enable verbose mode",
                    action="store_true")
args = parser.parse_args()

check_args()

print("Computer is", player)
print("")

place_all_ships(my_board)


if player == PLAYER1:
    game_state = GameState.GS_RUN_OFFENCE
else:
    game_state = GameState.GS_RUN_DEFENSE


if args.network:
    run_network_game()
else:
    run_local_game()






