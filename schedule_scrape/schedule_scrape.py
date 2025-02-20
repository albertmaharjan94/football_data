import time
import psycopg2
import os
import schedule

import csv
import psycopg2
import datetime
import re
import os
import chardet
import requests
import urllib.request

from bs4 import BeautifulSoup
from user_agent import generate_user_agent

# Database connection parameters
DB_PARAMS = {
    "dbname": "football_db",
    "user": "football_admin",
    "password": "f00tB@!!@DM",
    "host": "0.0.0.0",
    "port": "5432"
}

BASE_URL = 'https://www.football-data.co.uk/'

LEAGUES = [
    {'name': 'premier-league', 'path': 'englandm.php', 'key': 'E0', 'links': [], 'range': 23},
    {'name': 'la-liga', 'path': 'spainm.php', 'key': 'SP1', 'links': [], 'range': 22},
    {'name': 'bundesliga', 'path': 'germanym.php', 'key': 'D1', 'links': [], 'range': 22},
    {'name': 'serie-a', 'path': 'italym.php', 'key': 'I1', 'links': [], 'range': 22},
    {'name': 'ligue-1', 'path': 'francem.php', 'key': 'F1', 'links': [], 'range': 22}
]

# Column Mapping
COLUMN_MAPPING = {
    "Date": "match_date",
    "Time": "match_time",
    "HomeTeam": "home_team",
    "AwayTeam": "away_team",
    "FTHG": "full_time_home_goals",
    "FTAG": "full_time_away_goals",
    "FTR": "full_time_result",
    "HTHG": "half_time_home_goals",
    "HTAG": "half_time_away_goals",
    "HTR": "half_time_result",
    "Attendance": "attendance",
    "Referee": "referee",
    "HS": "home_shots",
    "AS": "away_shots",
    "HST": "home_shots_on_target",
    "AST": "away_shots_on_target",
    "HC": "home_corners",
    "AC": "away_corners",
    "HF": "home_fouls",
    "AF": "away_fouls",
    "HY": "home_yellow_cards",
    "AY": "away_yellow_cards",
    "HR": "home_red_cards",
    "AR": "away_red_cards"
}

def connect_db():
    """Establish a database connection."""
    return psycopg2.connect(**DB_PARAMS)

def create_table():
    """Create the football data table if it doesn't exist."""
    query = """
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
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    print("✅ Database table is ready.")
def insert_into_db(reader, league_name):
    """Insert or update records in PostgreSQL."""
    query = """
    INSERT INTO football_matches (
        league, match_date, match_time, home_team, away_team,
        full_time_home_goals, full_time_away_goals, full_time_result,
        half_time_home_goals, half_time_away_goals, half_time_result,
        attendance, referee, home_shots, away_shots,
        home_shots_on_target, away_shots_on_target,
        home_corners, away_corners, home_fouls, away_fouls,
        home_yellow_cards, away_yellow_cards,
        home_red_cards, away_red_cards,
        last_updated
    ) VALUES (
         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()
    )
    ON CONFLICT (match_date, home_team, away_team, league) DO UPDATE SET
        full_time_home_goals = EXCLUDED.full_time_home_goals,
        full_time_away_goals = EXCLUDED.full_time_away_goals,
        full_time_result = EXCLUDED.full_time_result,
        last_updated = NOW();
    """

    with connect_db() as conn:
        with conn.cursor() as cur:
            for row in reader:
                if not row["Date"].strip():
                    continue  

                try:
                    date_parts = row["Date"].split("/")
                    if len(date_parts) == 3:
                        match_date = datetime.datetime.strptime(row["Date"], "%d/%m/%y").strftime('%Y-%m-%d')
                    else:
                        continue  
                except ValueError:
                    continue  

                # Parse match_time correctly
                match_time = row.get("Time", "").strip()
                if match_time:
                    try:
                        match_time = datetime.datetime.strptime(match_time, "%H:%M").time()
                    except ValueError:
                        match_time = None
                else:
                    match_time = None

                data = [league_name, match_date, match_time]

                for col in COLUMN_MAPPING.keys():
                    if col in ["Date", "Time"]:
                        continue 

                    value = row.get(col, "").strip()
                    if value == "":
                        value = None  # Handle missing values as NULL
                    elif col in ["FTHG", "FTAG", "HTHG", "HTAG", "HS", "AS", "HST", "AST", "HC", "AC", "HF", "AF", "HY", "AY", "HR", "AR", "Attendance"]:  
                        try:
                            value = int(value) if value is not None else None
                        except ValueError:
                            value = None
                    data.append(value)

                # Debugging print statement to check data length and values
                print(f"Data Length: {len(data)} / Expected: 26")
                print(f"Data Values: {data}")

                if len(data) != 26:
                    print("❌ Error: Data length mismatch, skipping row.")
                    continue

                cur.execute(query, data)
                break

            conn.commit()
    print(f"✅ {league_name} database updated.")


def fetch_league_links(league):
    """Fetch CSV file links for a given league."""
    headers = {'User-Agent': generate_user_agent(device_type="desktop")}
    response = requests.get(BASE_URL + league['path'], headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=re.compile(r"mmz4281")):
        if league['key'] + '.csv' in link['href']:
            league['links'].append(BASE_URL + link['href'])

def download_and_store_data(league):
    """Download data and store it in PostgreSQL."""
    for link in league['links']:
        headers = {'User-Agent': generate_user_agent(device_type="desktop")}
        req = urllib.request.Request(link, headers=headers)
        with urllib.request.urlopen(req) as response:
            raw_data = response.read()
            detected_encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            data = raw_data.decode(detected_encoding)
            reader = csv.DictReader(data.splitlines())
            insert_into_db(reader, league["name"])

create_table()
for league in LEAGUES:
    fetch_league_links(league)
    download_and_store_data(league)


# # Database connection details from environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")

# def wait_for_postgres():
#     """Wait until PostgreSQL is ready before starting the scheduler."""
#     while True:
#         try:
#             conn = psycopg2.connect(DATABASE_URL)
#             conn.close()
#             print("✅ PostgreSQL is ready! Starting the scheduler...")
#             break
#         except psycopg2.OperationalError:
#             print("⏳ Waiting for PostgreSQL to be ready...")
#             time.sleep(5)

# def scrape_and_store_data():
#     """Scrapes data and saves it to the PostgreSQL database."""
#     print("🚀 Scraping data...")
#     scraped_data = "sample_data_" + str(time.time())  # Simulated scraped data

#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO scraped_data (data) VALUES (%s);", (scraped_data,))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("✅ Data stored successfully!")
#     except Exception as e:
#         print(f"❌ Error storing data: {e}")

# if __name__ == "__main__":
#     # Ensure PostgreSQL is ready before scheduling tasks
#     wait_for_postgres()

#     # Schedule the task to run daily at midnight (00:00)
#     schedule.every().day.at("00:00").do(scrape_and_store_data)

#     print("📅 Scheduler started. Waiting for the next execution...")

#     # Run the scheduler indefinitely
#     while True:
#         schedule.run_pending()
#         time.sleep(60)  # Check every minute if the task should run
