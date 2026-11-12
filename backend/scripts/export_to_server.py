# JEDNORAZOWY: uruchomiony 12.11.2026, ponowne uruchomienie = duplikaty.
import httpx
import sqlite3
import json
from getpass import getpass

SERVER_URL = "https://flowrate-production.up.railway.app"
LOCAL_USER_ID = 2

email = input("E-mail: ")

password = getpass("Hasło: ")

response = httpx.post(f"{SERVER_URL}/auth/login", json={"email": email, "password": password})

if response.status_code != 200:
    print(f"Wystąpił błąd: {response.status_code}")
    exit()

access_token = response.json()["access_token"]

print("Zalogowano")

# Read only connection
conn = sqlite3.connect("file:flowrate.db?mode=ro", uri=True)

conn.row_factory = sqlite3.Row

trainings = conn.execute(
    """SELECT * from trainings where user_id = ? ORDER BY date""",
    (LOCAL_USER_ID,)
).fetchall()

tasks = conn.execute(
    """SELECT * from training_tasks ORDER BY id""",
).fetchall()

task_segments = conn.execute(
    """SELECT * from task_segments ORDER BY position"""
).fetchall()

segments_by_task_id = {}

tasks_by_training_id = {}

for segment in task_segments:
    segment = dict(segment)

    if segment["times"]:
        segment["times"] = json.loads(segment["times"])

    if segment["task_id"] in segments_by_task_id:
        segments_by_task_id[segment["task_id"]].append(segment)
    else:
        segments_by_task_id[segment["task_id"]] = [segment]

for task in tasks:
    task = dict(task)
    task["segments"] = segments_by_task_id.get(task["id"], [])
    if task["training_id"] in tasks_by_training_id:
        tasks_by_training_id[task["training_id"]].append(task)
    else:
        tasks_by_training_id[task["training_id"]] = [task]

trainings_with_tasks = []

for training in trainings:
    training = dict(training)
    training["tasks"] = tasks_by_training_id.get(training["id"], [])
    trainings_with_tasks.append(training)

print(len(trainings_with_tasks))

answear = input(f"Wysłać {len(trainings_with_tasks)} treningów na konto {email}? (t/n)")

if answear != "t":
    exit()

for training in trainings_with_tasks:
    response = httpx.post(f"{SERVER_URL}/trainings", json=training, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code != 200:
        print(training["date"], response.status_code, response.text)
    else:
        print(training["date"], response.status_code)

pbs = conn.execute("SELECT distance, time FROM personal_bests WHERE user_id = ?", (LOCAL_USER_ID,)).fetchall()

for pb in pbs:
    response = httpx.put(f"{SERVER_URL}/personal-bests", json={"distance": pb["distance"], "time": pb["time"]}, headers={"Authorization": f"Bearer {access_token}"})
    print(pb["distance"], response.status_code)

conn.close()