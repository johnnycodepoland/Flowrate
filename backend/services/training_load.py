import datetime
import math
from backend.models.training import Training

def get_average_time(segment):
    if segment.times is None:
        return segment.average_time
    else:
        return sum(segment.times) / len(segment.times)

def calculate_deviation(target_time, average_time):
    if target_time is None or average_time is None:
        return None

    if target_time == 0:
        return None

    # Obliczamy procentowe odychlenie od planowanego czasu, korzystając z max, które ograniczy nam deviation do 0
    deviation = max(0, (average_time - target_time) / target_time)

    return deviation

def calculate_average_deviation(tasks):
    if len(tasks) <= 0:
        return 0

    deviations = []

    for task in tasks:
        segments = task.segments

        for segment in segments:
            deviations.append(calculate_deviation(segment.target_time, get_average_time(segment)))

    deviations = [number for number in deviations if number is not None]

    if not deviations:
        return 0

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

    # Korzystamy w wbudowanej w pythona funkcji min, która wybierze nam mniejszą z dwóch liczb, aby uniknąć 100 procentowego obciążenia
    percentage_fatigue = min(100, (fatigue_sum / maximum_value) * 100)

    return percentage_fatigue

