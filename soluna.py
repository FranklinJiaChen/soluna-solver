from copy import deepcopy
from itertools import combinations
from typing import List, Tuple, Literal
import json

from utils import nlist_to_ntup, ntup_to_nlist
import mysql.connector

IntBool = Literal[0, 1]
"""
GameState:
A 2D array where the rows denote the symbols
and the columns denote the size of the stacks of that symbol.
i.e. [[4, 1], [2, 2], [2, 1], []].
Represents the following board state:
a 4 stack and 1 stack of symbol A
two 2 stacks of symbol B
a 2 stack and 1 stack of symbol C
and no stack with symbol D

immutatable type Game State Tuple is needed for sets
Uses nlist_to_ntup and ntup_to_nlist to convert between the two types.
"""
GameState = List[List[int]]
GameStateTuple = Tuple[Tuple[int, ...]]
NUM_SYMBOLS = 4
NUM_TILES = 12
STARTING_CONFIGURATIONS: List[GameState] = [
    [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
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
    [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1], []]
]


SQL_CONFIG = {
    'user': 'root',
    'host': 'localhost',
    'database': 'soluna',
}

def get_total_stacks(board: GameState) -> int:
    """
    Get the number of stacks in a board

    Parameters:
    - board: The game state

    Returns:
    - The total number of stacks in the board
    """
    return sum(len(symbol) for symbol in board)


def get_move_num(board: GameState) -> int:
    """
    Get the number of moves in a board

    Parameters:
    - board: The game state

    Returns:
    - The number of moves this current board state will make.
      (i.e. starting states start will return 1)
    """
    return NUM_TILES-get_total_stacks(board) + 1


def is_player1_turn(board: GameState) -> IntBool:
    """
    Determine if it is player 1's turn

    Parameters:
    - board: The game state

    Returns:
    - 1 if it is player 1's turn, 0 otherwise
    """
    return get_move_num(board) % 2


def get_wanted_score(board: GameState) -> int:
    """
    Get the wanted score of the game by the current player

    Parameters:
    - board: The game state

    Returns:
    1 if it is player 1's turn, -1 otherwise
    """
    return 2 * is_player1_turn(board) - 1


class Soluna:
    """
    A class representing the Soluna game.

    Attributes:
    - board (GameState): The current state of the Soluna board.

    Methods:
    - __init__(self, board: GameState):
        Initializes a Soluna game.
        Also validates the provided board
        and normalizes the position.
    - validate_board(self, board: GameState):
        Validates the provided board.
    - normalize_position(self):
        Normalizes the position of the board.
    - display_board(self):
        Displays the current state of the Soluna board.
    - get_moves(self) -> List[GameState]:
        Get all possible moves from a given state.

    Raises:
    - ValueError: If the provided board is invalid.

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
    def __init__(self, board: GameState) -> None:
        """
        Initialize a Soluna game.

        Parameters:
        - board: The Game State

        Raises:
        - ValueError: If the provided board is invalid.
        """
        self.validate_board(board)
        self.board = deepcopy(board)
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
        if len(board) != NUM_SYMBOLS:
            raise ValueError("Invalid board: Board does not have exactly "
                             f"{NUM_SYMBOLS} symbols.")

        if sum(sum(symbol) for symbol in board if symbol) != NUM_TILES:
            raise ValueError("Invalid board: Board does not have exactly "
                             f"{NUM_TILES} tiles.")

        if not all(isinstance(stack, int) and stack >= 1
                   for symbol in board for stack in symbol):
            raise ValueError("Invalid board: Board's stacks "
                             "must be positive integers.")


    def display_board(self) -> None:
        """
        Display the current state of the Soluna board.
        Each stacks is seperated by spaces
            and consists of a number and letter.
        The number is the size of the stack
            and the letter is the the top stack's symbol
        """
        labels = iter("ABCD")
        for symbol in self.board:
            label = next(labels)
            if symbol:
                print(" ".join(f"{stack}{label}" for stack in symbol))


    def normalize_position(self) -> None:
        """
        Transform self.board represented by a 2d array
        into a normalized equivalent 2d array.
        1. Each symbols stack sizes are given in a nonincreasing order.
        2. The number of stacks the symbols have
           must be in a nonincreasing order.
        3. Two symbols with the same amount of stacks
           must be in reverse lexicographical ordering
        ex. ((1, 1, 1), (3, 1), (2, 2), (1,))
        """
        for i in range(NUM_SYMBOLS):
            self.board[i] = sorted(self.board[i], reverse=True)

        self.board = sorted(self.board,
                            key=lambda symbol: (len(symbol), symbol),
                            reverse=True)


    def get_moves(self) -> List[GameState]:
        """
        Get all possible moves from a given state.
        """
        possible_moves: List[GameState] = []
        board_copy: GameState = deepcopy(self.board)

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
        combinations_2 = list(combinations(range(NUM_SYMBOLS), 2))
        for (symbol1, symbol2) in combinations_2:
            matching_nums = (set(self.board[symbol1])
                             & set(self.board[symbol2]))
            for num in matching_nums:
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


    def get_formatted_moves(self) -> str:
        """
        Get all possible moves from a given state
        in a formatted string for SQL queries.
        """
        # if no moves, return empty string for SQL query
        if not self.get_moves():
            return '""'
        return ', '.join([f'"{move}"' for move in self.get_moves()])


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


def get_all_positions() -> List[GameState]:
    """
    Use breadth-first search to find all possible game states by move.
    """
    possible_positions_by_move: list[set[GameStateTuple]] = []
    # move 1 possible positions
    possible_positions_by_move.append(set(nlist_to_ntup(config)
                                      for config in STARTING_CONFIGURATIONS))

    # move 2-12 possible positions
    for positions_by_move in possible_positions_by_move:
        new_positions = set()
        for position in positions_by_move:
            soluna_game = Soluna(ntup_to_nlist(position))
            new_positions.update(nlist_to_ntup(soluna_game.get_moves()))
        if len(new_positions) != 0:
            possible_positions_by_move.append(new_positions)

    # convert list of set into flattened list
    return [ntup_to_nlist(position)
            for positions in possible_positions_by_move
            for position in positions]


def evaluate_board(board: GameState) -> int:
    """
    Evaluate a game board using memoization,
    retrieves and stores results in a database.

    Parameters:
    - board: The game state

    Returns the evaluation score for the given board.
    """
    soluna_game = Soluna(board)

    cursor.execute(f'''
                    SELECT eval FROM soluna
                    WHERE state = "{soluna_game.board}"
                    ''')
    board_data = cursor.fetchone()

    if board_data[0]: return board_data[0]

    possible_moves = soluna_game.get_moves()
    wanted_score = get_wanted_score(board)

    eval = -wanted_score
    if any(evaluate_board(move) == wanted_score for move in possible_moves):
        eval = wanted_score

    if board_data:
        cursor.execute(f'''
                        UPDATE soluna SET eval = {eval}
                        WHERE state = "{soluna_game.board}"
                        ''')
    else:
        cursor.execute(f'''
                        INSERT INTO soluna (state, eval)
                        VALUES ("{soluna_game.board}", {eval})
                        ''')

    conn.commit()
    return eval


def update_board_is_determined(board: GameState) -> None:
    """
    Update the is_determined column in the database

    Preconditions:
    - board is a valid game state
    - every possible move from the board
      has been evaluated and stored in the database
    - every move after this board is_determined has been updated
    """
    soluna_game = Soluna(board)
    cursor.execute(f'''
                    SELECT eval FROM soluna
                    WHERE state = "{soluna_game.board}"
                    ''')
    board_data = cursor.fetchone()

    if board_data:
        all_determined = True
        determined_result = board_data[0]
        possible_moves = soluna_game.get_moves()

        for move in possible_moves:
            cursor.execute(f'''
                             SELECT eval, is_determined FROM soluna
                             WHERE state = "{move}"
                            ''')
            move_data = cursor.fetchone()
            if move_data[1] == 0:
                all_determined = False
                break
            if move_data[0] != determined_result:
                all_determined = False
                break

        if all_determined:
            cursor.execute(f'''
                            UPDATE soluna
                            SET is_determined = 1
                            WHERE state = "{soluna_game.board}"
                            ''')
            conn.commit()


def update_eval() -> None:
    """
    Solve the game using memoization

    Where
    first player victory = 1
    second player victory = -1
    """
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions[::-1]):
        print(f"Updating eval, position {index+1}/{len(all_positions)}")
        evaluate_board(position)


def update_is_determined() -> None:
    """
    Update the is_determined column in the database.

    Where
    is_determined = 1 if the result of the game is known
    is_determined = 0 if the result of the game is unknown

    Preconditions:
    - every possible move from the board
      has been evaluated and stored in the database
    - every move after this board is_determined has been updated
    """
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions[::-1]):
        print("Updating is_determined, position "
              f"{index+1}/{len(all_positions)}")
        soluna_game = Soluna(position)

        all_determined = True
        determined_result = evaluate_board(position)

        cursor.execute(f'''
                        SELECT eval, is_determined FROM soluna
                        WHERE state IN ({soluna_game.get_formatted_moves()})
                        ''')
        results = cursor.fetchall()

        if any(result[0] != determined_result or result[1] == 0
               for result in results):
            all_determined = False

        if all_determined:
            cursor.execute(f'''
                            UPDATE soluna SET is_determined = 1
                            WHERE state = "{soluna_game.board}"
                            ''')
            conn.commit()


def update_move_info() -> None:
    """
    Update the move_num, possible_move_count,
               num_winning_moves, num_losing_moves,
               winning_move_percentage, losing_move_percentage
    columns in the database.

    Where
    move_num = the number of moves the board will make
    possible_move_count = the number of possible moves from the board
    num_winning_moves = the number of winning moves from the board
    num_losing_moves = the number of losing moves from the board
    winning_move_percentage = num_winning_moves/possible_move_count
                              rounded to 4 decimal places
    losing_move_percentage = num_losing_moves/possible_move_count
                              rounded to 4 decimal places

    Preconditions:
    - every possible move from the board
      has been evaluated and stored in the database
    """
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions):
        print(f"Updating move info, position {index+1}/{len(all_positions)}")
        soluna_game = Soluna(position)
        possible_moves = soluna_game.get_moves()
        wanted_score = get_wanted_score(soluna_game.board)
        num_win = len([move for move in possible_moves
                                 if evaluate_board(move) == wanted_score])
        num_lose = len([move for move in possible_moves
                                if evaluate_board(move) == -wanted_score])
        if len(possible_moves):
            win_percentage = round(num_win/len(possible_moves), 4)
            lose_percentage = round(num_lose/len(possible_moves), 4)
        else: # if no moves, set percentage to the game outcome
            win_percentage = evaluate_board(soluna_game.board) == wanted_score
            lose_percentage = 1 - win_percentage
        cursor.execute(f'''
                        UPDATE soluna
                        SET move_num = {get_move_num(soluna_game.board)},
                            possible_move_count = {len(possible_moves)},
                            num_winning_moves = {num_win},
                            num_losing_moves = {num_lose},
                            winning_move_percentage = {win_percentage},
                            losing_move_percentage = {lose_percentage}
                        WHERE state = "{soluna_game.board}"
                        ''')
        conn.commit()


def update_reachable_column(possible_positions_by_move: set[GameStateTuple],
                            optimal_player: int, column: str) -> None:
    """
    Update a reachable column in the database

    Parameters:
    - possible_positions_by_move:
        The possible positions by move.
        Initially contains the starting positions.
    - optimal_player:
        1 or 2 respectively for player 1 or 2
    - column:
        The column to update
        p1_optimal_p1_wins,
        p1_optimal_p2_wins,
        p2_optimal_p1_wins,
        p2_optimal_p2_wins

        where optimal means the player plays optimally
        and wins means the evaluation of the starting position is for
        that player to win

    Where
    column = 1 if the position is reachable from the starting position

    Preconditions:
    - every possible move from the board
      has been evaluated and stored in the database
    """
    # move 2-12 possible positions
    is_optimal_player_turn = optimal_player == 1
    for possible_positions in possible_positions_by_move:
        new_possible_positions = set()
        if is_optimal_player_turn:
            for position in possible_positions:
                cursor.execute(f'''
                                SELECT state, best_move
                                FROM soluna
                                WHERE state ="{ntup_to_nlist(position)}"
                                ''')
                result = cursor.fetchone()
                if result[1]:
                    best_move_list = json.loads(result[1])
                    new_possible_positions.add(nlist_to_ntup(best_move_list))
                    cursor.execute(f'''
                                    UPDATE soluna SET {column} = 1
                                    WHERE state = "{best_move_list}"
                                    ''')
        else:
            for position in possible_positions:
                soluna_game = Soluna(ntup_to_nlist(position))
                for move in soluna_game.get_moves():
                    new_possible_positions.add(nlist_to_ntup(move))
                    cursor.execute(f'''
                                    UPDATE soluna SET {column} = 1
                                    WHERE state = '{move}'
                                    ''')

        if len(new_possible_positions) != 0:
            possible_positions_by_move.append(new_possible_positions)
        is_optimal_player_turn = not is_optimal_player_turn
    conn.commit()


def update_reachable() -> None:
    """
    Update the reachable columns in the database.
    """
    p1_win_positions: list[set[GameStateTuple]] = [set()]
    p2_win_positions: list[set[GameStateTuple]] = [set()]
    for config in STARTING_CONFIGURATIONS:
        if evaluate_board(config) == 1:
            p1_win_positions[0].add(nlist_to_ntup(config))
            cursor.execute(f'''
                            UPDATE soluna
                            SET p1_optimal_p1_wins = 1,
                                p2_optimal_p1_wins = 1
                            WHERE state = "{config}"
                            ''')
        else:
            p2_win_positions[0].add(nlist_to_ntup(config))
            cursor.execute(f'''
                            UPDATE soluna
                            SET p1_optimal_p2_wins = 1,
                                p2_optimal_p2_wins = 1
                            WHERE state = "{config}"
                            ''')
    conn.commit()

    update_reachable_column(deepcopy(p1_win_positions),
                            1, "p1_optimal_p1_wins")
    update_reachable_column(deepcopy(p2_win_positions),
                            1, "p1_optimal_p2_wins")
    update_reachable_column(p1_win_positions, 2, "p2_optimal_p1_wins")
    update_reachable_column(p2_win_positions, 2, "p2_optimal_p2_wins")


def shadow_best_moves(explanation: str) -> bool:
    """
    Update the best_move and move_explanation column in the database.
    by choosing a already chosen reachable move when given a choice
    between multiple winning moves.

    Where
    move_explanation =
        "confirmed shadow" if the shadowed move
            is made with no assumption
        "probabilistic shadow" if the shadowed move is made with
            the assumption that the opponent plays randomly next turn
            and perfect play after that

    Returns:
    - True if any best move was shadowed, False otherwise
    """
    updated = False
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions):
        print(f"Updating best_move by shadowing, {explanation} "
              f"position {index+1}/{len(all_positions)}")
        # only update if move_explanation is not already set
        cursor.execute(f'''
                        SELECT best_move FROM soluna
                        WHERE state = "{position}"
                        ''')
        move_explanation = cursor.fetchone()[0]
        if move_explanation:
            continue

        soluna_game = Soluna(position)
        possible_moves = soluna_game.get_moves()

        wanted_score = get_wanted_score(soluna_game.board)
        winning_moves = [move for move in possible_moves
                         if evaluate_board(move) == wanted_score]
        if len(winning_moves) > 1:
            formatted_moves = ', '.join([f'"{move}"'
                                         for move in winning_moves])
            player = 1 if is_player1_turn(soluna_game.board) else 2
            cursor.execute(f'''
                            SELECT state FROM soluna
                            WHERE state IN ({formatted_moves})
                                        AND (p{player}_optimal_p1_wins = 1 OR
                                             p{player}_optimal_p2_wins = 1)
                            ''')

            results = cursor.fetchall()

            if results:
                best_move = results[0][0]
                cursor.execute(f'''
                                UPDATE soluna
                                SET best_move = "{best_move}",
                                    move_explanation = "{explanation}"
                                WHERE state = "{soluna_game.board}"
                                ''')
                conn.commit()
                updated = True
    return updated


def update_simple_best_move() -> None:
    """
    Update the best_move and move_explanation column in the database.

    Where
    best_move = the board state of the best move
    move_explanation = the explanation of the best move
        "any" if the result of the game is known
        "only winning move" if there is only one winning move
        "only move not determined losing"
            if there is only one move that is not determined losing

    Preconditions:
    - every possible move from the board
      has been evaluated and stored in the database
    - every move after this board is_dertermined has been updated
    """
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions):
        print(f"Updating best_move, position {index+1}/{len(all_positions)}")
        soluna_game = Soluna(position)
        cursor.execute(f'''
                        SELECT is_determined
                        FROM soluna
                        WHERE state = "{soluna_game.board}"
                        ''')
        is_determined = cursor.fetchone()[0]

        if is_determined:
            cursor.execute(f'''
                            UPDATE soluna
                            SET move_explanation = "any"
                            WHERE state = "{soluna_game.board}"
                            ''')
            continue

        possible_moves = soluna_game.get_moves()
        wanted_score = get_wanted_score(soluna_game.board)

        winning_moves = [move for move in possible_moves
                         if evaluate_board(move) == wanted_score]
        if len(winning_moves) == 1:
            cursor.execute(f'''
                            UPDATE soluna
                            SET best_move = "{winning_moves[0]}",
                                move_explanation = "only winning move"
                            WHERE state = "{soluna_game.board}"
                            ''')

        if len(winning_moves) == 0:
            formatted_moves = ', '.join([f'"{move}"'
                                         for move in possible_moves])
            cursor.execute(f'''
                            SELECT state, is_determined
                            FROM soluna
                            WHERE state IN ({formatted_moves})
                            ''')
            results = cursor.fetchall()

            non_determined_positions = [move[0]
                                        for move in results if move[1] == 0]
            if len(non_determined_positions) == 1:
                cursor.execute(f'''
                                UPDATE soluna
                                SET best_move =
                                        "{non_determined_positions[0]}",
                                    move_explanation =
                                        "only move not determined losing"
                                    WHERE state = "{soluna_game.board}"
                                ''')
    conn.commit()

def shadow_best_move_loop(explanation) -> None:
    """
    Loop shadow_best_moves until no best move can be shadowed
    """
    update_reachable()
    count = 1
    while shadow_best_moves(explanation):
        print(f"iteration {count}")
        update_reachable()
        count += 1


def update_best_losing_move() -> None:
    """
    Update the best_move and move_explanation column in the database.
    For when the board is a losing position.

    Where
    best_move = the board state of the best move
    move_explanation = "highest winning percentage if opponent
                        plays randomly next turn
                        and perfect play after that"
    """
    EXPLANATION = "highest winning percentage if opponent plays randomly "\
                  "next turn and perfect play after that"
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions):
        print("Updating best_move for losing position, position "
              f"{index+1}/{len(all_positions)}")
        # only update if move_explanation is not already set
        cursor.execute(f'''
                        SELECT move_explanation FROM soluna
                        WHERE state = "{position}"
                        ''')
        move_explanation = cursor.fetchone()[0]
        if move_explanation:
            continue

        soluna_game = Soluna(position)
        possible_moves = soluna_game.get_moves()
        wanted_score = get_wanted_score(soluna_game.board)
        losing_moves = [move for move in possible_moves
                        if evaluate_board(move) == -wanted_score]
        if len(losing_moves) == len(possible_moves):
            # the move is the one with the
            # max losing move percentage as best move
            # (losing since the board is opponent's turn/perspective)
            formatted_moves = soluna_game.get_formatted_moves()
            cursor.execute(f'''
                            SELECT state, losing_move_percentage
                            FROM soluna WHERE state IN ({formatted_moves})
                            ''')
            results = cursor.fetchall()
            best_move = max(results, key=lambda x: x[1])[0]
            cursor.execute(f'''
                            UPDATE soluna
                            SET best_move = "{best_move}",
                                move_explanation = "{EXPLANATION}"
                            WHERE state = "{soluna_game.board}"
                            ''')
            conn.commit()


def update_total_parents() -> None:
    """
    Update the total_parents column in the database.

    Where
    total_parents = the total number of positions
                    that can reach the current position
    """
    all_positions = get_all_positions()

    # exit if total_parents is already updated
    cursor.execute(f'''
                    SELECT total_parents FROM soluna
                    WHERE total_parents > 0
                    ''')
    if cursor.fetchone(): return

    for index, position in enumerate(all_positions):
        print("Updating total_parents, position "
              f"{index+1}/{len(all_positions)}")
        soluna_game = Soluna(position)
        possible_moves = soluna_game.get_moves()

        # add one to total parents to each possible move
        for move in possible_moves:
            cursor.execute(f'''
                            SELECT total_parents FROM soluna
                            WHERE state = "{move}"
                            ''')
            total_parents = cursor.fetchone()[0]
            cursor.execute(f'''
                            UPDATE soluna
                            SET total_parents = {total_parents+1}
                            WHERE state = "{move}"
                            ''')
            conn.commit()


def update_best_move_choice() -> None:
    """
    Update the best_move and move_explanation column in the database.
    when forced to choose amongst multiple winning moves,
    choose the one with the most parent states
    (in hopes that this will lower the solution space)

    Where
    best_move = the board state of the best move
    move_explanation = "choice amongst multiple winning moves"
    """
    EXPLANATION = "choice amongst multiple winning moves"
    all_positions = get_all_positions()

    for index, position in enumerate(all_positions):
        print("Updating best_move by choice, position "
              f"{index+1}/{len(all_positions)}")
        # only update if move_explanation is not already set
        cursor.execute(f'''
                        SELECT move_explanation
                        FROM soluna
                        WHERE state = "{position}"
                        ''')
        move_explanation = cursor.fetchone()[0]
        if move_explanation:
            continue

        soluna_game = Soluna(position)
        possible_moves = soluna_game.get_moves()
        wanted_score = get_wanted_score(soluna_game.board)
        winning_moves = [move for move in possible_moves
                        if evaluate_board(move) == wanted_score]

        if len(winning_moves) > 1:
            good_ids = [64, 70, 112, 114, 158, 156, 80, 161, 110, 103, 69]
            formatted_moves = ', '.join([f'"{move}"'
                                         for move in possible_moves])

            cursor.execute(f'''
                            SELECT state, total_parents, id
                            FROM soluna
                            WHERE state IN ({formatted_moves})
                            ''')
            results = cursor.fetchall()

            explanation = EXPLANATION
            for result in results:
                if result[2] in good_ids:
                    print(result[2])
                    best_move = result[0]
                    explanation = "good id"
                    break
            if explanation == EXPLANATION:
                best_move = max(results, key=lambda x: x[1])[0]
            cursor.execute(f'''
                            UPDATE soluna
                            SET best_move = "{best_move}",
                                move_explanation = "{explanation}"
                            WHERE state = "{soluna_game.board}"
                            ''')
            conn.commit()


def populate_table() -> None:
    """
    Populate the table with all possible game states
    """
    update_eval()
    update_is_determined()
    update_move_info()
    update_total_parents()
    update_best_move()
    update_reachable()


def update_best_move() -> None:
    """
    Update the best_move and move_explanation column in the database.
    """
    update_simple_best_move()
    shadow_best_move_loop("confirmed shadow")
    update_best_losing_move()
    shadow_best_move_loop("probabilistic shadow")
    update_best_move_choice()


def main() -> None:
    """
    Main function
    """
    connect_to_database()
    # populate_table()
    update_best_move()
    update_reachable()
    disconnect_from_database()

if __name__ == '__main__':
    main()
