from sqlite3 import IntegrityError
from backend.database import Database

database = Database()

class TrainingRepository:
    def __init__(self, database):
        self.connection = database.connection

        self.database = database

    def create_training(self, training):
        cursor = self.database.get_cursor()

        try:
            cursor.execute(
                """INSERT INTO trainings (date, time, distance, RPE) VALUES (?, ?, ?, ?)""",
                (training.date, training.time, training.distance, training.RPE)
            )

            # self.cursor.lastrowid zwraca id ostatnio wstawionego wiersza
            new_training_id = cursor.lastrowid

            for task in training.tasks:
                cursor.execute(
                    """INSERT INTO training_tasks (training_id, description, task_distance, task_reps, task_target_time, task_break, average_segment_time) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (new_training_id, task.description, task.task_distance, task.task_reps, task.task_target_time, task.task_break, task.average_segment_time)
                )
        except Exception as e:
            # Cofamy wszystkie dokonane, niezapisane zmiany w bazie dancyh
            self.connection.rollback()

            # Sprawdziamy czy błąd który wystąpił to IntegrityError
            if isinstance(e, IntegrityError):
                raise ValueError(f"Training with id {training.id} already exists")
            # Przepusczamy błąd do warstwy która go wywyołała
            raise

        self.connection.commit()

        return new_training_id

    def get_all_trainings(self):
        cursor = self.database.get_cursor()

        cursor.execute(
            """SELECT * from trainings order by date desc"""
        )

        trainings = cursor.fetchall()

        return trainings

    def get_training_by_id(self, training_id):
        cursor = self.database.get_cursor()

        training = cursor.execute("""SELECT * from trainings where id = ?""", (training_id,)).fetchone()

        tasks = cursor.execute("""SELECT * from training_tasks where training_id = ?""", (training_id,)).fetchall()

        return training, tasks

    def delete_training(self, training_id):
        cursor = self.database.get_cursor()

        try:
            cursor.execute(
                """DELETE from training_tasks where training_id = ?""",
                (training_id,)
            )

            cursor.execute(
                """DELETE from trainings where id = ?""",
                (training_id,)
            )
        except Exception:
            # Cofamy wszystkie dokonane, niezapisane zmiany w bazie dancyh
            self.connection.rollback()

            # Przepusczamy błąd do warstwy która go wywyołała
            raise

        self.connection.commit()

    def update_training(self, training):
        cursor = self.database.get_cursor()

        try:
            cursor.execute(
                """UPDATE trainings SET date = ?, time = ?, distance = ?, RPE = ? WHERE id = ?""",
                (training.date, training.time, training.distance, training.RPE, training.id)
            )

            cursor.execute(
                """DELETE from training_tasks where training_id = ?""",
                (training.id,)
            )

            for task in training.tasks:
                cursor.execute(
                    """INSERT INTO training_tasks (training_id, description, task_distance, task_reps, task_target_time, task_break, average_segment_time) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (training.id, task.description, task.task_distance, task.task_reps, task.task_target_time, task.task_break, task.average_segment_time)
                )
        except Exception:
            # Cofamy wszystkie dokonane, niezapisane zmiany w bazie dancyh
            self.connection.rollback()

            # Przepusczamy błąd do warstwy która go wywyołała
            raise

        self.connection.commit()

    def get_all_trainings_with_tasks(self):
        cursor = self.database.get_cursor()

        cursor.execute(
            """SELECT * from trainings"""
        )

        trainings = cursor.fetchall()

        cursor.execute(
            """SELECT * from training_tasks"""
        )

        tasks = cursor.fetchall()

        tasks_by_training_id = {}

        for task in tasks:
            if task["training_id"] in tasks_by_training_id:
                tasks_by_training_id[task["training_id"]].append(task)
            else:
                tasks_by_training_id[task["training_id"]] = [task]

        trainings_with_tasks = []

        for training in trainings:
            training = dict(training)
            # Korzstamy z get w celu zabezpieczenia się przed KeyError
            training["tasks"] = tasks_by_training_id.get(training["id"], [])
            trainings_with_tasks.append(training)

        return trainings_with_tasks

training_repository = TrainingRepository(database)