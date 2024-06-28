SELECT best_move, COUNT(*) AS move_count
FROM soluna
WHERE (move_num % 2 = 1 AND (p1_optimal_p1_wins = 1 OR p1_optimal_p2_wins))
   OR (move_num % 2 = 0 AND (p2_optimal_p1_wins = 1 OR p2_optimal_p2_wins))
GROUP BY best_move;
