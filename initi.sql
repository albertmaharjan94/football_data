CREATE DATABASE football_db;
use football_db;
-- Create the 'football_matches' table 
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

-- Create the 'admin' user
CREATE USER football_admin WITH ENCRYPTED PASSWORD 'f00tB@!!@DM';
GRANT ALL PRIVILEGES ON DATABASE football_db TO football_admin;

-- Create the 'readonly' user
CREATE USER football_read WITH ENCRYPTED PASSWORD '#fOOTbALLR3@D';
GRANT CONNECT ON DATABASE football_db TO football_read;
GRANT USAGE ON SCHEMA public TO football_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO football_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO football_read;

-- Performance tuning for 100+ concurrent read users
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