DROP TYPE IF EXISTS check_status CASCADE;
CREATE TYPE check_status AS ENUM ('Start', 'Success', 'Failure');

DROP TABLE IF EXISTS Peers CASCADE;
CREATE TABLE Peers (
    Nickname VARCHAR(50) PRIMARY KEY,
    Birthday DATE NOT NULL
);

DROP TABLE IF EXISTS Tasks CASCADE;
CREATE TABLE Tasks (
    Title      VARCHAR(50) PRIMARY KEY,
    ParentTask VARCHAR(50) REFERENCES Tasks(Title),
    MaxXP      INTEGER NOT NULL CHECK (MaxXP > 0)
);

DROP TABLE IF EXISTS Checks CASCADE;
CREATE TABLE Checks (
    ID   SERIAL PRIMARY KEY,
    Peer VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    Task VARCHAR(50) NOT NULL REFERENCES Tasks(Title),
    Date DATE NOT NULL
);

DROP TABLE IF EXISTS P2P CASCADE;
CREATE TABLE P2P (
    ID           SERIAL PRIMARY KEY,
    CheckID      INTEGER NOT NULL REFERENCES Checks(ID),
    CheckingPeer VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    State        check_status NOT NULL,
    Time         TIME NOT NULL
);

DROP TABLE IF EXISTS Verter CASCADE;
CREATE TABLE Verter (
    ID      SERIAL PRIMARY KEY,
    CheckID INTEGER NOT NULL REFERENCES Checks(ID),
    State   check_status NOT NULL,
    Time    TIME NOT NULL
);

-- (O'tkazilgan ball) table
DROP TABLE IF EXISTS TransferredPoints CASCADE;
CREATE TABLE TransferredPoints (
    ID           SERIAL PRIMARY KEY,
    CheckingPeer VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    CheckedPeer  VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    PointsAmount INTEGER NOT NULL DEFAULT 0 CHECK (PointsAmount >= 0)
);

DROP TABLE IF EXISTS Friends CASCADE;
CREATE TABLE Friends (
    ID    SERIAL PRIMARY KEY,
    Peer1 VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    Peer2 VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    CHECK (Peer1 <> Peer2)
);

DROP TABLE IF EXISTS Recommendations CASCADE;
CREATE TABLE Recommendations (
    ID              SERIAL PRIMARY KEY,
    Peer            VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    RecommendedPeer VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    CHECK (Peer <> RecommendedPeer)
);

DROP TABLE IF EXISTS XP CASCADE;
CREATE TABLE XP (
    ID       SERIAL PRIMARY KEY,
    CheckID  INTEGER NOT NULL REFERENCES Checks(ID),
    XPAmount INTEGER NOT NULL CHECK (XPAmount >= 0)
);

-- (Vaqt kuzatuvi) table
DROP TABLE IF EXISTS TimeTracking CASCADE;
CREATE TABLE TimeTracking (
    ID    SERIAL PRIMARY KEY,
    Peer  VARCHAR(50) NOT NULL REFERENCES Peers(Nickname),
    Date  DATE NOT NULL,
    Time  TIME NOT NULL,
    State INTEGER NOT NULL CHECK (State IN (1, 2))
);


-- import for Peers table 
CREATE OR REPLACE PROCEDURE import_peers(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Peers(Nickname, Birthday) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Peers table 
CREATE OR REPLACE PROCEDURE export_peers(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Peers TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

select * from Recommendations;
-- import for Tasks table 
CREATE OR REPLACE PROCEDURE import_tasks(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Tasks(Title, ParentTask, MaxXP) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Tasks table 
CREATE OR REPLACE PROCEDURE export_tasks(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Tasks TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for Check table
CREATE OR REPLACE PROCEDURE import_checks(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Checks(ID, Peer, Task, Date) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Check table
CREATE OR REPLACE PROCEDURE export_checks(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Checks TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for P2P table
CREATE OR REPLACE PROCEDURE import_p2p(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY P2P(ID, CheckID, CheckingPeer, State, Time) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- P2P jadvali uchun export
CREATE OR REPLACE PROCEDURE export_p2p(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY P2P TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for Verter table 
CREATE OR REPLACE PROCEDURE import_verter(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Verter(ID, CheckID, State, Time) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Verter table 
CREATE OR REPLACE PROCEDURE export_verter(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Verter TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for TransferredPoints table
CREATE OR REPLACE PROCEDURE import_transferred_points(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY TransferredPoints(ID, CheckingPeer, CheckedPeer, PointsAmount) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for TransferredPoints table
CREATE OR REPLACE PROCEDURE export_transferred_points(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY TransferredPoints TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for Friends table
CREATE OR REPLACE PROCEDURE import_friends(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Friends(ID, Peer1, Peer2) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Friends table
CREATE OR REPLACE PROCEDURE export_friends(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Friends TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for Recommendations table 
CREATE OR REPLACE PROCEDURE import_recommendations(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Recommendations(ID, Peer, RecommendedPeer) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for Recommendations table
CREATE OR REPLACE PROCEDURE export_recommendations(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY Recommendations TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for XP table
CREATE OR REPLACE PROCEDURE import_xp(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY XP(ID, CheckID, XPAmount) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for XP table 
CREATE OR REPLACE PROCEDURE export_xp(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY XP TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- import for TimeTracking table
CREATE OR REPLACE PROCEDURE import_time_tracking(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY TimeTracking(ID, Peer, Date, Time, State) FROM %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;

-- export for TimeTracking table
CREATE OR REPLACE PROCEDURE export_time_tracking(delim CHAR, file_path TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'COPY TimeTracking TO %L DELIMITER %L CSV HEADER',
        file_path, delim
    );
END;
$$;



INSERT INTO Peers (Nickname, Birthday) VALUES
    ('alice',   '2000-03-15'),
    ('bob',     '1999-07-22'),
    ('charlie', '2001-11-08'),
    ('diana',   '2000-05-30'),
    ('evan',    '1998-09-12'),
    ('fiona',   '2002-01-25'),
    ('george',  '2000-03-10'),
    ('helen',   '1999-12-05');

INSERT INTO Tasks (Title, ParentTask, MaxXP) VALUES
    ('C1',   NULL,  250),
    ('C2',   'C1',  350),
    ('C3',   'C2',  400),
    ('C4',   'C3',  500),
    ('C5',   'C4',  600),
    ('CPP1', 'C5',  700),
    ('CPP2', 'CPP1',800),
    ('CPP3', 'CPP2',900),
    ('A1',   'CPP3',1000),
    ('SQL1', 'C3',  500),
    ('SQL2', 'SQL1',700);

INSERT INTO Checks (Peer, Task, Date) VALUES
    ('alice',   'C1',   '2022-01-10'),
    ('bob',     'C1',   '2022-01-12'),
    ('charlie', 'C2',   '2022-02-05'),
    ('diana',   'C1',   '2022-01-15'),
    ('evan',    'C3',   '2022-03-20'),
    ('alice',   'C2',   '2022-02-10'),
    ('bob',     'C2',   '2022-02-14'),
    ('fiona',   'C1',   '2022-01-20'),
    ('george',  'C1',   '2022-01-22'),
    ('helen',   'C2',   '2022-02-18'),
    ('alice',   'C3',   '2022-03-01'),
    ('bob',     'CPP1', '2022-06-10'),
    ('charlie', 'SQL1', '2022-05-15'),
    ('diana',   'C2',   '2022-02-20');

INSERT INTO P2P (CheckID, CheckingPeer, State, Time) VALUES
    (1,  'bob',     'Start',   '10:00:00'),
    (1,  'bob',     'Success', '11:00:00'),
    (2,  'alice',   'Start',   '09:00:00'),
    (2,  'alice',   'Success', '10:30:00'),
    (3,  'alice',   'Start',   '14:00:00'),
    (3,  'alice',   'Success', '15:00:00'),
    (4,  'charlie', 'Start',   '09:00:00'),
    (4,  'charlie', 'Failure', '09:45:00'),
    (5,  'bob',     'Start',   '11:00:00'),
    (5,  'bob',     'Success', '12:00:00'),
    (6,  'charlie', 'Start',   '08:00:00'),
    (6,  'charlie', 'Success', '09:00:00'),
    (7,  'diana',   'Start',   '10:00:00'),
    (7,  'diana',   'Success', '11:00:00'),
    (8,  'alice',   'Start',   '13:00:00'),
    (8,  'alice',   'Success', '14:00:00'),
    (9,  'bob',     'Start',   '15:00:00'),
    (9,  'bob',     'Success', '16:00:00'),
    (10, 'evan',    'Start',   '09:30:00'),
    (10, 'evan',    'Success', '10:30:00'),
    (11, 'bob',     'Start',   '08:30:00'),
    (11, 'bob',     'Success', '09:30:00'),
    (12, 'alice',   'Start',   '10:00:00'),
    (12, 'alice',   'Success', '11:00:00'),
    (13, 'diana',   'Start',   '11:00:00'),
    (13, 'diana',   'Success', '12:30:00'),
    (14, 'evan',    'Start',   '09:00:00'),
    (14, 'evan',    'Failure', '10:00:00');

-- Verter - faqat muvaffaqiyatli P2P bo'lganlar uchun
INSERT INTO Verter (CheckID, State, Time) VALUES
    (1,  'Start',   '12:00:00'),
    (1,  'Success', '12:30:00'),
    (2,  'Start',   '11:00:00'),
    (2,  'Success', '11:45:00'),
    (3,  'Start',   '16:00:00'),
    (3,  'Success', '16:30:00'),
    (6,  'Start',   '10:00:00'),
    (6,  'Success', '10:20:00'),
    (11, 'Start',   '10:00:00'),
    (11, 'Failure', '10:30:00');

-- TransferredPoints (P2P tekshiruv boshlanganida +1 ball)
INSERT INTO TransferredPoints (CheckingPeer, CheckedPeer, PointsAmount) VALUES
    ('bob',     'alice',   3),
    ('alice',   'bob',     2),
    ('alice',   'charlie', 4),
    ('charlie', 'diana',   1),
    ('bob',     'evan',    2),
    ('alice',   'fiona',   1),
    ('bob',     'george',  1),
    ('evan',    'helen',   1),
    ('diana',   'alice',   2),
    ('evan',    'bob',     1);

INSERT INTO Friends (Peer1, Peer2) VALUES
    ('alice',   'bob'),
    ('bob',     'charlie'),
    ('charlie', 'diana'),
    ('diana',   'evan'),
    ('evan',    'fiona'),
    ('alice',   'charlie'),
    ('bob',     'diana'),
    ('fiona',   'george'),
    ('george',  'helen'),
    ('alice',   'diana');

INSERT INTO Recommendations (Peer, RecommendedPeer) VALUES
    ('alice',   'bob'),
    ('alice',   'charlie'),
    ('bob',     'alice'),
    ('charlie', 'alice'),
    ('diana',   'bob'),
    ('evan',    'alice'),
    ('fiona',   'charlie'),
    ('george',  'alice'),
    ('helen',   'bob'),
    ('diana',   'alice');

INSERT INTO XP (CheckID, XPAmount) VALUES
    (1,  200),
    (2,  220),
    (3,  300),
    (5,  350),
    (6,  320),
    (7,  330),
    (8,  240),
    (9,  250),
    (10, 280),
    (12, 600),
    (13, 450);

INSERT INTO TimeTracking (Peer, Date, Time, State) VALUES
    ('alice',   '2022-01-10', '08:30:00', 1),
    ('alice',   '2022-01-10', '22:00:00', 2),
    ('bob',     '2022-01-10', '07:45:00', 1),
    ('bob',     '2022-01-10', '12:00:00', 2),
    ('bob',     '2022-01-10', '13:00:00', 1),
    ('bob',     '2022-01-10', '21:00:00', 2),
    ('charlie', '2022-01-10', '09:00:00', 1),
    ('charlie', '2022-01-10', '15:00:00', 2),
    ('charlie', '2022-01-10', '16:00:00', 1),
    ('charlie', '2022-01-10', '20:00:00', 2),
    ('diana',   '2022-01-10', '11:30:00', 1),
    ('diana',   '2022-01-10', '19:00:00', 2),
    ('evan',    '2022-02-05', '08:00:00', 1),
    ('evan',    '2022-02-05', '11:00:00', 2),
    ('evan',    '2022-02-05', '12:00:00', 1),
    ('evan',    '2022-02-05', '20:00:00', 2),
    ('fiona',   '2022-02-05', '07:30:00', 1),
    ('fiona',   '2022-02-05', '21:00:00', 2),
    ('george',  '2022-03-01', '10:00:00', 1),
    ('george',  '2022-03-01', '18:00:00', 2),
    ('helen',   '2022-03-01', '11:00:00', 1),
    ('helen',   '2022-03-01', '17:00:00', 2),
    ('alice',   '2022-03-15', '06:00:00', 1),
    ('alice',   '2022-03-15', '10:00:00', 2),
    ('alice',   '2022-03-15', '11:00:00', 1),
    ('alice',   '2022-03-15', '22:00:00', 2),
    ('bob',     '2022-03-10', '11:30:00', 1),
    ('bob',     '2022-03-10', '20:00:00', 2);






TRUNCATE TABLE TimeTracking, XP, Recommendations, Friends,
               TransferredPoints, Verter, P2P, Checks CASCADE;
TRUNCATE TABLE Tasks CASCADE;
TRUNCATE TABLE Peers CASCADE;

SET datestyle = 'ISO, DMY';

\copy Peers(Nickname, Birthday) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/peers.csv' DELIMITER ';' CSV HEADER;

CREATE TEMP TABLE tmp_tasks (Title VARCHAR(50), ParentTask VARCHAR(50), MaxXP INTEGER);
\copy tmp_tasks FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/tasks.csv' DELIMITER ';' CSV HEADER;
INSERT INTO Tasks(Title, ParentTask, MaxXP)
    SELECT Title, NULLIF(ParentTask, 'None'), MaxXP FROM tmp_tasks;
DROP TABLE tmp_tasks;

\copy Checks(ID, Peer, Task, Date) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/checks.csv' DELIMITER ';' CSV HEADER;

CREATE TEMP TABLE tmp_p2p (ID INTEGER, CheckID INTEGER, CheckingPeer VARCHAR(50), State INTEGER, Time TIME);
\copy tmp_p2p FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/P2P.csv' DELIMITER ';' CSV HEADER;
INSERT INTO P2P(ID, CheckID, CheckingPeer, State, Time)
    SELECT ID, CheckID, CheckingPeer,
           CASE State WHEN 1 THEN 'Start' WHEN 2 THEN 'Success' ELSE 'Failure' END::check_status,
           Time
    FROM tmp_p2p;
DROP TABLE tmp_p2p;

CREATE TEMP TABLE tmp_verter (ID INTEGER, CheckID INTEGER, State INTEGER, Time TIME);
\copy tmp_verter FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/verter.csv' DELIMITER ';' CSV HEADER;
INSERT INTO Verter(ID, CheckID, State, Time)
    SELECT ID, CheckID,
           CASE State WHEN 1 THEN 'Start' WHEN 2 THEN 'Success' ELSE 'Failure' END::check_status,
           Time
    FROM tmp_verter;
DROP TABLE tmp_verter;

\copy TransferredPoints(ID, CheckingPeer, CheckedPeer, PointsAmount) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/transferred_points.csv' DELIMITER ';' CSV HEADER;

\copy Friends(ID, Peer1, Peer2) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/friends.csv' DELIMITER ';' CSV HEADER;

\copy Recommendations(ID, Peer, RecommendedPeer) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/recommendations.csv' DELIMITER ';' CSV HEADER;

\copy XP(ID, CheckID, XPAmount) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/xp.csv' DELIMITER ';' CSV HEADER;

\copy TimeTracking(ID, Peer, Date, Time, State) FROM 'C:/Users/hp/Desktop/SQL2_Info21_v1.0.ID_356301-Team_TL_emperora.8d6d669d_c715_410f-1/src/dataset_sql/time_tracking.csv' DELIMITER ';' CSV HEADER;

SELECT 'Peers' AS jadval, COUNT(*) AS soni FROM Peers
UNION ALL SELECT 'Tasks', COUNT(*) FROM Tasks
UNION ALL SELECT 'Checks', COUNT(*) FROM Checks
UNION ALL SELECT 'P2P', COUNT(*) FROM P2P
UNION ALL SELECT 'Verter', COUNT(*) FROM Verter
UNION ALL SELECT 'TransferredPoints', COUNT(*) FROM TransferredPoints
UNION ALL SELECT 'Friends', COUNT(*) FROM Friends
UNION ALL SELECT 'Recommendations', COUNT(*) FROM Recommendations
UNION ALL SELECT 'XP', COUNT(*) FROM XP
UNION ALL SELECT 'TimeTracking', COUNT(*) FROM TimeTracking;