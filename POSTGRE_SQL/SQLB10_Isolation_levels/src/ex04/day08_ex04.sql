-- Session1
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT * FROM pizzeria WHERE name = 'Pizza Hut';

-- Session2
-- BEGIN;
-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- UPDATE pizzeria SET rating = 3.0 WHERE name = 'Pizza Hut';
-- COMMIT;

-- Session1
SELECT * FROM pizzeria WHERE name = 'Pizza Hut';

COMMIT;
