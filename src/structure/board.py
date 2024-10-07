from typing import Optional
from colorama import Fore, Style


from typing import Optional


class Board:
    """
    Represents a game board.

    Attributes:
        grid (list[list[str | None]]): The grid representing the cells of the board.
        empty_positions (list[tuple[int, int]]): The positions of the empty cells.
        width (int): The width of the board.
        height (int): The height of the board.
    """

    grid: list[list[str | None]]
    empty_positions: list[tuple[int, int]]
    width: int
    height: int

    def __init__(self, width: int, height: int):
        """
        Initializes a new instance of the Board class.

        Args:
            width (int): The width of the board.
            height (int): The height of the board.
        """
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.empty_positions = []
        for i in range(height):
            for j in range(width):
                self.grid[i][j] = None
                if self.grid[i][j] is None:
                    self.empty_positions.append((i, j))

    def __str__(self):
        """
        Returns a string representation of the board.

        Returns:
            str: The string representation of the board.
        """
        rows = []
        for i, row in enumerate(self.grid):
            cells = []
            for cell in row:
                if cell == "X":
                    cells.append(f"{Fore.RED}{cell}{Style.RESET_ALL}")
                elif cell == "O":
                    cells.append(f"{Fore.BLUE}{cell}{Style.RESET_ALL}")
                else:
                    cells.append(" ")
            row_str = " │ ".join(cells)
            rows.append(f" {row_str} ")
            if i < self.height - 1:
                rows.append("".join(["───┼"] * (self.width - 1)) + "───")
        return "\n".join(rows)

    def __repr__(self):
        """
        Returns a string representation of the board.

        Returns:
            str: The string representation of the board.
        """
        return f"Board({self.width}, {self.height})"

    @property
    def cells(self):
        """
        Gets the cells of the board.

        Returns:
            list[list[str | None]]: The cells of the board.
        """
        return self.grid

    @property
    def empty_cells(self):
        """
        Gets the positions of the empty cells.

        Returns:
            list[tuple[int, int]]: The positions of the empty cells.
        """
        return self.empty_positions

    def is_full(self):
        """
        Checks if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return len(self.empty_positions) == 0

    def check_winner(self) -> Optional[str]:
        """
        Checks if there is a winner on the board.

        Returns:
            Optional[str]: The symbol of the winner, or None if there is no winner.
        """

        def check_equal(values: list[Optional[str]]) -> Optional[str]:
            if values[0] is not None and all(val == values[0] for val in values):
                return values[0]
            return None

        for row in self.grid:
            if (result := check_equal(row)) is not None:
                return result

        for col in range(self.width):
            if (
                result := check_equal(
                    [self.grid[row][col] for row in range(self.height)]
                )
            ) is not None:
                return result

        if self.width == self.height:
            if (
                result := check_equal([self.grid[i][i] for i in range(self.width)])
            ) is not None:
                return result
            if (
                result := check_equal(
                    [self.grid[i][self.width - 1 - i] for i in range(self.width)]
                )
            ) is not None:
                return result

        return None  # Nenhum vencedor

    def make_move(self, player, position: tuple[int, int]) -> None:
        """
        Makes a move on the board.

        Args:
            player: The player making the move.
            position (tuple[int, int]): The position to make the move.

        Raises:
            ValueError: If the position is invalid or already occupied.
        """
        if (
            position[0] < 0
            or position[0] >= self.height
            or position[1] < 0
            or position[1] >= self.width
        ):
            raise ValueError("Invalid position")
        if self.grid[position[0]][position[1]] is not None:
            raise ValueError("Position already occupied")

        self.grid[position[0]][position[1]] = player.symbol
        self.empty_positions.remove(position)

    def undo_move(self, position: tuple[int, int]) -> None:
        """
        Undoes a move on the board.

        Args:
            position (tuple[int, int]): The position to undo the move.

        Raises:
            ValueError: If the position is not occupied.
        """
        if self.grid[position[0]][position[1]] is None:
            raise ValueError("Position not occupied")

        self.grid[position[0]][position[1]] = None
        self.empty_positions.append(position)
