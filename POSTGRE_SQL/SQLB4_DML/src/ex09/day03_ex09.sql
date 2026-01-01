INSERT INTO person_visits (id, person_id, pizzeria_id, visit_date)
SELECT
    (SELECT MAX(id) + 1 FROM person_visits),
    p.id,
    (SELECT id FROM pizzeria WHERE name = 'Dominos'),
    DATE '2022-02-24'
FROM person p
WHERE p.name = 'Denis'

UNION ALL

SELECT
    (SELECT MAX(id) + 2 FROM person_visits),
    p.id,
    (SELECT id FROM pizzeria WHERE name = 'Dominos'),
    DATE '2022-02-24'
FROM person p
WHERE p.name = 'Irina';
