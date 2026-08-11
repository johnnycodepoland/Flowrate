from sqlite3 import IntegrityError
from backend.database import Database

database = Database()

class TrainingRepository:
    def __init__(self, cursor, connection):
        self.cursor = cursor

        self.connection = connection

    def create_training(self, training):
        try:
            self.cursor.execute(
                """INSERT INTO trainings (id, date, time, distance, RPE) VALUES (?, ?, ?, ?, ?)""",
                (training.id, training.date, training.time, training.distance, training.RPE)
            )

            for task in training.tasks:
                self.cursor.execute(
                    """INSERT INTO training_tasks (training_id, description, task_distance, task_reps, task_target_time, task_break, average_segment_time) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (training.id, task.description, task.task_distance, task.task_reps, task.task_target_time, task.task_break, task.average_segment_time)
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

    def get_all_trainings(self):
        self.cursor.execute(
            """SELECT * from trainings"""
        )

        trainings = self.cursor.fetchall()

        return trainings

    def get_training_by_id(self, training_id):
        training = self.cursor.execute("""SELECT * from trainings where id = ?""", (training_id,)).fetchone()

        tasks = self.cursor.execute("""SELECT * from training_tasks where training_id = ?""", (training_id,)).fetchall()

        return training, tasks

    def delete_training(self, training_id):
        try:
            self.cursor.execute(
                """DELETE from training_tasks where training_id = ?""",
                (training_id,)
            )

            self.cursor.execute(
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
        try:
            self.cursor.execute(
                """UPDATE trainings SET date = ?, time = ?, distance = ?, RPE = ? WHERE id = ?""",
                (training.date, training.time, training.distance, training.RPE, training.id)
            )

            self.cursor.execute(
                """DELETE from training_tasks where training_id = ?""",
                (training.id,)
            )

            for task in training.tasks:
                self.cursor.execute(
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
        self.cursor.execute(
            """SELECT * from trainings"""
        )

        trainings = self.cursor.fetchall()

        self.cursor.execute(
            """SELECT * from training_tasks"""
        )

        tasks = self.cursor.fetchall()

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

training_repository = TrainingRepository(database.cursor, database.connection)