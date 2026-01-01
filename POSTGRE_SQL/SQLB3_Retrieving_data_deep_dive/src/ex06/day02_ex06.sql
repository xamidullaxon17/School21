SELECT m.pizza_name AS pizza_name, pz.name AS pizzeria_name
FROM person_order po
JOIN person pr
    ON po.person_id = pr.id
JOIN menu m
    ON po.menu_id = m.id
JOIN pizzeria pz
    ON m.pizzeria_id = pz.id
WHERE pr.name IN ('Denis', 'Anna')
ORDER BY m.pizza_name, pz.name