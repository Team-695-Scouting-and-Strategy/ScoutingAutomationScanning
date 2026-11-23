from contextlib import closing
import sqlite3

from pathlib import Path
import os 
import sys

# get the path for the SQLite database file
def get_db_path(app_name, db_filename):
    home = Path.home()
    
    if sys.platform.startswith("win"): 
        # windows: %APPDATA%\app_name
        base_dir = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
    elif sys.platform == "darwin": 
        # macOS: ~/Library/Application Support/app_name
        base_dir = home / "Library" / "Application Support"
    else:
        # linux/unix: ~/.local/share/app_name
        data_home = os.environ.get("XDG_DATA_HOME", home / ".local" / "share")
        base_dir = Path(data_home)
        
    app_dir = base_dir / app_name
    
    # ensure the directory exists before SQLite tries to write to it
    app_dir.mkdir(parents=True, exist_ok=True)
    
    return app_dir / db_filename

# get a connection to the SQLite database
def get_connection():
	connection = sqlite3.connect(get_db_path("ScoutingApp", "scouting.db"))
	connection.row_factory = sqlite3.Row
	return connection

# to be run as app is init'ed creating a new database if it doesn't exist yet
def initialize_database():
    with closing(get_connection()) as connection:
        with connection:
            tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            if "matches" in tables and "match_scouting" not in tables:
                connection.execute("ALTER TABLE matches RENAME TO match_scouting")

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS match_scouting (
                    id INTEGER PRIMARY KEY,
                    team_number INTEGER NOT NULL,
                    match_number INTEGER NOT NULL,
                    auton_fuel_scored INTEGER NOT NULL,
                    teleop_fuel_scored INTEGER NOT NULL,
                    no_show BOOLEAN NOT NULL,
                    robot_disabled BOOLEAN NOT NULL,
                    beached BOOLEAN NOT NULL,
                    stuck_on_bump BOOLEAN NOT NULL,
                    other_problem BOOLEAN NOT NULL,
                    climbed BOOLEAN NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pit_scouting (
                    id INTEGER PRIMARY KEY,
                    team_number INTEGER NOT NULL,
                    robot_weight REAL NOT NULL,
                    robot_length REAL NOT NULL,
                    robot_height REAL NOT NULL,
                    can_climb BOOLEAN NOT NULL,
                    drive_train_type INTEGER NOT NULL,
                    shooter_type INTEGER NOT NULL,
                    max_fuel_capacity INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )