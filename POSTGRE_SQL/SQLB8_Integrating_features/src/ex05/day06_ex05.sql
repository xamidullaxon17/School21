COMMENT ON TABLE person_discounts IS 'This table created for saving discounts';
COMMENT ON COLUMN person_discounts.id IS 'Id (Primary Key), always unique';
COMMENT ON COLUMN person_discounts.person_id IS 'person_id - Costumer identificator and Foreign Key for person table';
COMMENT ON COLUMN person_discounts.pizzeria_id IS 'pizzeria_id - pizzeria identificator, Foreign Key for pizzeria table';
COMMENT ON COLUMN person_discounts.discount IS 'Discount - discount percent it has interval numbers from 0 to 100 (ex: 10.5, 22, 30)';
