-- 3.1 TransferredPoints jadvalini o'qilishi oson ko'rinishda
CREATE OR REPLACE FUNCTION fn_transferred_points_readable()
RETURNS TABLE(Peer1 VARCHAR, Peer2 VARCHAR, PointsAmount INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT
        tp1.CheckingPeer AS Peer1,
        tp1.CheckedPeer  AS Peer2,
        (tp1.PointsAmount - COALESCE(tp2.PointsAmount, 0)) AS PointsAmount
    FROM TransferredPoints tp1
    LEFT JOIN TransferredPoints tp2
        ON tp2.CheckingPeer = tp1.CheckedPeer
        AND tp2.CheckedPeer = tp1.CheckingPeer
    WHERE tp1.CheckingPeer < tp1.CheckedPeer
       OR NOT EXISTS (
           SELECT 1 FROM TransferredPoints
           WHERE CheckingPeer = tp1.CheckedPeer
             AND CheckedPeer  = tp1.CheckingPeer
       );
END;
$$ LANGUAGE plpgsql;

-- Test
SELECT * FROM fn_transferred_points_readable();


-- 3.2) Pir nomi, muvaffaqiyatli tekshirilgan vazifa, olingan XP
CREATE OR REPLACE FUNCTION fn_successful_checks()
RETURNS TABLE(Peer VARCHAR, Task VARCHAR, XP INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.Peer::VARCHAR,
        c.Task::VARCHAR,
        x.XPAmount
    FROM Checks c
    JOIN XP x ON x.CheckID = c.ID
    JOIN P2P p ON p.CheckID = c.ID AND p.State = 'Success'
    WHERE
        -- Verter yo'q yoki muvaffaqiyatli
        NOT EXISTS (
            SELECT 1 FROM Verter v
            WHERE v.CheckID = c.ID AND v.State = 'Failure'
        )
    ORDER BY c.Peer, c.Task;
END;
$$ LANGUAGE plpgsql;

-- Test
SELECT * FROM fn_successful_checks();


-- 3.3) Kun davomida kampusdan chiqmagan pirlarni aniqlaydigan funksiya
CREATE OR REPLACE FUNCTION fn_peers_not_left_campus(check_date DATE)
RETURNS TABLE(Peer VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT tt.Peer::VARCHAR
    FROM TimeTracking tt
    WHERE tt.Date = check_date
    GROUP BY tt.Peer
    -- Faqat 1 marta kirgan va chiqmagan (faqat bitta yozuv: kirish)
    HAVING COUNT(*) = 1 AND MAX(tt.State) = 1
    
    UNION
    
    -- Yoki kirgan va oxirgi chiqishlari yo'q (juft kirish-chiqish soni tekshiriladi)
    SELECT DISTINCT t.Peer::VARCHAR
    FROM TimeTracking t
    WHERE t.Date = check_date
    GROUP BY t.Peer
    HAVING
        SUM(CASE WHEN t.State = 1 THEN 1 ELSE 0 END) =
        SUM(CASE WHEN t.State = 2 THEN 1 ELSE 0 END)
       AND
        -- '2' holat soni 0 - ya'ni hech chiqmagan
        SUM(CASE WHEN t.State = 2 THEN 1 ELSE 0 END) = 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_peers_not_left_campus(check_date DATE)
RETURNS TABLE(Peer VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT tt.Peer::VARCHAR
    FROM TimeTracking tt
    WHERE tt.Date = check_date
    GROUP BY tt.Peer
    HAVING COUNT(CASE WHEN tt.State = 2 THEN 1 END) = 0;
END;
$$ LANGUAGE plpgsql;

-- Test
SELECT * FROM fn_peers_not_left_campus('2022-01-10');


-- 3.4) Har bir pirning TransferredPoints bo'yicha ball o'zgarishi
CREATE OR REPLACE PROCEDURE pr_peers_points_change(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    SELECT
        Peer,
        SUM(PointsChange) AS PointsChange
    FROM (
        SELECT CheckingPeer AS Peer,  PointsAmount AS PointsChange FROM TransferredPoints
        UNION ALL
        SELECT CheckedPeer  AS Peer, -PointsAmount AS PointsChange FROM TransferredPoints
    ) sub
    GROUP BY Peer
    ORDER BY PointsChange DESC;
END;
$$;

-- Test
BEGIN;
CALL pr_peers_points_change();
FETCH ALL FROM res;
COMMIT;


-- 3.5) Ball o'zgarishini 1-funksiya natijalari bo'yicha hisoblash
CREATE OR REPLACE PROCEDURE pr_peers_points_change_from_fn(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    SELECT
        Peer,
        SUM(PointsChange) AS PointsChange
    FROM (
        SELECT Peer1 AS Peer,  PointsAmount AS PointsChange FROM fn_transferred_points_readable()
        UNION ALL
        SELECT Peer2 AS Peer, -PointsAmount AS PointsChange FROM fn_transferred_points_readable()
    ) sub
    GROUP BY Peer
    ORDER BY PointsChange DESC;
END;
$$;

-- Test
BEGIN;
CALL pr_peers_points_change_from_fn();
FETCH ALL FROM res;
COMMIT;


-- 3.6) Har bir kunda eng ko'p tekshirilgan vazifani aniqlash
CREATE OR REPLACE PROCEDURE pr_most_checked_task_per_day(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH daily_counts AS (
        SELECT
            Date,
            Task,
            COUNT(*) AS check_count
        FROM Checks
        GROUP BY Date, Task
    ),
    max_per_day AS (
        SELECT Date, MAX(check_count) AS max_count
        FROM daily_counts
        GROUP BY Date
    )
    SELECT
        TO_CHAR(dc.Date, 'DD.MM.YYYY') AS Day,
        dc.Task
    FROM daily_counts dc
    JOIN max_per_day mpd
        ON dc.Date = mpd.Date AND dc.check_count = mpd.max_count
    ORDER BY dc.Date DESC;
END;
$$;

-- Test
BEGIN;
CALL pr_most_checked_task_per_day();
FETCH ALL FROM res;
COMMIT;


-- 3.7) Berilgan blokdagi barcha vazifalarni bajargan pirlar va oxirgi vazifani bajargan kunni topish
-- Parametr: blok nomi (masalan, 'C' yoki 'CPP')
CREATE OR REPLACE PROCEDURE pr_completed_block(
    block_name VARCHAR,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH block_tasks AS (
        SELECT Title FROM Tasks
        WHERE Title LIKE block_name || '%'
    ),
    peer_completed AS (
        SELECT
            c.Peer,
            MAX(c.Date) AS completion_date,
            COUNT(DISTINCT c.Task) AS done_tasks
        FROM Checks c
        JOIN P2P p ON p.CheckID = c.ID AND p.State = 'Success'
        LEFT JOIN Verter v ON v.CheckID = c.ID
        WHERE c.Task IN (SELECT Title FROM block_tasks)
          AND (v.ID IS NULL OR v.State = 'Success')
        GROUP BY c.Peer
    )
    SELECT
        pc.Peer,
        TO_CHAR(pc.completion_date, 'DD.MM.YYYY') AS Day
    FROM peer_completed pc
    WHERE pc.done_tasks = (SELECT COUNT(*) FROM block_tasks)
    ORDER BY pc.completion_date;
END;
$$;

-- Test
BEGIN;
CALL pr_completed_block('C');
FETCH ALL FROM res;
COMMIT;


-- 3.8) Har bir pir uchun do'stlari tavsiya qilgan tekshiruvchini topish
CREATE OR REPLACE PROCEDURE pr_recommended_peer(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH friend_recommendations AS (
        SELECT
            f.Peer1 AS Peer,
            r.RecommendedPeer,
            COUNT(*) AS rec_count
        FROM Friends f
        JOIN Recommendations r ON r.Peer = f.Peer2
        WHERE r.RecommendedPeer <> f.Peer1
        GROUP BY f.Peer1, r.RecommendedPeer

        UNION ALL

        SELECT
            f.Peer2 AS Peer,
            r.RecommendedPeer,
            COUNT(*) AS rec_count
        FROM Friends f
        JOIN Recommendations r ON r.Peer = f.Peer1
        WHERE r.RecommendedPeer <> f.Peer2
        GROUP BY f.Peer2, r.RecommendedPeer
    ),
    aggregated AS (
        SELECT Peer, RecommendedPeer, SUM(rec_count) AS total
        FROM friend_recommendations
        GROUP BY Peer, RecommendedPeer
    ),
    ranked AS (
        SELECT
            Peer,
            RecommendedPeer,
            ROW_NUMBER() OVER (PARTITION BY Peer ORDER BY total DESC) AS rn
        FROM aggregated
    )
    SELECT Peer, RecommendedPeer
    FROM ranked
    WHERE rn = 1
    ORDER BY Peer;
END;
$$;

-- Test
BEGIN;
CALL pr_recommended_peer();
FETCH ALL FROM res;
COMMIT;


-- 3.9) Ikki blokni boshlagan/boshlamagan pirlar foizi
-- Parametrlar: blok1 nomi, blok2 nomi
CREATE OR REPLACE PROCEDURE pr_block_start_percentages(
    block1 VARCHAR,
    block2 VARCHAR,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH total_peers AS (
        SELECT COUNT(*) AS total FROM Peers
    ),
    started1 AS (
        SELECT DISTINCT Peer FROM Checks WHERE Task LIKE block1 || '%'
    ),
    started2 AS (
        SELECT DISTINCT Peer FROM Checks WHERE Task LIKE block2 || '%'
    )
    SELECT
        ROUND(100.0 * COUNT(CASE WHEN s1.Peer IS NOT NULL AND s2.Peer IS NULL THEN 1 END) / tp.total) AS StartedBlock1,
        ROUND(100.0 * COUNT(CASE WHEN s2.Peer IS NOT NULL AND s1.Peer IS NULL THEN 1 END) / tp.total) AS StartedBlock2,
        ROUND(100.0 * COUNT(CASE WHEN s1.Peer IS NOT NULL AND s2.Peer IS NOT NULL THEN 1 END) / tp.total) AS StartedBothBlocks,
        ROUND(100.0 * COUNT(CASE WHEN s1.Peer IS NULL AND s2.Peer IS NULL THEN 1 END) / tp.total) AS DidntStartAnyBlock
    FROM Peers p
    LEFT JOIN started1 s1 ON s1.Peer = p.Nickname
    LEFT JOIN started2 s2 ON s2.Peer = p.Nickname
    CROSS JOIN total_peers tp
    GROUP BY tp.total;
END;
$$;

-- Test
BEGIN;
CALL pr_block_start_percentages('C', 'SQL');
FETCH ALL FROM res;
COMMIT;


-- 3.10) Tug'ilgan kunida muvaffaqiyatli/muvaffaqiyatsiz tekshiruv o'tkazgan pirlar foizi
CREATE OR REPLACE PROCEDURE pr_birthday_check_percentages(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH birthday_checks AS (
        SELECT
            c.Peer,
            -- Muvaffaqiyatli: P2P Success + Verter yo'q yoki Success
            BOOL_OR(
                p.State = 'Success'
                AND (
                    NOT EXISTS (SELECT 1 FROM Verter v WHERE v.CheckID = c.ID)
                    OR EXISTS (SELECT 1 FROM Verter v WHERE v.CheckID = c.ID AND v.State = 'Success')
                )
            ) AS had_success,
            -- Muvaffaqiyatsiz: P2P Failure yoki Verter Failure
            BOOL_OR(
                p.State = 'Failure'
                OR EXISTS (SELECT 1 FROM Verter v WHERE v.CheckID = c.ID AND v.State = 'Failure')
            ) AS had_failure
        FROM Checks c
        JOIN Peers pr ON pr.Nickname = c.Peer
        JOIN P2P p ON p.CheckID = c.ID AND p.State != 'Start'
        WHERE EXTRACT(MONTH FROM c.Date) = EXTRACT(MONTH FROM pr.Birthday)
          AND EXTRACT(DAY   FROM c.Date) = EXTRACT(DAY   FROM pr.Birthday)
        GROUP BY c.Peer
    ),
    total AS (SELECT COUNT(*) AS total FROM Peers)
    SELECT
        ROUND(100.0 * COUNT(CASE WHEN bc.had_success THEN 1 END) / t.total) AS SuccessfulChecks,
        ROUND(100.0 * COUNT(CASE WHEN bc.had_failure THEN 1 END) / t.total) AS UnsuccessfulChecks
    FROM total t
    LEFT JOIN birthday_checks bc ON TRUE
    GROUP BY t.total;
END;
$$;

-- Test
BEGIN;
CALL pr_birthday_check_percentages();
FETCH ALL FROM res;
COMMIT;


-- 3.11) Vazifa1 va Vazifa2 ni topshirgan, lekin Vazifa3 ni topshirmagan pirlar
CREATE OR REPLACE PROCEDURE pr_passed_12_not_3(
    task1 VARCHAR,
    task2 VARCHAR,
    task3 VARCHAR,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH successful_peers AS (
        SELECT DISTINCT c.Peer, c.Task
        FROM Checks c
        JOIN P2P p ON p.CheckID = c.ID AND p.State = 'Success'
        WHERE NOT EXISTS (
            SELECT 1 FROM Verter v
            WHERE v.CheckID = c.ID AND v.State = 'Failure'
        )
    )
    SELECT DISTINCT sp1.Peer
    FROM successful_peers sp1
    JOIN successful_peers sp2 ON sp2.Peer = sp1.Peer AND sp2.Task = task2
    WHERE sp1.Task = task1
      AND NOT EXISTS (
          SELECT 1 FROM successful_peers sp3
          WHERE sp3.Peer = sp1.Peer AND sp3.Task = task3
      )
    ORDER BY sp1.Peer;
END;
$$;

-- Test
BEGIN;
CALL pr_passed_12_not_3('C1', 'C2', 'C3');
FETCH ALL FROM res;
COMMIT;


-- 3.12) Rekursiv CTE: har bir vazifa uchun oldingi vazifalar soni
CREATE OR REPLACE PROCEDURE pr_task_predecessors(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH RECURSIVE task_chain AS (
        -- Bosh vazifalar (ParentTask = NULL)
        SELECT Title, 0 AS prev_count
        FROM Tasks
        WHERE ParentTask IS NULL

        UNION ALL

        -- Rekursiv qism
        SELECT t.Title, tc.prev_count + 1
        FROM Tasks t
        JOIN task_chain tc ON tc.Title = t.ParentTask
    )
    SELECT Title AS Task, prev_count AS PrevCount
    FROM task_chain
    ORDER BY prev_count, Title;
END;
$$;

-- Test
BEGIN;
CALL pr_task_predecessors();
FETCH ALL FROM res;
COMMIT;


-- 3.13) lucky days - ketma-ket N ta muvaffaqiyatli tekshiruv bor kunlar
-- XP har bir tekshiruv uchun maksimumdan 80% dan kam emas
CREATE OR REPLACE PROCEDURE pr_lucky_days(
    n_consecutive INTEGER,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH check_results AS (
        SELECT
            c.ID,
            c.Date,
            p.Time AS start_time,
            x.XPAmount,
            t.MaxXP,
            -- Muvaffaqiyatli tekshiruv va XP >= 80%
            CASE WHEN
                p.State = 'Success'
                AND (
                    NOT EXISTS (SELECT 1 FROM Verter v WHERE v.CheckID = c.ID)
                    OR EXISTS (SELECT 1 FROM Verter v WHERE v.CheckID = c.ID AND v.State = 'Success')
                )
                AND x.XPAmount >= t.MaxXP * 0.8
            THEN 1 ELSE 0 END AS is_lucky
        FROM Checks c
        JOIN P2P p ON p.CheckID = c.ID AND p.State != 'Start'
        JOIN Tasks t ON t.Title = c.Task
        LEFT JOIN XP x ON x.CheckID = c.ID
        ORDER BY c.Date, p.Time
    ),
    with_groups AS (
        SELECT
            Date,
            is_lucky,
            SUM(CASE WHEN is_lucky = 0 THEN 1 ELSE 0 END)
                OVER (PARTITION BY Date ORDER BY start_time) AS grp
        FROM check_results
    ),
    consecutive_counts AS (
        SELECT Date, grp, COUNT(*) AS streak
        FROM with_groups
        WHERE is_lucky = 1
        GROUP BY Date, grp
    )
    SELECT DISTINCT TO_CHAR(Date, 'DD.MM.YYYY') AS Day
    FROM consecutive_counts
    WHERE streak >= n_consecutive
    ORDER BY Day;
END;
$$;

-- Test
BEGIN;
CALL pr_lucky_days(2);
FETCH ALL FROM res;
COMMIT;


-- 3.14) Eng ko'p XP to'plagan pir
CREATE OR REPLACE PROCEDURE pr_top_xp_peer(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    SELECT c.Peer, SUM(x.XPAmount) AS XP
    FROM XP x
    JOIN Checks c ON c.ID = x.CheckID
    GROUP BY c.Peer
    ORDER BY XP DESC
    LIMIT 1;
END;
$$;

-- Test
BEGIN;
CALL pr_top_xp_peer();
FETCH ALL FROM res;
COMMIT;


-- 3.15) Berilgan vaqtdan oldin N marta kelgan pirlar
CREATE OR REPLACE PROCEDURE pr_early_arrivals(
    early_time TIME,
    min_times  INTEGER,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    SELECT Peer
    FROM TimeTracking
    WHERE State = 1 AND Time < early_time
    GROUP BY Peer
    HAVING COUNT(*) >= min_times
    ORDER BY Peer;
END;
$$;

-- Test
BEGIN;
CALL pr_early_arrivals('10:00:00', 2);
FETCH ALL FROM res;
COMMIT;


-- 3.16) So'ngi N kunda M martadan ko'p chiqib ketgan pirlar
CREATE OR REPLACE PROCEDURE pr_frequent_leavers(
    n_days   INTEGER,
    m_times  INTEGER,
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    SELECT Peer
    FROM TimeTracking
    WHERE State = 2
      AND Date >= CURRENT_DATE - n_days
    GROUP BY Peer
    HAVING COUNT(*) > m_times
    ORDER BY Peer;
END;
$$;

-- Test
BEGIN;
CALL pr_frequent_leavers(365, 1);
FETCH ALL FROM res;
COMMIT;


-- 3.17) Har bir oy uchun erta kelishlar foizi
-- (o'sha oyda tug'ilgan pirlarning 12:00 dan oldin kelish foizi)
CREATE OR REPLACE PROCEDURE pr_early_entries_by_birth_month(
    INOUT result REFCURSOR DEFAULT 'res'
)
LANGUAGE plpgsql AS $$
BEGIN
    OPEN result FOR
    WITH birth_month_tracking AS (
        SELECT
            TO_CHAR(TO_DATE(TO_CHAR(EXTRACT(MONTH FROM p.Birthday)::INT, '99'), 'MM'), 'Month') AS Month,
            EXTRACT(MONTH FROM p.Birthday) AS month_num,
            COUNT(*) AS total_entries,
            COUNT(CASE WHEN tt.Time < '12:00:00' THEN 1 END) AS early_entries
        FROM TimeTracking tt
        JOIN Peers p ON p.Nickname = tt.Peer
        WHERE tt.State = 1
        GROUP BY EXTRACT(MONTH FROM p.Birthday)
    )
    SELECT
        TRIM(Month) AS Month,
        CASE
            WHEN total_entries = 0 THEN 0
            ELSE ROUND(100.0 * early_entries / total_entries)
        END AS EarlyEntries
    FROM birth_month_tracking
    ORDER BY month_num;
END;
$$;

-- Test
BEGIN;
CALL pr_early_entries_by_birth_month();
FETCH ALL FROM res;
COMMIT;