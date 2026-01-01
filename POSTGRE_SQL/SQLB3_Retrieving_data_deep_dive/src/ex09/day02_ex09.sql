SELECT pr.name AS name
FROM person pr
WHERE pr.gender = 'female'
AND pr.id IN (
      SELECT po.person_id
      FROM person_order po
      JOIN menu m ON po.menu_id = m.id
      WHERE m.pizza_name = 'pepperoni pizza')
AND pr.id IN (
      SELECT po.person_id
      FROM person_order po
      JOIN menu m ON po.menu_id = m.id
      WHERE m.pizza_name = 'cheese pizza')
ORDER BY pr.name
