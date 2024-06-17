-- SELECT * FROM soluna WHERE p1_optimal_p1_wins=1 AND move_num % 2 = 0;
SELECT * FROM soluna WHERE p2_optimal_p2_wins=1 AND move_num % 2 = 1 AND move_num != 1;
