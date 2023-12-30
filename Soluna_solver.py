from typing import Tuple

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
    GameState = Tuple[Tuple[int, ...], ...]
    NUM_SYMBOLS = 4
    NUM_TILES = 12

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

    def display_board(self):
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

    def normalize_position(self):
        """
        Transform the board represented by a 2d array into a normalized equivalent 2d array.
        1. Each symbols stack sizes are given in a nonincreasing order.
        2. The number of stacks the symbols have must be in a nonincreasing order.
        3. Two symbols with the same amount of stacks must be in reverse lexicographical ordering
        """
        for i in range(Soluna.NUM_SYMBOLS):
            self.board[i] = sorted(self.board[i], reverse=True)

        self.board = sorted(self.board, key=lambda symbol: (len(symbol), symbol), reverse=True)

example_board = [
    [2,],
    [1, 1, 3],
    [1, 1, 2, 1],
    []
]

soluna_game = Soluna(example_board)
soluna_game.display_board()

import doctest
doctest.testmod()

