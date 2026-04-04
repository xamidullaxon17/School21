SELECT p.address AS address, pz.name AS name, COUNT(po.id) AS count_of_orders
FROM person_order po
JOIN person p ON po.person_id = p.id
JOIN menu m ON po.menu_id = m.id
JOIN pizzeria pz ON m.pizzeria_id = pz.id
GROUP BY p.address, pz.name 
ORDER BY p.address, pz.name