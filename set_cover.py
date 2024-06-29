"""
In order to minimize the solution space of
the optimal strategy for Soluna,
we can use the set cover problem to
identify the smallest set of states that
covers all the winning positions for player 2's first move.

This translates to an instance of the
set cover problem, which is NP-complete.

For this problem, we have
- A universe of elements: the winning positions for player 2's first move.
- A collection of sets: A winning position that a subset of
    the universe can make the move to reach.

the universe is size 40
the collection of sets is size 48

We use heuristics to solve this particular instance
of the set cover problem.
"""

import mysql.connector
from soluna import Soluna
from itertools import combinations

SQL_CONFIG = {
    'user': 'root',
    'host': 'localhost',
    'database': 'soluna',
}

INFO = dict[int: list[int]]
"""
A dictionary where the key is the id of the possible
    moves that can be made from player 2's first move.
The value is a list of the parent states of the key.
"""

def connect_to_database() -> None:
    """
    Connects to the MySQL database.
    """
    global conn, cursor
    try:
        conn = mysql.connector.connect(**SQL_CONFIG)
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return


def disconnect_from_database() -> None:
    """
    Disconnects from the MySQL database.
    """
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print('MySQL connection closed')


def get_info_from_database() -> dict[int: list[int]]:
    """
    Returns info from the database of the interested states.

    Returns:
        dict[int: list[int]]: A dictionary
        where the key is the id of the state.
        The value is a list of ids of the states
            that are winning positions for player 2's first move.
    """

    cursor.execute("""
                   SELECT id, state
                   FROM soluna
                   WHERE move_num = 2 AND eval = -1
                   """)
    results = cursor.fetchall()
    states = [result for result in results]

    state_dict = {}
    for id, state in states:

        soluna_game = Soluna(eval(state))
        formatted_moves = soluna_game.get_formatted_moves()

        cursor.execute(f"""
                       SELECT id
                       FROM soluna
                       WHERE state in ({formatted_moves}) AND
                             eval = -1
                       """)
        results = cursor.fetchall()
        winning_ids = [winning_id[0] for winning_id in results]

        state_dict[id] = winning_ids

    return state_dict


def remove_redundant_states(info: INFO) -> INFO:
    """
    Removes redundant states from the dictionary.

    States are redundant if what they cover are a subset
        of what another state covers.

    Parameters:
        states (dict[int: list[int]]): A dictionary
            where the key is the id of possible moves that can be made
            and the value is a list of parent states of the key.

    Returns:
        A subdictionary of states that are not redundant.
    """
    redundant_states = set()
    for key1, key2 in combinations(info.keys(), 2):
        value1_set = set(info[key1])
        value2_set = set(info[key2])

        if value1_set < value2_set:
            redundant_states.add(key1)
        elif value2_set < value1_set:
            redundant_states.add(key2)

    for state in redundant_states:
        del info[state]

def reverse_dict(states: dict[int: list[int]]) -> dict[int: list[int]]:
    """
    Reverses the dictionary to solve the set cover problem.
    """
    reversed_dict = {}
    for key, value in states.items():
        for val in value:
            if val not in reversed_dict:
                reversed_dict[val] = []
            reversed_dict[val].append(key)
    return reversed_dict


def print_dictionary_formatted(states: dict[int: list[int]],
                               name: str) -> None:
    """
    Prints the dictionary in a formatted way.

    Parameters:
        states (dict[int: list[int]]): A dictionary
            where the key is the id of possible moves that can be made
            and the value is a list of parent states of the key.
        name (str): The name of the dictionary.
    """
    print(f"Length of dictionary {name}: {len(states)} \n")
    for key, value in states.items():
        print(f"{key}: {value}")
    print()


def add_to_solution(info: INFO, state: int) -> None:
    """
    Adds a state to the solution.

    Update the info dictionary by removing the state and
        all the states covers
    """
    solution.append(state)
    covered_states = info[state]
    del info[state]
    for key, values in info.items():
        values = [value for value in values if value not in covered_states]
        info[key] = values

    print_dictionary_formatted(info, "info after adding to solution")



def get_must_pick_sets(info: INFO) -> bool:
    """
    Returns the sets that must be picked in the set cover problem.
    """
    reversed_info = reverse_dict(info)
    print_dictionary_formatted(reversed_info, "reversed_info")
    for value in reversed_info.values():
        if len(value) == 1:
            add_to_solution(info, value[0])
            return True
    return False


def simplify_and_solve(info: INFO) -> None:
    """
    Simplifies the problem and solves it.
    """
    remove_redundant_states(info)
    while (get_must_pick_sets(info)):
        remove_redundant_states(info)

    print(solution)
    print_dictionary_formatted(info, "info after simplification")
    print_dictionary_formatted(reverse_dict(info), "reversed info after simplification")

def main():
    connect_to_database()
    reverse_info = get_info_from_database()
    disconnect_from_database()

    info = reverse_dict(reverse_info)

    global solution
    solution = []

    simplify_and_solve(info)

    # 84 or 156
    # 80, 69 and 132 choose 2
    # 131 or 110
    add_to_solution(info, 156)
    add_to_solution(info, 69)
    add_to_solution(info, 80)
    add_to_solution(info, 110)
    simplify_and_solve(info)



if __name__ == '__main__':
    main()