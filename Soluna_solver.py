from typing import List
from copy import deepcopy
from itertools import combinations

class Soluna:
    """
    A class representing the Soluna game.

    Attributes:
    - board (GameState): The current state of the Soluna board.

    Methods:
    - __init__(self, board: GameState): Initializes a Soluna game.
    - validate_board(self, board: GameState): Validates the provided board.
    - display_board(self): Displays the current state of the Soluna board.

    Raises:
    - ValueError: If the provided board is invalid.

    GameState:
    A 2D array where the rows denote the symbols and the columns denote the size of the stacks of that symbol.
    i.e. [[4, 1], [2, 2], [2, 1], []]. Represents the following board state:
    A 4 stack and 1 stack of symbol A
    two 2 stacks of symbol B
    a 2 stack and 1 stack of symbol C
    and no stack with symbol D

    Examples:
    >>> correct_board = Soluna([[5,], [1, 2], [2, 2], []])
    >>> correct_board.display_board()
    2A 2A
    2B 1B
    5C
    >>> too_many_symbols = Soluna([[4, 1], [2, 2], [2, 1], [], []])
    Traceback (most recent call last):
        ...
    ValueError: Invalid board: Board does not have exactly 4 symbols.

    >>> too_many_tiles = Soluna([[3, 1, 1], [2, 2], [2, 1], [1,]])
    Traceback (most recent call last):
        ...
    ValueError: Invalid board: Board does not have exactly 12 tiles.

    >>> non_positive_stack = Soluna([[4, 1], [2, 2], [2, 1], [0,]])
    Traceback (most recent call last):
        ...
    ValueError: Invalid board: Board's stacks must be positive integers.
    """
    GameState = List[List[int]]
    NUM_SYMBOLS = 4
    NUM_TILES = 12
    minimax_counter = 0

    def __init__(self, board: GameState) -> None:
        """
        Initialize a Soluna game.

        Parameters:
        - board: The Game State

        Raises:
        - ValueError: If the provided board is invalid.
        """
        self.validate_board(board)
        self.board = board
        self.normalize_position()

    def validate_board(self, board: GameState) -> None:
        """
        Validate the provided board.

        Parameters:
        - board: The Game State to be verified

        Raises:
        - ValueError: If the provided board is invalid.

        The validation checks include:
        1. Ensuring the board has correct amount of symbols.
        2. Verifying that the board has correct amount of tiles.
        3. Confirming that each stack has positive height.
        """
        if len(board) != Soluna.NUM_SYMBOLS:
            raise ValueError(f"Invalid board: Board does not have exactly {Soluna.NUM_SYMBOLS} symbols.")

        if sum(sum(symbol) for symbol in board if symbol) != Soluna.NUM_TILES:
            raise ValueError(f"Invalid board: Board does not have exactly {Soluna.NUM_TILES} tiles.")

        if not all(isinstance(stack, int) and stack >= 1 for symbol in board for stack in symbol):
            raise ValueError("Invalid board: Board's stacks must be positive integers.")

    def display_board(self) -> None:
        """
        Display the current state of the Soluna board.
        Each stacks is seperated by spaces and consists of a number and letter.
        The number is the size of the stack and the letter is the the top stack's symbol
        """
        labels = iter("ABCD")
        for symbol in self.board:
            label = next(labels)
            if symbol:
                print(" ".join(f"{stack}{label}" for stack in symbol))

    def normalize_position(self) -> None:
        """
        Transform self.board represented by a 2d array into a normalized equivalent 2d array.
        1. Each symbols stack sizes are given in a nonincreasing order.
        2. The number of stacks the symbols have must be in a nonincreasing order.
        3. Two symbols with the same amount of stacks must be in reverse lexicographical ordering
        """
        for i in range(Soluna.NUM_SYMBOLS):
            self.board[i] = sorted(self.board[i], reverse=True)

        self.board = sorted(self.board, key=lambda symbol: (len(symbol), symbol), reverse=True)

    def get_moves(self) -> List[GameState]:
        """
        Get all possible moves from a given state.
        """
        possible_moves = []
        board_copy = deepcopy(self.board)

        # combining stacks of same symbol
        for index, symbol in enumerate(self.board):
            distinct = set(combinations(symbol, 2))
            for (stack1, stack2) in distinct:
                self.board[index].remove(stack1)
                self.board[index].remove(stack2)
                self.board[index].append(stack1+stack2)
                self.normalize_position()
                possible_moves.append(self.board)
                self.board = deepcopy(board_copy)

        # combining stacks of different symbol
        combinations_2 = list(combinations(range(Soluna.NUM_SYMBOLS), 2))
        for (symbol1, symbol2) in combinations_2:
            matching_numbers = set(self.board[symbol1]) & set(self.board[symbol2])
            for num in matching_numbers:
                self.board[symbol1].remove(num)
                self.board[symbol2].remove(num)
                self.board[symbol1].append(num*2)
                self.normalize_position()
                possible_moves.append(self.board)
                self.board = deepcopy(board_copy)

                self.board[symbol1].remove(num)
                self.board[symbol2].remove(num)
                self.board[symbol2].append(num*2)
                self.normalize_position()
                possible_moves.append(self.board)
                self.board = deepcopy(board_copy)

        unique_moves = []

        for move in possible_moves:
            if move not in unique_moves:
                unique_moves.append(move)

        return unique_moves

    def minimax(self, alpha: float = float('-inf'), beta: float = float('inf')) -> int:
        """
        Implement the minimax algorithm to find the optimal move.
        Player 1 is the maximizing player. (starts the game and want final position to have odd number of stacks.)
        Player 2 is the minimizing player. (goes second and want final position to have even number of stacks).

        Returns:
        - The minimax value for the current state of the board.
        - alpha: The current best score that the maximizing player is assured of.
        - beta: The current best score that the minimizing player is assured of.
        """
        Soluna.minimax_counter += 1

        is_player1_turn  = 1 - sum(len(symbol) for symbol in self.board if symbol) % 2
        possible_moves = self.get_moves()
        # Base cases
        if len(possible_moves) == 0:
            return -2*is_player1_turn+1

        board_copy = deepcopy(self.board)
        if is_player1_turn:
            max_eval = float('-inf')
            for move in possible_moves:
                self.board = move
                eval = self.minimax(alpha, beta)
                self.board = deepcopy(board_copy)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                self.board = move
                eval = self.minimax(alpha, beta)
                self.board = deepcopy(board_copy)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval

    def find_best_move(self) -> int:
        """
        Find the best move using the minimax algorithm.
        In case of multiple equally optimal moves, the tiebreaker is [insert weird rules]

        Returns:
        - The index of the best move on the board. (-1 if no possible moves)
        """
        Soluna.minimax_counter = 0
        is_player1_turn  = 1 - sum(len(symbol) for symbol in self.board if symbol) % 2

        best_val = float('-inf') if is_player1_turn else float('inf')
        best_move = -1

        possible_moves = self.get_moves()
        board_copy = deepcopy(self.board)
        if is_player1_turn:
            for move in possible_moves:
                self.board = deepcopy(move)
                move_val = self.minimax()
                self.board = deepcopy(board_copy)

                if move_val > best_val:
                    best_val = move_val
                    best_move = move
        else:
            for move in possible_moves:
                self.board = deepcopy(move)
                move_val = self.minimax()
                self.board = deepcopy(board_copy)

                if move_val < best_val:
                    best_val = move_val
                    best_move = move
        if best_move == -1:
            return best_move, -2*is_player1_turn+1
        return best_move, best_val

example_board = [
    [1, 1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1]
]

# soluna_game = Soluna(example_board)
# soluna_game.display_board()
# soluna_game.get_moves()
# soluna_game.minimax()
# print(soluna_game.find_best_move())
# print(soluna_game.minimax_counter)

STARTING_CONFIGURATIONS = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
[[1, 1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1]],
[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1], [1, 1]],
[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1], [1,]],
[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], []],
[[1, 1, 1, 1, 1], [1, 1, 1], [1, 1], [1, 1]],
[[1, 1, 1, 1, 1], [1, 1, 1], [1, 1, 1], [1,]],
[[1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1], [1,]],
[[1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1], []],
[[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1,], [1,]],
[[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1], []],
[[1, 1, 1, 1, 1, 1], [1, 1], [1, 1], [1, 1]],
[[1, 1, 1, 1, 1, 1], [1, 1, 1], [1, 1], [1,]],
[[1, 1, 1, 1, 1, 1], [1, 1, 1], [1, 1, 1], []],
[[1, 1, 1, 1, 1, 1], [1, 1, 1, 1], [1,], [1,]],
[[1, 1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1], []]]


total_counter = 0
for board in STARTING_CONFIGURATIONS:
    soluna_game = Soluna(board)
    soluna_game.display_board()
    soluna_game.minimax()
    print(soluna_game.find_best_move())
    print(soluna_game.minimax_counter)
    total_counter += soluna_game.minimax_counter
print(total_counter)

import doctest
doctest.testmod()

