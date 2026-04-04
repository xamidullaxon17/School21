SELECT p.name as name, COUNT(pv.id) AS count_of_visits
FROM person_visits pv
JOIN person p ON pv.person_id = p.id
JOIN pizzeria pz ON pv.pizzeria_id = pz.id
GROUP BY p.name
HAVING COUNT(pv.id) > 3
