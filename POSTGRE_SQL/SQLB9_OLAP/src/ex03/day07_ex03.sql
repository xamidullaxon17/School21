WITH visits AS (
    SELECT pz.name, COUNT(*) AS visit_count
    FROM person_visits pv
    JOIN pizzeria pz ON pv.pizzeria_id = pz.id
    GROUP BY pz.name
),
orders AS (
    SELECT pz.name, COUNT(*) AS order_count
    FROM person_order po
    JOIN menu m ON po.menu_id = m.id
    JOIN pizzeria pz ON m.pizzeria_id = pz.id
    GROUP BY pz.name
)

SELECT COALESCE(v.name, o.name) AS name,
    COALESCE(v.visit_count, 0) + COALESCE(o.order_count, 0) AS total_count
FROM visits v
FULL JOIN orders o ON v.name = o.name
ORDER BY total_count DESC, name ASC;
