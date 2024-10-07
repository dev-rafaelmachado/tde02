import random
from structure.board import Board
from structure.players.player import Player


class ComputerPlayer(Player):
    def __init__(self, symbol: str, strategy: int, max_depth: int = 4):
        """
        Classe que representa um jogador de computador.

        Args:
            symbol (str): O símbolo do jogador (X ou O).
            strategy (int): A estratégia de escolha de movimento do jogador.
            max_depth (int, optional): A profundidade máxima para a busca do algoritmo Minimax. Padrão é 4.
        """
        super().__init__(symbol)
        self.strategy = strategy
        self.max_depth = max_depth

    def make_move(self, board: Board):
        """Decide qual método de escolha de movimento usar, com base na estratégia."""
        if self.strategy == 1:
            self.random_move(board)
        elif self.strategy in [2, 3]:
            best_move = self.get_best_move(board, use_alpha_beta=self.strategy == 3)
            board.make_move(self, best_move)

    def random_move(self, board: Board):
        """Escolhe um movimento aleatório entre as células disponíveis."""
        random_choice = random.choice(board.empty_cells)
        board.make_move(self, random_choice)

    def evaluate_board(self, board: Board, depth: int) -> float | None:
        """
        Avalia o estado do tabuleiro, retornando o score final ou None se o jogo não acabou.

        Args:
            board (Board): O tabuleiro atual.
            depth (int): A profundidade atual da busca.

        Returns:
            float | None: O score final do tabuleiro ou None se o jogo não acabou.
        """
        winner = board.check_winner()
        if winner is not None:
            if winner == self.symbol:
                return 1000 - depth
            else:
                return -1000 + depth

        if board.is_full():
            return 0

        return None

    def evaluate_heuristic(self, board: Board, depth: int) -> float:
        """
        Avalia o estado do tabuleiro usando uma heurística aprimorada.

        Args:
            board (Board): O tabuleiro atual.
            depth (int): A profundidade atual da busca.

        Returns:
            float: O score do tabuleiro com base na heurística.
        """
        score = 0

        for i in range(board.height):
            score += self.evaluate_line(board.grid[i])

        for i in range(board.width):
            score += self.evaluate_line([row[i] for row in board.grid])

        score += self.evaluate_line(
            [board.grid[i][i] for i in range(min(board.height, board.width))]
        )
        score += self.evaluate_line(
            [
                board.grid[i][board.width - 1 - i]
                for i in range(min(board.height, board.width))
            ]
        )

        score -= depth

        return score

    def evaluate_line(self, line: list) -> float:
        """
        Avalia uma linha do tabuleiro.

        Args:
            line (list): A linha do tabuleiro a ser avaliada.

        Returns:
            float: O score da linha.
        """
        player_count = line.count(self.symbol)
        opponent_count = line.count("O" if self.symbol == "X" else "X")
        empty_count = line.count(None)

        if player_count == 3:
            return 100
        elif opponent_count == 3:
            return -100

        # Prioriza ganhar ou bloquear
        if player_count == 2 and empty_count == 1:
            return 10  # Jogada que leva à vitória
        elif opponent_count == 2 and empty_count == 1:
            return -90  # Jogada que bloqueia o oponente (ajuste de peso)

        # Penaliza jogadas que apenas ocupam espaço
        if player_count == 1 and empty_count == 2:
            return 1
        elif opponent_count == 1 and empty_count == 2:
            return -1

        return 0

    def get_best_move(self, board: Board, use_alpha_beta=False):
        """
        Usa o algoritmo Minimax (com ou sem poda alfa-beta) para determinar o melhor movimento.

        Args:
            board (Board): O tabuleiro atual.
            use_alpha_beta (bool, optional): Indica se a poda alfa-beta deve ser usada. Padrão é False.

        Returns:
            tuple[int, int]: As coordenadas do melhor movimento.
        """
        best_score = float("-inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")

        options = board.empty_cells.copy()
        for cell in options:
            board.make_move(self, cell)
            score = self.minimax(
                board,
                0,
                is_maximizing=False,
                use_alpha_beta=use_alpha_beta,
                alpha=alpha,
                beta=beta,
            )
            board.undo_move(cell)

            print(f"Considerando jogada {cell} com score {score}")

            if score > best_score:
                best_score = score
                best_move = cell

            if use_alpha_beta:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        if best_move is None:
            raise ValueError("Nenhuma jogada válida encontrada.")

        print(
            f"Player {self.symbol} made a move at ({best_move[0]}, {best_move[1]}) with a score of {best_score}\n\n"
        )
        return best_move

    def minimax(
        self,
        board: Board,
        depth: int,
        is_maximizing: bool,
        use_alpha_beta=False,
        alpha=float("-inf"),
        beta=float("inf"),
    ) -> float:
        """
        Calcula o valor Minimax para o tabuleiro atual, com opção de usar poda alfa-beta.

        Args:
            board (Board): O tabuleiro atual.
            depth (int): A profundidade atual da busca.
            is_maximizing (bool): Indica se é a vez do jogador atual maximizar o score.
            use_alpha_beta (bool, optional): Indica se a poda alfa-beta deve ser usada. Padrão é False.
            alpha (float, optional): O valor alfa para a poda alfa-beta. Padrão é float("-inf").
            beta (float, optional): O valor beta para a poda alfa-beta. Padrão é float("inf").

        Returns:
            float: O valor Minimax para o tabuleiro atual.
        """
        score = self.evaluate_board(board, depth)
        if score is not None:
            return score

        if depth == self.max_depth:
            return self.evaluate_heuristic(board, depth)

        if is_maximizing:
            return self.get_max_score(board, depth, use_alpha_beta, alpha, beta)
        else:
            return self.get_min_score(board, depth, use_alpha_beta, alpha, beta)

    def get_max_score(
        self,
        board: Board,
        depth: int,
        use_alpha_beta=False,
        alpha=float("-inf"),
        beta=float("inf"),
    ) -> float:
        """
        Obtém o melhor score maximizando o jogador atual, com opção de usar poda alfa-beta.

        Args:
            board (Board): O tabuleiro atual.
            depth (int): A profundidade atual da busca.
            use_alpha_beta (bool, optional): Indica se a poda alfa-beta deve ser usada. Padrão é False.
            alpha (float, optional): O valor alfa para a poda alfa-beta. Padrão é float("-inf").
            beta (float, optional): O valor beta para a poda alfa-beta. Padrão é float("inf").

        Returns:
            float: O melhor score maximizando o jogador atual.
        """
        best_score = float("-inf")
        for cell in board.empty_cells:
            board.make_move(self, cell)
            score = self.minimax(
                board,
                depth + 1,
                is_maximizing=False,
                use_alpha_beta=use_alpha_beta,
                alpha=alpha,
                beta=beta,
            )
            board.undo_move(cell)
            best_score = max(score, best_score)
            if use_alpha_beta:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score

    def get_min_score(
        self,
        board: Board,
        depth: int,
        use_alpha_beta=False,
        alpha=float("-inf"),
        beta=float("inf"),
    ) -> float:
        """
        Obtém o melhor score minimizando o oponente, com opção de usar poda alfa-beta.

        Args:
            board (Board): O tabuleiro atual.
            depth (int): A profundidade atual da busca.
            use_alpha_beta (bool, optional): Indica se a poda alfa-beta deve ser usada. Padrão é False.
            alpha (float, optional): O valor alfa para a poda alfa-beta. Padrão é float("-inf").
            beta (float, optional): O valor beta para a poda alfa-beta. Padrão é float("inf").

        Returns:
            float: O melhor score minimizando o oponente.
        """
        best_score = float("inf")
        opponent = Player(symbol="O" if self.symbol == "X" else "X")

        for cell in board.empty_cells:
            board.make_move(opponent, cell)
            score = self.minimax(
                board,
                depth + 1,
                is_maximizing=True,
                use_alpha_beta=use_alpha_beta,
                alpha=alpha,
                beta=beta,
            )
            board.undo_move(cell)
            best_score = min(score, best_score)
            if use_alpha_beta:
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score
