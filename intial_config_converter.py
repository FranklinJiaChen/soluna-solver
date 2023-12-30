"""
One-off script used to convert starting configuration into format that represent the game board of Soluna.
i.e (2, 1) --> ((1, 1), (1))
"""
from typing import Tuple, List

def convert_to_tuples(input_tuple: Tuple[int, ...]) -> Tuple[Tuple[int, ...], ...]:
    """
    Converts the lengths provided in the input tuple into tuples of 1s.

    Parameters:
    - input_tuple (tuple): A tuple containing integers >= 0 representing the lengths of tuples.

    Returns:
    tuple: A tuple of tuples, where each inner tuple consists of 1 repeated according to the corresponding length
           specified in the input tuple.
    """
    result = []

    for length in input_tuple:
        inner_tuple = tuple([1] * length)
        result.append(inner_tuple)

    return tuple(result)

def add_letter_to_tuples(input_tuple: Tuple[Tuple[int, ...], ...]) -> Tuple[str, ...]:
    """
    Adds a letter corresponding to the index of each tuple in the input tuple.

    Parameters:
    - input_tuple (Tuple[Tuple[int, ...], ...]): A tuple containing tuples of integers.

    Returns:
    Tuple[str, ...]: A tuple of strings where each string is formed by concatenating the lengths and letters based on the input tuples.

    Tests:
    >>> input_tuple_test = ((2,), (3, 1), (2, 1), (1, 1, 1, 1))
    >>> add_letter_to_tuples(input_tuple_test)
    ('2A', '3B', '1B', '2C', '1C', '1D', '1D', '1D', '1D')
    >>> input_tuple_test = ((12,), (), (), ())
    >>> add_letter_to_tuples(input_tuple_test)
    ('12A',)
    """
    letters = ['A', 'B', 'C', 'D']
    result: List[str] = [f'{length}{letter}' for lengths, letter in zip(input_tuple, letters) for length in lengths]
    return tuple(result)


# Test cases
test_cases = [
    (3, 3, 3, 3),
    (4, 3, 3, 2),
    (4, 4, 2, 2),
    (4, 4, 3, 1),
    (4, 4, 4, 0),
    (5, 3, 2, 2),
    (5, 3, 3, 1),
    (5, 4, 2, 1),
    (5, 4, 3, 0),
    (5, 5, 1, 1),
    (5, 5, 2, 0),
    (6, 2, 2, 2),
    (6, 3, 2, 1),
    (6, 3, 3, 0),
    (6, 4, 1, 1),
    (6, 4, 2, 0),
    (6, 5, 1, 0),
    (6, 6, 0, 0),
    (7, 2, 2, 1),
    (7, 3, 1, 1),
    (7, 3, 2, 0),
    (7, 4, 1, 0),
    (7, 5, 0, 0),
    (8, 2, 1, 1),
    (8, 2, 2, 0),
    (8, 3, 1, 0),
    (8, 4, 0, 0),
    (9, 1, 1, 1),
    (9, 2, 1, 0),
    (9, 3, 0, 0),
    (10, 1, 1, 0),
    (10, 2, 0, 0),
    (11, 1, 0, 0),
    (12, 0, 0, 0),
]

for test_case in test_cases:
    result = convert_to_tuples(test_case)
    result = add_letter_to_tuples(convert_to_tuples(test_case))
    print(f"{result}")
