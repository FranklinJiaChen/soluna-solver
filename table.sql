CREATE TABLE `soluna` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`move_num` INT(11) NULL DEFAULT NULL COMMENT 'the move number of the state. Starting configurations are move 1',
	`state` VARCHAR(255) NOT NULL COMMENT 'the board state' COLLATE 'utf8mb4_general_ci',
	`best_move` VARCHAR(255) NULL DEFAULT NULL COMMENT 'the state of the best move' COLLATE 'utf8mb4_general_ci',
	`eval` INT(11) NULL DEFAULT NULL COMMENT 'under perfect play, which player will win. 1 = player 1, -1 = player 2',
	`is_determined` TINYINT(1) NULL DEFAULT '0' COMMENT 'is the winning player already determined no matter the moves either player make',
	`p1_optimal_p1_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable in the smallest set of states of player 1 when player 1 is an optimal player and player 1 is guaranteed to win at the start',
	`p1_optimal_p2_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable when player 1 is an optimal player and player 2 is guaranteed to win at the start',
	`p2_optimal_p1_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable when player 2 is an optimal player and player 1 is guaranteed to win at the start',
	`p2_optimal_p2_wins` TINYINT(1) NULL DEFAULT '0' COMMENT 'reachable in the smallest set of states of player 2 when player 2 is an optimal player and player 2 is guaranteed to win at the start',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `state_unique` (`state`) USING BTREE,
	INDEX `best_move` (`best_move`) USING BTREE,
	CONSTRAINT `soluna_ibfk_1` FOREIGN KEY (`best_move`) REFERENCES `soluna` (`state`) ON UPDATE CASCADE ON DELETE SET NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
