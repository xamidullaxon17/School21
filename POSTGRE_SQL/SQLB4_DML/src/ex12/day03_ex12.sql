INSERT INTO person_order (id, person_id, menu_id, order_date)
SELECT
    (SELECT COALESCE(MAX(id),0) FROM person_order) + gs.n AS id,
    p.id AS person_id,
    m.id AS menu_id,
    DATE '2022-02-25' AS order_date
FROM menu m
JOIN generate_series(1, (SELECT COUNT(*) FROM person)) AS gs(n) ON TRUE
JOIN person p ON p.id = gs.n
WHERE m.pizza_name = 'greek pizza';
