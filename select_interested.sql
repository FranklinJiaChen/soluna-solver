-- get the number of states to ensure p1's victory given that p1 has a winning strategy from the start
SELECT * FROM soluna WHERE p1_optimal_p1_wins=1 AND move_num % 2 = 0;
-- get the number of states to ensure p2's victory given that p2 has a winning strategy from the start
SELECT * FROM soluna WHERE p2_optimal_p2_wins=2 AND move_num % 2 = 1;
