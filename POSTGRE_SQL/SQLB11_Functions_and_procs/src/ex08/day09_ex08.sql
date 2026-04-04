CREATE OR REPLACE FUNCTION fnc_fibonacci(pstop integer DEFAULT 10)
RETURNS TABLE(num bigint)
AS $$
DECLARE
    a bigint := 0;
    b bigint := 1;
    c bigint;
BEGIN
    WHILE a < pstop LOOP
        num := a;
        RETURN NEXT;
        c := a + b;
        a := b;
        b := c;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

select * from fnc_fibonacci(100);
select * from fnc_fibonacci();
