CREATE TABLE `soluna` (
	`id` INT(11) UNSIGNED NOT NULL,
	`move_num` INT(11) NULL DEFAULT NULL COMMENT 'the move number of the state. Starting configurations are move 1',
	`state` VARCHAR(255) NOT NULL COMMENT 'the board state' COLLATE 'utf8mb4_general_ci',
	`eval` INT(11) NULL DEFAULT NULL COMMENT 'under perfect play, which player will win. 1 = player 1, -1 = player 2',
	`best_move` VARCHAR(255) NULL DEFAULT NULL COMMENT 'the state of the best move' COLLATE 'utf8mb4_general_ci',
	`move_explanation` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`possible_move_count` INT(11) NULL DEFAULT NULL COMMENT 'the amount of possible moves from this position',
	`total_parents` INT(11) NULL DEFAULT '0',
	`num_winning_moves` INT(11) NULL DEFAULT NULL,
	`num_losing_moves` INT(11) NULL DEFAULT NULL,
	`winning_move_percentage` DECIMAL(5,4) NULL DEFAULT NULL,
	`losing_move_percentage` DECIMAL(5,4) NULL DEFAULT NULL,
	`is_determined` TINYINT(1) NULL DEFAULT '0' COMMENT 'is the winning player already determined no matter the moves either player make',
	`reachable` TINYINT(1) NULL DEFAULT '0' COMMENT 'is the state reachable given one player has an optimal strategy',
	`p1_optimal_p1_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable in the smallest set of states of player 1 when player 1 is an optimal player and player 1 is guaranteed to win at the start',
	`p1_optimal_p2_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable when player 1 is an optimal player and player 2 is guaranteed to win at the start',
	`p2_optimal_p1_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable when player 2 is an optimal player and player 1 is guaranteed to win at the start',
	`p2_optimal_p2_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable in the smallest set of states of player 2 when player 2 is an optimal player and player 2 is guaranteed to win at the start',
	PRIMARY KEY (`state`) USING BTREE,
	INDEX `best_move` (`best_move`) USING BTREE,
	CONSTRAINT `soluna_ibfk_1` FOREIGN KEY (`best_move`) REFERENCES `soluna` (`state`) ON UPDATE CASCADE ON DELETE SET NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
