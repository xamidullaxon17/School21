INSERT INTO person_order (id, person_id, menu_id, order_date)
SELECT
    (SELECT MAX(id) + 1 FROM person_order),
    p.id,
    m.id,
    DATE '2022-02-24'
FROM person p
JOIN menu m
    ON m.pizza_name = 'sicilian pizza'
WHERE p.name = 'Denis'

UNION ALL

SELECT
    (SELECT MAX(id) + 2 FROM person_order),
    p.id,
    m.id,
    DATE '2022-02-24'
FROM person p
JOIN menu m
    ON m.pizza_name = 'sicilian pizza'
WHERE p.name = 'Irina';
