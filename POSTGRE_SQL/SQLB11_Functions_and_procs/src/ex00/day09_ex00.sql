CREATE TABLE person_audit (
    created     timestamptz NOT NULL DEFAULT current_timestamp,
    type_event  char(1) NOT NULL DEFAULT 'I',
    row_id      bigint NOT NULL,
    name        varchar,
    age         integer,
    gender      varchar,
    address     varchar,
    CONSTRAINT ch_type_event CHECK (type_event IN ('I','U','D'))
);

CREATE OR REPLACE FUNCTION fnc_trg_person_insert_audit()
RETURNS trigger AS $$
BEGIN
    INSERT INTO person_audit(row_id, name, age, gender, address, type_event)
    VALUES (NEW.id, NEW.name, NEW.age, NEW.gender, NEW.address, 'I');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_person_insert_audit
AFTER INSERT ON person
FOR EACH ROW
EXECUTE FUNCTION fnc_trg_person_insert_audit();

INSERT INTO person(id, name, age, gender, address)
VALUES (10,'Damir', 22, 'male', 'Irkutsk');

SELECT * FROM person_audit;
