import sqlite3

DB_PATH = "flowrate_dev.db"
USER_ID = 1

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute(
    # user_id musi znajdować się w tabeli users za co odpowiada INTEGER REFERENCES users(id)
    """ALTER TABLE trainings ADD COLUMN user_id INTEGER REFERENCES users(id)""")

cursor.execute(
    """UPDATE trainings SET user_id = ?""",
    (USER_ID,)
)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_bests_new (
        user_id INTEGER REFERENCES users(id),
        distance INTEGER,
        time REAL,
        PRIMARY KEY (user_id, distance))
        """)

cursor.execute(
    """INSERT INTO personal_bests_new (user_id, distance, time) SELECT ?, distance, time FROM personal_bests""",
    (USER_ID,)
)

cursor.execute(
    """DROP TABLE personal_bests"""
)

cursor.execute(
    """ALTER TABLE personal_bests_new RENAME TO personal_bests"""
)

connection.commit()

connection.close()