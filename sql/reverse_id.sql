-- note id can be set as not the key as state may be the primary key
-- reverse the id column as the database
-- will be created in reverse move order due to Dynamic Programming
SET @max_id = (SELECT MAX(id) FROM soluna);
SET @row_number = 0;

UPDATE soluna
SET id = (@max_id - (@row_number := @row_number + 1)) + 1
ORDER BY id;