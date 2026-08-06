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
                task_distance INTEGER,
                task_reps INTEGER,
                task_target_time INTEGER,
                task_break INTEGER,
                average_segment_time INTEGER)
                """)

        self.connection.commit()
