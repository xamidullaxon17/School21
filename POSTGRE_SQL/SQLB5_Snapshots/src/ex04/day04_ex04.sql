CREATE VIEW v_symmetric_union AS
WITH r_minus_s AS (
    SELECT person_id
    FROM person_visits
    WHERE visit_date = DATE '2022-01-02'
    EXCEPT
    SELECT person_id
    FROM person_visits
    WHERE visit_date = DATE '2022-01-06'
),
s_minus_r AS (
    SELECT person_id
    FROM person_visits
    WHERE visit_date = DATE '2022-01-06'
    EXCEPT
    SELECT person_id
    FROM person_visits
    WHERE visit_date = DATE '2022-01-02'
)
SELECT person_id
FROM r_minus_s
UNION
SELECT person_id
FROM s_minus_r
ORDER BY person_id;

SELECT * FROM v_symmetric_union
