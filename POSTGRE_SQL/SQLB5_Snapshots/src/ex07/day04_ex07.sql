INSERT INTO person_visits (id, person_id, pizzeria_id, visit_date)
SELECT
    (SELECT COALESCE(MAX(id),0)+1 FROM person_visits) AS new_id,
    p.id,
    pz.id,
    DATE '2022-01-08'
FROM person p
JOIN pizzeria pz ON 1=1
WHERE p.name = 'Dmitriy'
  AND NOT EXISTS (
        SELECT 1
        FROM person_visits pv
        WHERE pv.person_id = p.id
          AND pv.pizzeria_id = pz.id
          AND pv.visit_date = DATE '2022-01-08'
    )
LIMIT 1;

REFRESH MATERIALIZED VIEW mv_dmitriy_visits_and_eats;


SELECT * FROM mv_dmitriy_visits_and_eats