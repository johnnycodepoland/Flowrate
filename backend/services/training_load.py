import datetime
import math
from backend.models.training import Training

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
    personal_best_400 = personal_bests[400]

    personal_best_200 = personal_bests[200]

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

def get_average_time(segment):
    if segment.times is None or segment.times == []:
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

    # Korzystamy z wbudowanej w pythona funkcji min, która wybierze nam mniejszą z dwóch liczb, aby uniknąć 100 procentowego obciążenia
    percentage_fatigue = min(100, (fatigue_sum / maximum_value) * 100)

    return percentage_fatigue

