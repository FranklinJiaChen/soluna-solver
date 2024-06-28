-- resets columns of table
UPDATE soluna
SET best_move = NULL, move_explanation = NULL, reachable = 0, p1_optimal_p1_wins = 0, p1_optimal_p2_wins = 0, p2_optimal_p1_wins = 0, p2_optimal_p2_wins = 0;