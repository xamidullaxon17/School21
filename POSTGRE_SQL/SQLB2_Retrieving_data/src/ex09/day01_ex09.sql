SELECT name
FROM pizzeria
WHERE id NOT IN (SELECT pizzeria_id FROM person_visits);

SELECT p.name
FROM pizzeria p
WHERE NOT EXISTS (SELECT 1 FROM person_visits v WHERE v.pizzeria_id = p.id);
