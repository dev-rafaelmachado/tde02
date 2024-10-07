from structure.board import Board


# interface Player
class Player:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"Player({self.symbol})"

    def make_move(self, board: Board):
        pass
