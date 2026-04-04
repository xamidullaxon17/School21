SELECT gs::date AS missing_date
FROM generate_series(DATE '2022-01-01', DATE '2022-01-10', INTERVAL '1 day') AS gs
LEFT JOIN person_visits pv
    ON pv.visit_date = gs::date
    AND (pv.person_id = 1 OR pv.person_id = 2)
WHERE pv.id IS NULL
ORDER BY missing_date;
