from structure.board import Board
from structure.players.player import Player


class HumanPlayer(Player):
    def __init__(self, symbol):
        """
        Initializes a new instance of the HumanPlayer class.

        Args:
            symbol (str): The symbol representing the player on the board.
        """
        super().__init__(symbol)

    def make_move(self, board: Board):
        """
        Makes a move on the board.

        Args:
            board (Board): The game board.

        Raises:
            ValueError: If the position entered by the player is invalid.
        """
        print(f"Player {self.symbol} is making a move")
        position = input("Enter the position to move (i, j): ")
        try:
            i, j = map(int, position.split(","))
            board.make_move(self, (i, j))
        except ValueError:
            print("Invalid position")
            self.make_move(board)
