import sys
from structure.game import Game
from utils.console import clear_screen

DEFAULT_BOARD_SIZE = 4


def main():
    board_size = DEFAULT_BOARD_SIZE
    try:
        if len(sys.argv) > 1:
            board_size = int(sys.argv[1])

    except ValueError:
        print("Invalid board size. Please provide a valid integer.")
        return

    game = Game(board_size=board_size)
    game.start()


if __name__ == "__main__":
    try:
        clear_screen()
        print("🚀 Welcome to the Tic Tac Toe game!\n\n")
        main()
        print("🎉 Tank you for playing!")
    except KeyboardInterrupt:
        print("\n\n👋 Bye bye!")
