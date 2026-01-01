SELECT m.pizza_name AS pizza_name, m.price AS price, pz.name AS pizzeria_name, pv.visit_date AS visit_date
FROM person p
JOIN person_visits pv
    ON p.id = pv.person_id
JOIN pizzeria pz
   ON pv.pizzeria_id = pz.id
JOIN menu m 
   ON pz.id = m.pizzeria_id 
WHERE p.name = 'Kate' AND m.price BETWEEN 800 AND 1000
ORDER BY pizza_name, price, pizzeria_name

