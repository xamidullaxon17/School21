CREATE VIEW v_generated_dates AS 
SELECT generate_series(DATE '2022-01-01', 
						DATE '2022-01-31', 
						INTERVAL '1 day')::DATE AS generated_date
ORDER BY generated_date;

SELECT * FROM v_generated_dates
