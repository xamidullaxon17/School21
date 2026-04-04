SELECT COALESCE(person.name, '-') AS person_name, visit_date, COALESCE(pizzeria.name, '-') AS pizzeria_name
FROM (
    SELECT *
    FROM person_visits
    WHERE visit_date BETWEEN DATE '2022-01-01' AND DATE '2022-01-03'
) pv
FULL JOIN person ON person.id = pv.person_id
FULL JOIN pizzeria ON pizzeria.id = pv.pizzeria_id
ORDER BY person_name, visit_date, pizzeria_name;
