import os
import sqlite3
import sys


class DatabaseManager:
    """
    Handles secure database initialization, path mapping for Windows environments,
    automatic schema migrations, and parameterized query transactional execution.
    """

    def __init__(self):
        # Resolve the standard Windows AppData folder path for absolute security
        app_data_root = os.environ.get("APPDATA")
        if not app_data_root:
            # Fallback path if environment string is missing
            app_data_root = os.path.expanduser("~")

        self.db_dir = os.path.join(app_data_root, "Sport_aid")
        self.db_path = os.path.join(self.db_dir, "sport_aid.db")

        # Ensure target workspace sub-folders exist before establishing connection
        os.makedirs(self.db_dir, exist_ok=True)

        # Initialize tables immediately
        self._initialize_database_schema()

    def get_connection(self) -> sqlite3.Connection:
        """Establishes an isolated raw database connection with active foreign key constraints."""
        conn = sqlite3.connect(self.db_path)
        # Force SQLite engine to monitor relational foreign key rules
        conn.execute("PRAGMA foreign_keys = ON;")
        # Allow row extraction by dictionary keys instead of indexed tuples
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_database_schema(self):
        """Creates physical application entity tables using parameterized schema strings."""
        schema_queries = [
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')) NOT NULL,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_type TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                distance_km REAL DEFAULT 0,
                steps INTEGER DEFAULT 0,
                calories_burned REAL NOT NULL,
                log_date TEXT NOT NULL,
                notes TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS routines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS routine_exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                routine_id INTEGER NOT NULL,
                exercise_name TEXT NOT NULL,
                order_index INTEGER NOT NULL,
                target_duration_seconds INTEGER DEFAULT 0,
                target_reps INTEGER DEFAULT 0,
                rest_seconds INTEGER DEFAULT 0,
                FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE
            );
            """
        ]

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for query in schema_queries:
                cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database Initialization Structural Failure: {e}", file=sys.stderr)
            raise e
        finally:
            if conn:
                conn.close()

    def execute_write(self, query: str, params: tuple = ()) -> int:
        """Executes a parameterized INSERT, UPDATE, or DELETE modification query securely."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Secure Database Transaction Write Failure: {e}", file=sys.stderr)
            raise e
        finally:
            conn.close()

    def execute_read(self, query: str, params: tuple = ()) -> list:
        """Executes a parameterized SELECT query extraction safely, returning rows."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Secure Database Transaction Read Failure: {e}", file=sys.stderr)
            raise e
        finally:
            conn.close()
