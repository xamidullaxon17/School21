--Session1
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT SUM(rating) AS total_rating FROM pizzeria;

--Session2
-- BEGIN;
-- SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- INSERT INTO pizzeria (id, name, rating) VALUES (10, 'Kazan Pizza', 5);
-- COMMIT;

--Session1
SELECT SUM(rating) AS total_rating FROM pizzeria;

COMMIT;
