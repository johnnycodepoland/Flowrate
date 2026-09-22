import sqlite3
import os

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "../flowrate.db")
        # Umożlwiamy odpalenie bazy danych z dowolnego miesjca
        self.connection = sqlite3.connect(db_path, check_same_thread=False)

        # Teraz każdy wiersz zwrócony preze fetchall(), będzie obiektem podobnym do słownika
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        # Ten tryb pozwala na jednoczesne odczyty i zapisy bez blokowania się nawzajem tak mocno jak domyślny tryb
        self.cursor.execute("PRAGMA journal_mode=WAL")

        # Ten tryb włączy pilnowanie kluczy obcych, czyli jeżeli warunek klucza nie zostanie spełniony to wiersz nie zostanie zapisany
        self.cursor.execute("PRAGMA foreign_keys=ON")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY,
                date TEXT,
                time INTEGER,
                distance INTEGER,
                RPE INTEGER)
                """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_tasks (
                id INTEGER PRIMARY KEY,
                training_id INTEGER,
                description TEXT,
                task_reps INTEGER,
                task_break INTEGER)
                """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_segments (
                id INTEGER PRIMARY KEY,
                task_id INTEGER,
                position INTEGER,
                description TEXT,
                distance REAL,
                target_time REAL,
                average_time REAL,
                times TEXT,
                FOREIGN KEY (task_id) REFERENCES training_tasks (id))
                """)

        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()