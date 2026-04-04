--Session1
BEGIN;

UPDATE pizzeria SET rating = 4 WHERE id = 1;

--Session2
-- BEGIN;
-- UPDATE pizzeria SET rating = 3.5 WHERE id = 2;

-- Session1:
UPDATE pizzeria SET rating = 5 WHERE id = 2;  -- Session2 blocked session1

-- Session2: Session2 is trying to update blocked Session2
UPDATE pizzeria SET rating = 2.5 WHERE id = 1;

--  Result: deadlock