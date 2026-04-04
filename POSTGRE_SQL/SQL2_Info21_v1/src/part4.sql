CREATE TABLE IF NOT EXISTS TableName_users (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS TableName_orders (
    id      SERIAL PRIMARY KEY,
    user_id INTEGER,
    amount  NUMERIC
);

CREATE TABLE IF NOT EXISTS TableName_products (
    id    SERIAL PRIMARY KEY,
    title VARCHAR(100),
    price NUMERIC
);

-- Oddiy jadval
CREATE TABLE IF NOT EXISTS regular_table (
    id SERIAL PRIMARY KEY
);

CREATE OR REPLACE FUNCTION fn_add_numbers(a INTEGER, b INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_get_greeting(username VARCHAR)
RETURNS TEXT AS $$
BEGIN
    RETURN 'Hi, ' || username || '!';
END;
$$ LANGUAGE plpgsql;

-- Parametrsiz funksiya
CREATE OR REPLACE FUNCTION fn_current_time()
RETURNS TIME AS $$
BEGIN
    RETURN NOW()::TIME;
END;
$$ LANGUAGE plpgsql;

-- Test triggerlar uchun table
CREATE TABLE IF NOT EXISTS test_log (
    id         SERIAL PRIMARY KEY,
    action     VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_data (
    id   SERIAL PRIMARY KEY,
    val  INTEGER
);

-- Test trigger 1
CREATE OR REPLACE FUNCTION fn_log_insert_test_data()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO test_log(action) VALUES ('INSERT into test_data');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_test1 ON test_data;
CREATE TRIGGER trg_test1
    AFTER INSERT ON test_data
    FOR EACH ROW
    EXECUTE FUNCTION fn_log_insert_test_data();

-- Test trigger 2
CREATE OR REPLACE FUNCTION fn_log_delete_test_data()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO test_log(action) VALUES ('DELETE from test_data');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_test2 ON test_data;
CREATE TRIGGER trg_test2
    AFTER DELETE ON test_data
    FOR EACH ROW
    EXECUTE FUNCTION fn_log_delete_test_data();

-- 4.1) "TableName" bilan boshlanadigan barcha jadvallarni o'chiradigan protsedura

CREATE OR REPLACE PROCEDURE pr_drop_tables_by_prefix(table_prefix VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_table_name TEXT;
    v_sql        TEXT;
BEGIN
    FOR v_table_name IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE table_prefix || '%'
    LOOP
        v_sql := 'DROP TABLE IF EXISTS ' || quote_ident(v_table_name) || ' CASCADE';
        RAISE NOTICE 'Jadval o''chirilmoqda: %', v_table_name;
        EXECUTE v_sql;
    END LOOP;
END;
$$;

-- Test
CALL pr_drop_tables_by_prefix('TableName');
-- Tekshirish: TableName_* jadvallar yo'q bo'lishi kerak, regular_table qolishi kerak
SELECT tablename FROM pg_tables WHERE schemaname = 'public';


-- 4.2) Barcha skalar SQL-funksiyalarining nomi va parametrlarini qaytaruvchi protsedura
CREATE OR REPLACE PROCEDURE pr_list_scalar_functions(
    INOUT func_count INTEGER DEFAULT 0
)
LANGUAGE plpgsql AS $$
DECLARE
    v_row RECORD;
BEGIN
    func_count := 0;

    FOR v_row IN
        SELECT
            p.proname AS func_name,
            pg_get_function_arguments(p.oid) AS func_args
        FROM pg_proc p
        JOIN pg_namespace n ON n.oid = p.pronamespace
        WHERE n.nspname = 'public'
          AND p.prokind = 'f'                    -- oddiy funksiya
          AND p.prorettype != 0                  -- qaytarish tipi mavjud
          -- Skalar: set-returning emas
          AND NOT p.proretset
          AND p.pronargs > 0
        ORDER BY p.proname
    LOOP
        RAISE NOTICE 'Funksiya: % ( % )', v_row.func_name, v_row.func_args;
        func_count := func_count + 1;
    END LOOP;

    RAISE NOTICE 'Jami skalar funksiyalar soni: %', func_count;
END;
$$;

-- Test
DO $$
DECLARE
    cnt INTEGER;
BEGIN
    CALL pr_list_scalar_functions(cnt);
    RAISE NOTICE 'Qaytarilgan son: %', cnt;
END;
$$;


-- 4.3) Barcha DML triggerlarini o'chiradigan protsedura
CREATE OR REPLACE PROCEDURE pr_drop_all_dml_triggers(
    INOUT dropped_count INTEGER DEFAULT 0
)
LANGUAGE plpgsql AS $$
DECLARE
    v_row RECORD;
    v_sql TEXT;
BEGIN
    dropped_count := 0;

    FOR v_row IN
        SELECT
            t.tgname    AS trigger_name,
            c.relname   AS table_name
        FROM pg_trigger t
        JOIN pg_class c ON c.oid = t.tgrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public'
          AND NOT t.tgisinternal  -- faqat foydalanuvchi triggerlar
    LOOP
        v_sql := 'DROP TRIGGER IF EXISTS ' ||
                 quote_ident(v_row.trigger_name) ||
                 ' ON ' ||
                 quote_ident(v_row.table_name) ||
                 ' CASCADE';
        RAISE NOTICE 'Trigger o''chirilmoqda: % (jadval: %)',
                     v_row.trigger_name, v_row.table_name;
        EXECUTE v_sql;
        dropped_count := dropped_count + 1;
    END LOOP;

    RAISE NOTICE 'Jami o''chirilgan triggerlar soni: %', dropped_count;
END;
$$;

-- Test
DO $$
DECLARE
    cnt INTEGER;
BEGIN
    CALL pr_drop_all_dml_triggers(cnt);
    RAISE NOTICE 'O''chirilgan triggerlar: %', cnt;
END;
$$;


-- 4.4) Berilgan satr mavjud bo'lgan barcha protsedura va
-- funksiyalarning nomini va turini chiqaradigan protsedura
CREATE OR REPLACE PROCEDURE pr_find_objects_with_text(
    search_string VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_row RECORD;
BEGIN
    FOR v_row IN
        SELECT
            p.proname AS obj_name,
            CASE p.prokind
                WHEN 'f' THEN 'FUNCTION'
                WHEN 'p' THEN 'PROCEDURE'
                ELSE 'UNKNOWN'
            END AS obj_type,
            pg_get_functiondef(p.oid) AS obj_def
        FROM pg_proc p
        JOIN pg_namespace n ON n.oid = p.pronamespace
        WHERE n.nspname = 'public'
          AND p.prokind IN ('f', 'p')
          AND pg_get_functiondef(p.oid) ILIKE '%' || search_string || '%'
        ORDER BY p.prokind, p.proname
    LOOP
        RAISE NOTICE 'Tur: % | Nom: %', v_row.obj_type, v_row.obj_name;
    END LOOP;
END;
$$;

-- Test: 'RETURN' so'zini o'z ichiga olgan barcha funksiya/protseduralarni topish
CALL pr_find_objects_with_text('RETURN');

-- Test: 'INSERT' so'zini o'z ichiga olgan ob'ektlarni topish
CALL pr_find_objects_with_text('INSERT');
