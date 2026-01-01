SELECT pz.name AS pizzeria_name
FROM pizzeria pz
JOIN menu m ON m.pizzeria_id = pz.id
JOIN person_order po ON po.menu_id = m.id
JOIN person pe ON pe.id = po.person_id
GROUP BY pz.name
HAVING 
    COUNT(CASE WHEN pe.gender = 'female' THEN 1 END) > 0
    AND
    COUNT(CASE WHEN pe.gender = 'male' THEN 1 END) = 0

UNION

SELECT pz.name AS pizzeria_name
FROM pizzeria pz
JOIN menu m ON m.pizzeria_id = pz.id
JOIN person_order po ON po.menu_id = m.id
JOIN person pe ON pe.id = po.person_id
GROUP BY pz.name
HAVING 
    COUNT(CASE WHEN pe.gender = 'male' THEN 1 END) > 0
    AND
    COUNT(CASE WHEN pe.gender = 'female' THEN 1 END) = 0

ORDER BY pizzeria_name;

