--Session1
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT SUM(rating) AS total_rating FROM pizzeria;

--Session2
-- BEGIN;
-- SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- INSERT INTO pizzeria (id, name, rating) VALUES (11, 'Kazan Pizza 2', 4);
-- COMMIT;

--Session1
SELECT SUM(rating) AS total_rating FROM pizzeria;

COMMIT;
