WITH date_range AS (
    SELECT generate_series(DATE '2022-01-01', DATE '2022-01-10', INTERVAL '1 day')::date AS day
)
SELECT dr.day AS missing_date
FROM date_range dr
LEFT JOIN person_visits pv
    ON pv.visit_date = dr.day
   AND (pv.person_id = 1 OR pv.person_id = 2)
WHERE pv.id IS NULL
ORDER BY missing_date;

