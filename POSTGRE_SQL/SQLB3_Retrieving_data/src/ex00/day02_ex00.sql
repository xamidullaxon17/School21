SELECT p.name, p.rating
FROM pizzeria p
LEFT JOIN person_visits pv
	ON p.id = pv.pizzeria_id
WHERE pv.person_id IS NULL