from backend.database import Database

database = Database()

class UserRepository:
    def __init__(self, database):
        self.connection = database.connection

        self.database = database

    def get_user_by_email(self, email):
        cursor = self.database.get_cursor()

        cursor.execute(
            """SELECT * from users WHERE email = ?""",
            (email,)
        )

        user = cursor.fetchone()

        return user

    def create_user(self, email, password_hash):
        cursor = self.database.get_cursor()

        cursor.execute(
            """INSERT into users (email, password_hash) VALUES (?, ?)""",
            (email, password_hash)
        )

        self.connection.commit()

        return cursor.lastrowid

user_repository = UserRepository(database)
