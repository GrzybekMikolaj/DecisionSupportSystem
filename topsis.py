import enum
import math
from file_handler import read_json
from parse import parse_weights2dict


def topsis(data):
    algo_settings, alternatives = parse_weights2dict(data)
    # print("YOOOOOOOOOOOOOO")
    # print(algo_settings)
    # print(alternatives)
    
    normalized_data = normalize_data(alternatives)

    weighted_normalized_matrix = calculate_weighted_normalized_matrix(normalized_data, algo_settings)

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
    rankings = map(lambda x: {x[0]: x[1]}, rankings)
    rankings = enumerate(rankings)
    rankings = dict(rankings)
    return rankings

# file_path = 'static/data.json'
# data = read_json(file_path)

# file_path_new = 'static/data20rand.json'
# data_new = read_json(file_path_new)
# result = topsis(data_new)

# print("Rankings:")
# for rank, score in result:
#     rounded_score = round(score, 3)
#     print(f"{rank}: {rounded_score}") 