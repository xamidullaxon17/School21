SELECT m.pizza_name AS pizza_name, p.name AS pizzeria_name, m.price AS price 
FROM menu m
JOIN pizzeria p
	ON p.id = m.pizzeria_id
WHERE m.pizza_name = 'mushroom pizza'
   OR m.pizza_name = 'pepperoni pizza'
ORDER BY m.pizza_name, p.name
