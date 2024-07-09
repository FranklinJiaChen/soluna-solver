-- Purpose: resets all the fields in the soluna table to their default values.
--          while keeping the ids and the board state.
UPDATE soluna
SET
    move_num = NULL,
    eval = NULL,
    best_move = NULL,
    move_explanation = NULL,
    possible_move_count = NULL,
    total_parents = 0,
    num_winning_moves = NULL,
    num_losing_moves = NULL,
    winning_move_percentage = NULL,
    losing_move_percentage = NULL,
    is_determined = 0,
    reachable = 0,
    p1_optimal_p1_wins = 0,
    p1_optimal_p2_wins = 0,
    p2_optimal_p1_wins = 0,
    p2_optimal_p2_wins = 0;
