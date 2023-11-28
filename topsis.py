import json
import math

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def topsis(data):
    weights = {key: value for key, value in data.get("weights", {}).items() if value != 0 and isinstance(value, (int, float))}

    if not weights:
        print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
        return

    numeric_parameters = ["cena", "pojemnosc", "predkosc_odczytu", "predkosc_zapisu"]

    alternatives = {
        key: {
            param: value for param, value in data[key].items() if param in numeric_parameters and isinstance(value, (int, float))
        } for key in data if key not in ["weights"]
    }

    if not alternatives:
        print("Brak prawidłowych danych. Algorytm nie może być wykonany.")
        return
    
    normalized_data = normalize_data(alternatives)

    weighted_normalized_matrix = calculate_weighted_normalized_matrix(normalized_data, weights)

    ideal_positive, ideal_negative = calculate_ideal_solutions(weighted_normalized_matrix)

    separation_measures = calculate_separation_measures(weighted_normalized_matrix, ideal_positive, ideal_negative)

    rankings = rank_alternatives(separation_measures)

    return rankings

def normalize_data(alternatives):
    normalized_data = {}
    for criterion in alternatives["M1"]:
        temp_sum = 0
        if all(criterion in alternative for alternative in alternatives.values()):
            for alternative in alternatives.values():
                temp_sum += pow(alternative[criterion], 2)
            sqrt_of_pow = math.sqrt(temp_sum)

            for key in alternatives:
                if criterion not in normalized_data:
                    normalized_data[criterion] = {}
                if criterion in alternatives[key]:
                    if criterion == "cena":
                        normalized_data[criterion][key] = alternatives[key][criterion] / sqrt_of_pow
                    else:
                        normalized_data[criterion][key] = 1 - alternatives[key][criterion] / sqrt_of_pow
    return normalized_data
def calculate_weighted_normalized_matrix(normalized_data, weights):
    weighted_normalized_matrix = {}

    for key in normalized_data:
        if key not in weighted_normalized_matrix:
            weighted_normalized_matrix[key] = {}
        for alternative in normalized_data[key]:
            weighted_normalized_matrix[key][alternative] = normalized_data[key][alternative] * weights[key]

    return weighted_normalized_matrix

def calculate_ideal_solutions(weighted_normalized_matrix):
    ideal_positive = {}
    ideal_negative = {}

    for key in weighted_normalized_matrix:
        ideal_positive[key] = max(weighted_normalized_matrix[key].values())
        ideal_negative[key] = min(weighted_normalized_matrix[key].values())

    return ideal_positive, ideal_negative

def calculate_separation_measures(weighted_normalized_matrix, ideal_positive, ideal_negative):
    separation_measures = {}

    for alternative in weighted_normalized_matrix[list(weighted_normalized_matrix.keys())[0]]:
        positive_distance = sum((weighted_normalized_matrix[key][alternative] - ideal_negative[key]) ** 2 for key in weighted_normalized_matrix)
        negative_distance = sum((weighted_normalized_matrix[key][alternative] - ideal_positive[key]) ** 2 for key in weighted_normalized_matrix)

        separation_measures[alternative] = negative_distance / (positive_distance + negative_distance)

    return separation_measures

def rank_alternatives(separation_measures):
    rankings = sorted(separation_measures.items(), key=lambda x: x[1], reverse=True)
    return rankings

file_path = 'static/data.json'

data = read_json(file_path)

result = topsis(data)

print("Rankings:")
for rank, score in result:
    rounded_score = round(score, 3)
    print(f"{rank}: {rounded_score}")