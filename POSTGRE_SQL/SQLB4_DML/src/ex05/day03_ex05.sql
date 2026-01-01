SELECT DISTINCT pz.name AS pizzeria_name
FROM person_visits pv
JOIN person p ON pv.person_id = p.id
JOIN pizzeria pz ON pv.pizzeria_id = pz.id
WHERE p.name = 'Andrey'
  AND pz.id NOT IN (
      SELECT m.pizzeria_id
      FROM person_order po
      JOIN menu m ON po.menu_id = m.id
      JOIN person p2 ON po.person_id = p2.id
      WHERE p2.name = 'Andrey')
ORDER BY pizzeria_name;
