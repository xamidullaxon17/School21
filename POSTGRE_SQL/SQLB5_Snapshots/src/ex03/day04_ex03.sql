CREATE VIEW v_missing_visit_days AS
SELECT
    gd.generated_date AS missing_date
FROM v_generated_dates gd
LEFT JOIN person_visits pv
    ON gd.generated_date = pv.visit_date
WHERE pv.visit_date IS NULL
ORDER BY missing_date;

SELECT * FROM v_missing_visit_days