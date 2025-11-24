SELECT po.order_date AS order_date, p.name || ' (age:' || p.age || ')' AS person_information
FROM person_order po
NATURAL JOIN (
	SELECT p.id AS person_id, name, age
	FROM person p
) AS p
ORDER BY order_date, person_information;