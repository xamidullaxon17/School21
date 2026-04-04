\c info21;

-- Sequence larni CSV import dan keyin to'g'irlash
SELECT setval('checks_id_seq', (SELECT MAX(ID) FROM Checks));
SELECT setval('p2p_id_seq', (SELECT MAX(ID) FROM P2P));
SELECT setval('verter_id_seq', (SELECT MAX(ID) FROM Verter));
SELECT setval('transferredpoints_id_seq', (SELECT MAX(ID) FROM TransferredPoints));
SELECT setval('friends_id_seq', (SELECT MAX(ID) FROM Friends));
SELECT setval('recommendations_id_seq', (SELECT MAX(ID) FROM Recommendations));
SELECT setval('xp_id_seq', (SELECT MAX(ID) FROM XP));
SELECT setval('timetracking_id_seq', (SELECT MAX(ID) FROM TimeTracking));

-- 2.1) P2P tekshiruvini qo'shish protsedurasi
-- Parametrlar: tekshiriluvchi nick, tekshiruvchi nick,
--              vazifa nomi, holat, vaqt
CREATE OR REPLACE PROCEDURE add_p2p_check(
    checked_peer   VARCHAR,
    checking_peer  VARCHAR,
    task_name      VARCHAR,
    p2p_state      check_status,
    check_time     TIME
)
LANGUAGE plpgsql AS $$
DECLARE
    v_check_id INTEGER;
BEGIN
    IF p2p_state = 'Start' THEN
        -- Yangi tekshiruv yozuvini qo'shish
        INSERT INTO Checks (Peer, Task, Date)
        VALUES (checked_peer, task_name, CURRENT_DATE)
        RETURNING ID INTO v_check_id;

        -- P2P jadvaliga yozuv qo'shish
        INSERT INTO P2P (CheckID, CheckingPeer, State, Time)
        VALUES (v_check_id, checking_peer, p2p_state, check_time);
    ELSE
        -- Tugallanmagan P2P tekshiruvini topish
        SELECT c.ID INTO v_check_id
        FROM Checks c
        JOIN P2P p ON p.CheckID = c.ID
        WHERE c.Peer     = checked_peer
          AND c.Task     = task_name
          AND p.CheckingPeer = checking_peer
          AND p.State    = 'Start'
          AND NOT EXISTS (
              SELECT 1 FROM P2P p2
              WHERE p2.CheckID     = p.CheckID
                AND p2.CheckingPeer= p.CheckingPeer
                AND p2.State      != 'Start'
          )
        ORDER BY c.Date DESC, p.Time DESC
        LIMIT 1;

        IF v_check_id IS NULL THEN
            RAISE EXCEPTION 'Tugallanmagan P2P tekshiruvi topilmadi!';
        END IF;

        -- P2P jadvaliga natija yozuvini qo'shish
        INSERT INTO P2P (CheckID, CheckingPeer, State, Time)
        VALUES (v_check_id, checking_peer, p2p_state, check_time);
    END IF;
END;
$$;

-- Test: P2P tekshiruvini boshlash
CALL add_p2p_check('mvazvelhwy', 'iosfiypdje', 'C1', 'Start', '10:00:00');
-- Test: P2P tekshiruvini muvaffaqiyatli yakunlash
CALL add_p2p_check('mvazvelhwy', 'iosfiypdje', 'C1', 'Success', '11:00:00');


-- 2.2) Verter tekshiruvini qo'shish protsedurasi
-- Parametrlar: tekshiriluvchi nick, vazifa nomi, holat, vaqt
CREATE OR REPLACE PROCEDURE add_verter_check(
    checked_peer VARCHAR,
    task_name    VARCHAR,
    v_state      check_status,
    check_time   TIME
)
LANGUAGE plpgsql AS $$
DECLARE
    v_check_id INTEGER;
BEGIN
    -- Eng so'ngi muvaffaqiyatli P2P tekshiruvi bo'lgan Checks ni topish
    SELECT c.ID INTO v_check_id
    FROM Checks c
    JOIN P2P p ON p.CheckID = c.ID
    WHERE c.Peer = checked_peer
      AND c.Task = task_name
      AND p.State = 'Success'
    ORDER BY c.Date DESC, p.Time DESC
    LIMIT 1;

    IF v_check_id IS NULL THEN
        RAISE EXCEPTION 'Muvaffaqiyatli P2P tekshiruvi topilmadi!';
    END IF;

    INSERT INTO Verter (CheckID, State, Time)
    VALUES (v_check_id, v_state, check_time);
END;
$$;

-- Test: Verter tekshiruvini boshlash
CALL add_verter_check('mvazvelhwy', 'C1', 'Start', '12:00:00');
-- Test: Verter tekshiruvini muvaffaqiyatli yakunlash
CALL add_verter_check('mvazvelhwy', 'C1', 'Success', '12:30:00');


-- 2.3) Trigger: P2P 'Start' qo'shilganda TransferredPoints yangilanadi
CREATE OR REPLACE FUNCTION fn_update_transferred_points()
RETURNS TRIGGER AS $$
DECLARE
    v_checked_peer VARCHAR;
BEGIN
    -- Faqat 'Start' holatida ishlaymiz
    IF NEW.State = 'Start' THEN
        -- Checks jadvalidan tekshiriluvchi pirni topamiz
        SELECT Peer INTO v_checked_peer
        FROM Checks
        WHERE ID = NEW.CheckID;

        -- TransferredPoints jadvalida juft mavjud bo'lsa yangilash, bo'lmasa qo'shish
        IF EXISTS (
            SELECT 1 FROM TransferredPoints
            WHERE CheckingPeer = NEW.CheckingPeer
              AND CheckedPeer  = v_checked_peer
        ) THEN
            UPDATE TransferredPoints
            SET PointsAmount = PointsAmount + 1
            WHERE CheckingPeer = NEW.CheckingPeer
              AND CheckedPeer  = v_checked_peer;
        ELSE
            INSERT INTO TransferredPoints (CheckingPeer, CheckedPeer, PointsAmount)
            VALUES (NEW.CheckingPeer, v_checked_peer, 1);
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_transferred_points ON P2P;
CREATE TRIGGER trg_update_transferred_points
    AFTER INSERT ON P2P
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_transferred_points();


-- 2.4) Trigger: XP jadvaliga yozuvdan oldin to'g'rilik tekshiruvi
CREATE OR REPLACE FUNCTION fn_check_xp_validity()
RETURNS TRIGGER AS $$
DECLARE
    v_max_xp     INTEGER;
    v_is_success BOOLEAN;
BEGIN
    -- Vazifaning maksimal XP sini olish
    SELECT t.MaxXP INTO v_max_xp
    FROM Tasks t
    JOIN Checks c ON c.Task = t.Title
    WHERE c.ID = NEW.CheckID;

    -- Tekshiruv muvaffaqiyatli ekanligini aniqlash:
    -- P2P Success bo'lishi kerak + Verter yo'q yoki Success bo'lishi kerak
    SELECT (
        -- P2P muvaffaqiyatli
        EXISTS (
            SELECT 1 FROM P2P
            WHERE CheckID = NEW.CheckID AND State = 'Success'
        )
        AND
        -- Verter yo'q yoki muvaffaqiyatli
        (
            NOT EXISTS (SELECT 1 FROM Verter WHERE CheckID = NEW.CheckID)
            OR
            EXISTS (
                SELECT 1 FROM Verter
                WHERE CheckID = NEW.CheckID AND State = 'Success'
            )
        )
    ) INTO v_is_success;

    -- Tekshiruvlar
    IF NOT v_is_success THEN
        RAISE WARNING 'XP qo''shilmadi: tekshiruv muvaffaqiyatli emas!';
        RETURN NULL;
    END IF;

    IF NEW.XPAmount > v_max_xp THEN
        RAISE WARNING 'XP qo''shilmadi: XP miqdori (%) maksimumdan (%) oshib ketdi!',
                      NEW.XPAmount, v_max_xp;
        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_xp_validity ON XP;
CREATE TRIGGER trg_check_xp_validity
    BEFORE INSERT ON XP
    FOR EACH ROW
    EXECUTE FUNCTION fn_check_xp_validity();

-- Test: To'g'ri XP qo'shish (yangi qo'shilgan muvaffaqiyatli tekshiruv uchun)
INSERT INTO XP (CheckID, XPAmount)
    SELECT c.ID, 100 FROM Checks c
    JOIN P2P p ON p.CheckID = c.ID AND p.State = 'Success'
    WHERE c.Peer = 'mvazvelhwy' AND c.Task = 'C1'
    AND NOT EXISTS (SELECT 1 FROM XP x WHERE x.CheckID = c.ID)
    ORDER BY c.ID DESC LIMIT 1;
-- Test: Noto'g'ri - XP haddan oshgan
INSERT INTO XP (CheckID, XPAmount)
    SELECT c.ID, 99999 FROM Checks c
    JOIN P2P p ON p.CheckID = c.ID AND p.State = 'Success'
    WHERE c.Peer = 'mvazvelhwy' AND c.Task = 'C1'
    ORDER BY c.ID DESC LIMIT 1;
-- Test: Noto'g'ri - muvaffaqiyatsiz tekshiruv (ID=0 mavjud emas)
INSERT INTO XP (CheckID, XPAmount) VALUES (0, 100);