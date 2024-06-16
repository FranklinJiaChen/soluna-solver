-- note id can be set as not the key as state may be the primary key
SET @max_id = (SELECT MAX(id) FROM soluna);
SET @row_number = 0;

UPDATE soluna
SET id = (@max_id - (@row_number := @row_number + 1)) + 1
ORDER BY id;