from backend.database import Database

database = Database()

class PersonalBestRepository:
    def __init__(self, database):
        self.connection = database.connection

        self.database = database

    def get_all_personal_bests(self):
        cursor = self.database.get_cursor()

        cursor.execute(
            """SELECT distance, time from personal_bests"""
        )

        personal_bests = cursor.fetchall()

        personal_bests = dict(personal_bests)

        return personal_bests

    def upsert_personal_best(self, personal_best):
        cursor = self.database.get_cursor()

        cursor.execute(
            """INSERT OR REPLACE into personal_bests (distance, time) VALUES (?, ?)""",
            (personal_best.distance, personal_best.time)
        )

        self.connection.commit()

personal_best_repository = PersonalBestRepository(database)
