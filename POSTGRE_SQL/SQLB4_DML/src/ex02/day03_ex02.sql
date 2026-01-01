SELECT m.pizza_name AS pizza_name, m.price AS price, p.name AS pizzeria_name
FROM menu m
JOIN pizzeria p
    ON m.pizzeria_id = p.id
WHERE m.id IN (SELECT m.id FROM menu m WHERE m.id NOT IN (SELECT po.menu_id FROM person_order po))
ORDER BY m.pizza_name, m.price;