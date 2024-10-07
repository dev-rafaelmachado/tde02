import time
from typing import Optional
from structure.board import Board
from structure.players.player import Player
from structure.players.computer_player import ComputerPlayer
from structure.players.human_player import HumanPlayer
from utils.console import clear_screen
from utils.input import get_user_choice


class Game:
    def __init__(self, board_size: int = 3):
        """
        Initializes a new instance of the Game class.
        """
        self.board: Board = Board(board_size, board_size)
        self.player_1: Player
        self.player_2: Player
        self.turn_counter: int = 0

    def start(self):
        """
        Starts the game by setting up the game mode and playing the game.
        """
        self.setup_game_mode()
        self.play()

    def setup_game_mode(self):
        """
        Configures the game mode and strategy.
        """
        mode = get_user_choice(
            "Which mode do you want to play?\n1. Human vs Computer\n2. Computer vs Computer\n",
            [1, 2],
            "Enter your choice: ",
        )
        strategy = get_user_choice(
            "\nWith strategy computer uses:\n1. Random\n2. Minimax\n3. Alpha-Beta\n",
            [1, 2, 3],
            "Enter your choice: ",
        )

        player_1_symbol = self.get_user_symbol(
            "\nPlayer 1 symbol (X or O, X always goes first): "
        )
        player_2_symbol = "O" if player_1_symbol == "X" else "X"

        self.player_1, self.player_2 = self.create_players(
            mode, player_1_symbol, player_2_symbol, strategy
        )

    @staticmethod
    def get_user_symbol(prompt: str) -> str:
        """
        Gets the player's symbol, ensuring that it is 'X' or 'O'.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The player's symbol.
        """
        symbol = None
        while symbol not in ["X", "O"]:
            symbol = input(prompt).upper()
        return symbol

    @staticmethod
    def create_players(
        mode: int, player_1_symbol: str, player_2_symbol: str, strategy: int
    ) -> tuple[Player, Player]:
        """
        Creates the players based on the game mode and symbols provided.

        Args:
            mode (int): The game mode.
            player_1_symbol (str): The symbol for player 1.
            player_2_symbol (str): The symbol for player 2.
            strategy (int): The strategy to be used by the computer players.

        Returns:
            tuple[Player, Player]: A tuple containing the player objects.
        """
        if mode == 1:
            return HumanPlayer(player_1_symbol), ComputerPlayer(
                player_2_symbol, strategy
            )
        return ComputerPlayer(player_1_symbol, strategy), ComputerPlayer(
            player_2_symbol, strategy
        )

    def play(self):
        """
        Executes the main game loop until a winner is found or it's a tie.
        """
        winner = None
        while not winner and not self.board.is_full():
            self.play_turn()
            winner = self.check_for_winner()

        self.display_result(winner)

    def play_turn(self):
        """
        Executes a game turn, alternating between players.
        """
        clear_screen()
        self.display_board()

        current_player = self.player_1 if self.turn_counter % 2 == 0 else self.player_2
        start_time = time.time()

        current_player.make_move(self.board)

        finish_time = time.time()
        clear_screen()
        self.display_board()

        print(f"\nTurn {self.turn_counter + 1}: Player {current_player.symbol}")
        print(f"Time taken: {finish_time - start_time:.2f} seconds")

        self.turn_counter += 1
        input("Press Enter to continue...")

    def check_for_winner(self) -> Optional[Player]:
        """
        Checks if there is a winner on the board.

        Returns:
            Optional[Player]: The winning player, or None if there is no winner.
        """
        winner_symbol = self.board.check_winner()
        if winner_symbol == self.player_1.symbol:
            return self.player_1
        elif winner_symbol == self.player_2.symbol:
            return self.player_2
        return None

    def display_board(self):
        """
        Displays the board on the console.
        """
        print(self.board)

    def display_result(self, winner: Optional[Player]):
        """
        Displays the game result, indicating the winner or a tie.

        Args:
            winner (Optional[Player]): The winning player, or None if it's a tie.
        """
        if winner:
            print(f"Player {winner.symbol} wins!")
        else:
            print("It's a tie!")
