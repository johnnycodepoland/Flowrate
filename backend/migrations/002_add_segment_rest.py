import sqlite3
import os

DB_PATH = os.environ.get("FLOWRATE_DB", default="flowrate_dev.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

table_info = cursor.execute("PRAGMA table_info(task_segments)").fetchall()

columns = set()

for row in table_info:
    columns.add(row[1])

if "rest_after" not in columns:
    cursor.execute("ALTER TABLE task_segments ADD COLUMN rest_after REAL")

if "send_off" not in columns:
    cursor.execute("ALTER TABLE task_segments ADD COLUMN send_off REAL")

connection.commit()

connection.close()