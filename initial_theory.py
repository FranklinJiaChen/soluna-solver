"""
This script solves how many ways are there to partition 12 into at most 4 parts.
This is equivalent to solving the initial positions of Soluna in theory.
"""

from typing import List, Set, Tuple

def partition(n: int, current_partition: List[int], all_partitions: Set[Tuple[int]]) -> None:
    """
    Recursive function to generate partitions of a number into at most 4 parts.

    Parameters:
    - n (int): The remaining sum to partition.
    - current_partition (List[int]): The current partition being constructed.
    - all_partitions (Set[Tuple[int]]): Set to store unique partitions.

    Returns:
    None: Partitions are added to the all_partitions set.
    """
    if n == 0:
        # Check if the current partition has at most 4 elements
        if len(current_partition) <= 4:
            # Append zeros to make it exactly 4 elements
            current_partition += [0] * (4 - len(current_partition))
            all_partitions.add(tuple(sorted(current_partition, reverse=True)))
        return

    for i in range(1, n + 1):
        partition(n - i, current_partition + [i], all_partitions)

def generate_partitions(n: int) -> Set[Tuple[int]]:
    """
    Generate partitions of a number into at most 4 parts.

    Parameters:
    - n (int): The number to partition.

    Returns:
    Set[Tuple[int]]: Set containing unique partitions.
    """
    all_partitions = set()
    partition(n, [], all_partitions)
    return all_partitions

# Example usage for n = 12
result = generate_partitions(12)

# Sort the set and print the result
for partition_set in sorted(result, reverse=True):
    print(partition_set)
