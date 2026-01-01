SELECT pr.name AS name
FROM person pr
JOIN person_order po
    ON pr.id = po.person_id
JOIN menu m 
    ON po.menu_id = m.id
WHERE pr.gender = 'male' AND pr.address IN ('Moscow', 'Samara') AND m.pizza_name IN ('pepperoni pizza', 'mushroom pizza')
ORDER BY pr.name DESC;

