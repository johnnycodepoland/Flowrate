import datetime
import math

from backend.models.training import Training


def calculate_deviation(task_target_time, average_segment_time):
    # Obliczamy procentowe odychlenie od planowanego czasu
    deviation = (average_segment_time - task_target_time) / task_target_time

    return deviation

def calculate_average_deviation(tasks):
    if len(tasks) <= 0:
        return 0

    deviations = []

    for task in tasks:
        deviations.append(calculate_deviation(task.task_target_time, task.average_segment_time))

    average_deviation = sum(deviations) / len(deviations)

    return average_deviation

def calculate_final_load(RPE, time, average_deviation):
    base_load = RPE * time

    final_load = base_load * (1 + average_deviation)

    return final_load

def calculate_training_load(training):
    # Obliczamy średnie obciążenie
    average_deviation = calculate_average_deviation(training.tasks)

    # Obliczamy końcowe obciążenie
    final_load = calculate_final_load(training.RPE, training.time, average_deviation)

    return final_load

# Ta funkcja policzy nam jak duże znaczenie ma mieć ten trening przy obliczaniu ostatecznego obciążenia
def calculate_decay_weight(days_ago):
    # Stała zaniku
    decay_constant = 7

    # Korzystamy z wbudowanej w biblioteke math funkcji math.exp która oblicza nam funkcje wykładniczą e^x
    decay_weight =  math.exp(-days_ago / decay_constant)

    return decay_weight

# Ta funkcja podsumuje nam ważone obciążenie wszystkich treningów
def calculate_fatigue_sum(trainings_with_tasks):
    fatigue_sum = 0

    for training_dict in trainings_with_tasks:
        training_obj = Training(**training_dict)
        training_load = calculate_training_load(training_obj)
        days_ago = (datetime.date.today() - training_obj.date).days
        decay_weight = calculate_decay_weight(days_ago)
        training_fatigue = training_load * decay_weight
        fatigue_sum += training_fatigue

    return fatigue_sum

def calculate_percentage_fatigue(trainings_with_tasks):
    maximum_value = 6000
    fatigue_sum = calculate_fatigue_sum(trainings_with_tasks)

    # Korzystamy w wbudowanej w pythona funkcji min, która wybierze nam mniejszą z dwóch liczb któ^
    percentage_fatigue = min(100, (fatigue_sum / maximum_value) * 100)

    return percentage_fatigue

