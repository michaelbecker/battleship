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
import logging
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


def get_binary_coordinates(ui_row, ui_col):
    """ Translate from UI coordinates to internal coordinates."""
    if not isinstance(ui_row, str):
        sys.exit("get_binary_coordinates: c1 - Invalid type")

    if not isinstance(ui_col, str):
        sys.exit("get_binary_coordinates: c2 - Invalid type")

    binary_row = ord(ui_row) - ord("A")
    binary_col = int(ui_col) - 1
    return binary_row, binary_col


def get_UI_coordinates(c1, c2):
    """ Translate from internal coordinates to UI coordinates."""
    if not isinstance(c1, int):
        sys.exit("get_string_coordinates: c1 - Invalid type")

    if not isinstance(c2, int):
        sys.exit("get_string_coordinates: c2 - Invalid type")

    row = chr(c1 + ord("A"))
    col = str(c2 + 1)
    return row, col


def place_ship_randomly(b, ship):
    """ Place a ship on a board randomly. """

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


def place_all_ships_randomly(b):
    """ Place all 5 ships on a board randomly. """
    place_ship_randomly(b, CARRIER);
    place_ship_randomly(b, BATTLESHIP);
    place_ship_randomly(b, CRUISER);
    place_ship_randomly(b, SUBMARINE);
    place_ship_randomly(b, DESTROYER);


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
    return get_UI_coordinates(row, col)

offence_guess.guess = (5, 5)


def offence_result(b, result):
    row, col = offence_guess.guess[0], offence_guess.guess[1]

    if result == "M":
        b[row][col] = MISS
    elif result == "H":
        b[row][col] = HIT
    else:
        print("UNKNOWN RESULT!")


def process_defense(b, ui_row, ui_col):
    """ Handle getting coordinates from our opponents."""


def run_game_defense(coordinates):
    ui_row = coordinates[0:1]
    ui_col = coordinates[1:]
    ui_row = ui_row.upper()

    if not 'A' <= ui_row <= 'J':
        print("Invalid letter coordinate")
        return "E"
    
    if not 1 <= int(ui_col) <= 10:
        print("Invalid number coordinate")
        return "E"

    if args.verbose:
        print("(" + ui_row + ", " + str(ui_col) + ")")

    # Translate from UI coordinates to internal coordinates.
    row, col = get_binary_coordinates(ui_row, ui_col)

    if my_board[row][col] == " ":
        my_board[row][col] = MISS
        return "M"

    elif my_board[row][col] == MISS:
        print("Error - Dup request")
        return "E"

    elif my_board[row][col] == HIT:
        print("Error - Dup request")
        return "E"

    else:
        ship = my_board[row][col]
        my_board[row][col] = HIT

        if is_sunk(my_board, ship):
            return ship
        else:
            return "H"


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
    global args
    global logger
    global port

    args.player = args.player.upper()

    if args.player == "P1":
        player = PLAYER1
    elif args.player == "P2":
        player = PLAYER2
    else:
        print("Unknown player")
        sys.exit(-1)

    if args.port:
        port = int(args.port)

    if args.letters_on_top:
        set_print_board(LETTERS_ON_TOP)
    else:
        set_print_board(NUMBERS_ON_TOP)

    if args.log_level:
        args.log_level = args.log_level.upper()
        args.numeric_level = getattr(logging, args.log_level, None)
        if not isinstance(args.numeric_level, int):
            print('Invalid log level: ', args.log_level)
            sys.exit(-1)
        logging.basicConfig(level=args.numeric_level)
    else:
        logging.basicConfig(level=logging.WARNING)


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

port = 50500


def run_network_game():
    """ This is the main loop for the network game. """
    global game_state

    #
    #   If we are player 2, we will be the server.
    #
    if game_state == GameState.GS_RUN_DEFENSE:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((args.ip, port))

        logger.debug("listen() - %s", socket.gethostname())
        server_socket.listen()

        logger.debug("accept()")
        (client_socket, address) = server_socket.accept()
        logger.debug("accept() RETURNED")
    #
    #   Else we are player 1 and we will be the client.
    #
    else:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((args.ip, port))

    #
    #   Main loop for the network game.
    #
    while True:

        print_my_board()

        logger.debug("Game State: %d", game_state)
        match game_state:

            case GameState.GS_RUN_DEFENSE:
                try:
                    #
                    #   If we are in the defense phase, we need to read the coordinates
                    #   from our opponent
                    #
                    c = client_socket.recv(3).decode("utf-8")
                    logger.debug("Received: %s", c)

                except Exception as e:
                    logger.debug("Exception!", exec_info=True)
                    print("\nExiting game")
                    sys.exit(-1)

                result = run_game_defense(c)

                logger.debug("Sending: %s", result)
                client_socket.send(result.encode("utf-8"))

                #
                #   We switch to Offense now.
                #
                game_state = GameState.GS_RUN_OFFENCE

            case GameState.GS_RUN_OFFENCE:
                c1, c2 = offence_guess(opponent_board)
                c = c1 + c2
                logger.debug("Sending: %s", c)

                #
                #   We call this on the opponent computer.
                #
                try:
                    client_socket.send(c.encode("utf-8"))
                    result = client_socket.recv(1)
                    result = result.decode("utf-8")
                    logger.debug("Received: %s", result)
                except Exception as e:
                    logger.debug("Exception!", exec_info=True)
                    print("\nExiting game")
                    sys.exit(-1)

                result = result.upper()
                if result == "M" or "H" in result:
                    offence_result(opponent_board, result)
                else:
                    print("Unknown response! " + result)
                    sys.exit(-1)

                print_opponent_board()

                #
                #   We switch to Defense now.
                #
                game_state = GameState.GS_RUN_DEFENSE

            case _:
                print("I'M LOST!!!!")
                sys.exit(-1)


################################ MAIN SCRIPT ################################

# Actually "make" the boards we will use.
my_board = build_board()
opponent_board = build_board()
player = "unknown"
game_state = GameState.GS_RUN_OFFENCE

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
parser.add_argument("--port",
                    help="Set port, default is 50500")
parser.add_argument("--log-level",
                    help="DEBUG|INFO|WARNING|ERROR")

# Get the arguments from the command line.
args = parser.parse_args()

# Check the arguments to make sure they are valid.
check_args()

# Set up the logger, a lot of setup is done in check_args()
logger = logging.getLogger(__name__)

print("Computer is", player)
print("")

place_all_ships_randomly(my_board)


if player == PLAYER1:
    game_state = GameState.GS_RUN_OFFENCE
else:
    game_state = GameState.GS_RUN_DEFENSE


if args.network:
    run_network_game()
else:
    run_local_game()






