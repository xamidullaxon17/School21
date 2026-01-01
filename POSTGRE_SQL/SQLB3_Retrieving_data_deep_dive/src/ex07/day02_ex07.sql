SELECT DISTINCT pz.name AS pizzeria_name
FROM person_order po
JOIN person ps 
	ON ps.id = po.person_id
JOIN menu m 
	ON m.id = po.menu_id
JOIN pizzeria pz 
	ON pz.id = m.pizzeria_id
WHERE ps.name = 'Dmitriy' AND po.order_date = DATE '2022-01-08' AND m.price < 800