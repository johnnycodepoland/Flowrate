import datetime
import math
from backend.models.training import Training

# Wykładnik intensywności
INTENSITY_EXPONENT = 3

# Waga gęstości
DENSITY_WEIGHT = 15

# Wykładnik gęstości
DENSITY_EXPONENT = 5

EXTERNAL_LOAD_MAXIMUM = 25000

INTERNAL_LOAD_MAXIMUM = 5000

def get_pb_speed(distance, personal_bests):
    distances = sorted(personal_bests)

    if distance in personal_bests:
        return distance / personal_bests[distance]

    if distance < distances[0]:
        return distances[0] / personal_bests[distances[0]]
    if distance > distances[-1]:
        return distances[-1] / personal_bests[distances[-1]]

    # Funkcja zip będzie nam za każdym razem, łączyć kolejne elementy listy, (50, 100);(100, 200) itd, w celu sprawdzenia czy distance jest między nimi
    for d1, d2 in zip(distances, distances[1:]):
        if d1 < distance < d2:
            # Liczymy prędkości dla każdej z dwóch wartośći z zip
            v1 = d1 / personal_bests[d1]

            v2 = d2 / personal_bests[d2]

            # A następnie liczmymy w którym momencie drogi od d1 do d2, leży distance
            location_between = (distance - d1) / (d2 - d1)

            # Wyliczamy ostateczną prędkość PB dla distance
            return v1 + (v2 - v1) * location_between

def get_segment_speed(segment):
    segment_average_time = get_average_time(segment)

    if segment_average_time is None or segment_average_time <= 0:
        return None

    if segment.distance is None or segment.distance <= 0:
        return None

    speed = segment.distance / segment_average_time

    return speed

def get_critical_speed(personal_bests):
    personal_best_400 = personal_bests.get(400)

    personal_best_200 = personal_bests.get(200)

    if personal_best_400 is None or personal_best_200 is None:
        return None

    if personal_best_400 <= 2 * personal_best_200:
        return None

    critical_speed = (400 - 200) / (personal_best_400 - personal_best_200)

    return critical_speed

def segment_intensity(segment, critical_speed):
    segment_speed = get_segment_speed(segment)

    if critical_speed is None or segment_speed is None:
        return None

    intensity  = segment_speed / critical_speed

    return intensity

def segment_reserve_usage(segment, critical_speed, personal_bests):
    segment_speed = get_segment_speed(segment)

    if segment_speed is None or critical_speed is None:
        return None

    pb_speed = get_pb_speed(segment.distance, personal_bests)

    reserve_usage = max(0, min((segment_speed - critical_speed) / (pb_speed - critical_speed), 1))

    return reserve_usage

def task_density(task):
    rep_time = 0

    if task.task_reps <= 0:
        return None

    for segment in task.segments:
        average_segment_time = get_average_time(segment)

        if average_segment_time is None:
            continue

        rep_time += average_segment_time

    if rep_time == 0:
        return None

    work = rep_time * task.task_reps

    breaks = task.task_break * (task.task_reps - 1)

    return work / (work + breaks)

def task_load(task, critical_speed, personal_bests):
    # Zadanie bez czasów nie daje obciążenia zewnętrznego
    d = task_density(task)

    if d is None:
        return 0

    # Obliczmy reapeat_factor który odpowiada za karę, za liczbę powtórzeń powyżej 1, które rozładowują naszą baterie
    repeat_factor = (task.task_reps - 1) / task.task_reps

    total_load = 0

    for segment in task.segments:
        I = segment_intensity(segment, critical_speed)

        X = segment_reserve_usage(segment, critical_speed, personal_bests)

        if I is None:
            continue

        segment_load = get_average_time(segment) * task.task_reps * I ** INTENSITY_EXPONENT * (1 + DENSITY_WEIGHT * d ** DENSITY_EXPONENT * X * repeat_factor)

        total_load += segment_load

    return total_load

def training_load(training, personal_bests):
    critical_speed = get_critical_speed(personal_bests)

    total_load = 0

    for task in training.tasks:
        total_load += task_load(task, critical_speed, personal_bests)

    return total_load

def session_rpe(training):
    return training.RPE * training.time

def get_average_time(segment):
    if segment.times is None or segment.times == []:
        return segment.average_time
    else:
        return sum(segment.times) / len(segment.times)

# Ta funkcja policzy nam jak duże znaczenie ma mieć ten trening przy obliczaniu ostatecznego obciążenia
def calculate_decay_weight(days_ago):
    # Stała zaniku
    decay_constant = 7

    # Korzystamy z wbudowanej w biblioteke math funkcji math.exp która oblicza nam funkcje wykładniczą e^x
    decay_weight =  math.exp(-days_ago / decay_constant)

    return decay_weight

# Ta funkcja podsumuje nam ważone obciążenie wszystkich treningów
def calculate_fatigue_sum(trainings_with_tasks, personal_bests):
    fatigue_sum = 0

    for training_dict in trainings_with_tasks:
        training_obj = Training(**training_dict)
        load = training_load(training_obj, personal_bests)
        days_ago = (datetime.date.today() - training_obj.date).days
        decay_weight = calculate_decay_weight(days_ago)
        training_fatigue = load * decay_weight
        fatigue_sum += training_fatigue

    return fatigue_sum

def calculate_rpe_sum(trainings_with_tasks):
    rpe_sum = 0

    for training_dict in trainings_with_tasks:
        training_obj = Training(**training_dict)
        load = session_rpe(training_obj)
        days_ago = (datetime.date.today() - training_obj.date).days
        decay_weight = calculate_decay_weight(days_ago)
        training_fatigue = load * decay_weight
        rpe_sum += training_fatigue

    return rpe_sum

def calculate_percentage_fatigue(trainings_with_tasks, personal_bests):
    fatigue_sum = calculate_fatigue_sum(trainings_with_tasks, personal_bests)

    rpe_sum = calculate_rpe_sum(trainings_with_tasks)

    # Korzystamy z wbudowanej w pythona funkcji min, która wybierze nam mniejszą z dwóch liczb, aby uniknąć 100 procentowego obciążenia
    external_percentage_fatigue = min(100, (fatigue_sum / EXTERNAL_LOAD_MAXIMUM) * 100)

    internal_percentage_fatigue = min(100, (rpe_sum / INTERNAL_LOAD_MAXIMUM) * 100)

    average_percentage_fatigue = (external_percentage_fatigue + internal_percentage_fatigue) / 2

    return average_percentage_fatigue, external_percentage_fatigue, internal_percentage_fatigue

