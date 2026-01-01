SELECT action_date, person.name AS pizza_name
FROM (
	SELECT order_date AS action_date, person_id
	FROM person_order 
	INTERSECT ALL
	SELECT visit_date, person_id
	FROM person_visits
) AS table1
INNER JOIN person
ON table1.person_id = person.id
ORDER BY action_date, pizza_name DESC