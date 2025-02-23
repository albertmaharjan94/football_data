DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'football_db') THEN
        CREATE DATABASE football_db;
    END IF;
END
$$;

\c football_db;

CREATE TABLE IF NOT EXISTS football_matches (
    id SERIAL PRIMARY KEY,
    league VARCHAR(50),
    match_date DATE,
    match_time TIME,
    home_team VARCHAR(50),
    away_team VARCHAR(50),
    full_time_home_goals INT,
    full_time_away_goals INT,
    full_time_result CHAR(1),
    half_time_home_goals INT,
    half_time_away_goals INT,
    half_time_result CHAR(1),
    attendance INT,
    referee VARCHAR(50),
    home_shots INT,
    away_shots INT,
    home_shots_on_target INT,
    away_shots_on_target INT,
    home_corners INT,
    away_corners INT,
    home_fouls INT,
    away_fouls INT,
    home_yellow_cards INT,
    away_yellow_cards INT,
    home_red_cards INT,
    away_red_cards INT,
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE (match_date, home_team, away_team, league)
);

-- Create the 'admin' user if it doesn't exist
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'football_admin') THEN
        CREATE USER football_admin WITH ENCRYPTED PASSWORD 'f00tballAdmin';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE football_db TO football_admin;
ALTER ROLE football_admin CREATEDB;
GRANT CREATE ON SCHEMA public TO football_admin;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO football_admin;
GRANT CONNECT ON DATABASE football_db TO football_admin;
GRANT USAGE ON SCHEMA public TO football_admin;
GRANT ALL PRIVILEGES ON DATABASE football_db TO football_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES  IN SCHEMA public TO football_admin;
GRANT ALL PRIVILEGES ON DATABASE football_db TO football_admin;

-- Create an index for league (useful for filtering matches by league)
CREATE INDEX idx_league ON football_matches (league);
-- Create an index for referee (useful if filtering by referee name)
CREATE INDEX idx_referee ON football_matches (referee);
-- Create an index for home_team (useful for queries filtering by home team)
CREATE INDEX idx_home_team ON football_matches (home_team);
-- Create an index for away_team (useful for queries filtering by away team)
CREATE INDEX idx_away_team ON football_matches (away_team);
-- Create a composite index for (match_date, league) for date-based queries per league
CREATE INDEX idx_match_date_league ON football_matches (match_date, league);

-- Create the 'readonly' user if it doesn't exist
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'football_read') THEN
        CREATE USER football_read WITH ENCRYPTED PASSWORD 'footBallIreAD';
    END IF;
END
$$;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO football_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO football_read;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO football_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO football_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO football_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO football_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO football_admin;

GRANT CONNECT ON DATABASE football_db TO football_read;
GRANT USAGE ON SCHEMA public TO football_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO football_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO football_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO football_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO football_read;

-- Performance tuning settings
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '512MB';  
ALTER SYSTEM SET work_mem = '16MB';  
ALTER SYSTEM SET maintenance_work_mem = '128MB';
ALTER SYSTEM SET effective_cache_size = '2GB';  
ALTER SYSTEM SET random_page_cost = 1.1;  
ALTER SYSTEM SET autovacuum_max_workers = 5;  
ALTER SYSTEM SET autovacuum_naptime = 10;  
ALTER SYSTEM SET log_min_duration_statement = 500;
SELECT pg_reload_conf();