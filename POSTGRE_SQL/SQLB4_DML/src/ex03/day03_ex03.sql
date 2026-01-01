(
SELECT pz.name AS pizzeria_name
FROM person_visits pv
JOIN pizzeria pz
    ON pv.pizzeria_id = pz.id 
JOIN person p
    ON pv.person_id = p.id
WHERE gender = 'female'
EXCEPT ALL
SELECT pz.name AS pizzeria_name
FROM person_visits pv
JOIN pizzeria pz
    ON pv.pizzeria_id = pz.id 
JOIN person p
    ON pv.person_id = p.id
WHERE gender = 'male'
)
UNION ALL
(
SELECT pz.name AS pizzeria_name
FROM person_visits pv
JOIN pizzeria pz
    ON pv.pizzeria_id = pz.id
JOIN person p
    ON pv.person_id = p.id
WHERE gender = 'male'
EXCEPT ALL
SELECT pz.name AS pizzeria_name
FROM person_visits pv
JOIN pizzeria pz
    ON pv.pizzeria_id = pz.id
JOIN person p
    ON pv.person_id = p.id
WHERE gender = 'female'
)
ORDER BY pizzeria_name

