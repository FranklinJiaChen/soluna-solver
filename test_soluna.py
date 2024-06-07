import unittest
from Soluna import Soluna
from io import StringIO
import sys

class TestInitialization(unittest.TestCase):
    """
    tests initialization and by extension, validation and normalization.
    """
    def test_valid_board(self) -> None:
        """
        Test initialization with a valid board
        """
        board = [[4, 1], [2, 2], [2, 1], []]
        soluna = Soluna(board)
        self.assertEqual(soluna.board, board)

    def test_invalid_board_symbols(self) -> None:
        """
        Test initialization with an invalid board (wrong number of symbols)
        """
        board = [[4, 1], [2, 2], [2, 1], [], []]
        with self.assertRaises(ValueError):
            Soluna(board)

    def test_invalid_board_tiles(self) -> None:
        """
        Test initialization with an invalid board (wrong number of tiles)
        """
        board = [[4, 1], [2, 2], [2, 1], [1, 1, 1]]
        with self.assertRaises(ValueError):
            Soluna(board)

    def test_invalid_board_heights(self) -> None:
        """
        Test initialization with an invalid board (negative stack sizes)
        """
        board = [[4, 1], [2, 2], [2, 1], [1, -1]]
        with self.assertRaises(ValueError):
            Soluna(board)

    def test_normalized_position(self) -> None:
        """
        Test normalization of board position
        """
        board = [[1,], [3, 1], [2, 2], [1, 1, 1]]
        expected_board = [[1, 1, 1], [3, 1], [2, 2], [1,]]
        soluna = Soluna(board)
        self.assertEqual(soluna.board, expected_board)

class TestDisplayBoard(unittest.TestCase):
    def test_display_board(self):
        """
        Test display board
        """
        board = [[4, 1], [2, 2], [2], [1]]
        expected_output = "4A 1A\n2B 2B\n2C\n1D\n"
        captured_output = StringIO()
        sys.stdout = captured_output
        soluna = Soluna(board)
        soluna.display_board()
        sys.stdout = sys.__stdout__
        printed_output = captured_output.getvalue()
        self.assertEqual(printed_output, expected_output)

class TestGetMoves(unittest.TestCase):
    def test_get_moves(self):
        board = [[3, 2, 1], [2, 1], [2], [1]]
        expected_moves = [
            # same symbol
            [[5, 1], [2, 1], [2], [1]],
            [[4, 2], [2, 1], [2], [1]],
            [[3, 3], [2, 1], [2], [1]],
            [[3, 2, 1], [3], [2], [1]],

            # first symbol untouched
            [[3, 2, 1], [4, 1], [1], []],
            [[3, 2, 1], [4], [1], [1]],
            [[3, 2, 1], [2], [2], [2]],
            [[3, 2, 1], [2, 2], [2], []],

            # add to first symbol
            [[4, 3, 1], [2], [1], [1]],
            [[4, 3, 1], [2, 1], [1], []],
            [[3, 2, 2], [2], [2], [1]],
            [[3, 2, 2], [2, 1], [2], []],

            # subtract to first symbol
            [[4, 1], [3, 1], [2], [1]],
            [[3, 1], [2, 1], [4], [1]],
            [[3, 2], [2, 2], [2], [1]],
            [[3, 2], [2, 1], [2], [2]]
        ]

        self.assertCountEqual(Soluna(board).get_moves(), expected_moves)



if __name__ == '__main__':
    unittest.main()

