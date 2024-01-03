import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from file_handler import read_json
from parser import parse_weights2dict
from sp_cs import remove_dominated_points


def reference_set_method(data):
    #  Unpack algorithm settings and alternatives from input data
    reference_points, alternatives = parse_weights2dict(data)

    # Unpack reference points set
    aspiration_points = reference_points[0]
    status_quo_points = reference_points[1]
    optimum_limit_points = reference_points[2]

    # Step 1 - Remove dominated points (Create Pareto Set)
    minimize_criteria = {'cena': True, 'pojemnosc': False, 'predkosc_odczytu': False, 'predkosc_zapisu': False}
    pareto_set = remove_dominated_points(alternatives, minimize=minimize_criteria)

    # Step 2 - Calc distance between points in Pareto Set and every point from every set in Reference Points Set
    distances = calculate_distance(aspiration_points, status_quo_points, optimum_limit_points, pareto_set)

    # Step 3 - Calc scoring based on the distances
    distances, score, best_alternative = scoring_function(distances)

    # Step 4 - Visualize results
    plot_results(alternatives, pareto_set, aspiration_points, status_quo_points, optimum_limit_points)

    print("Distances:", distances)
    print("Score:", score)
    print("Best Alternative:", best_alternative)

def calculate_distance(aspiration_points, status_quo_points, optimum_limit_points, alternatives):
    distances = {}

    for ref_key, ref_value in aspiration_points.items():
        ref_x = aspiration_points["cena-asp"]
        ref_y = aspiration_points["pojemnosc-asp"]

        distances_of_set = {}
        for alt_key, alt_value in alternatives.items():
            alt_x = alt_value['cena']
            alt_y = alt_value['pojemnosc']

            # calculate the distance between reference point and given alternative
            # dist = euclidean_distance(alt_x, alt_y, ref_x, ref_y)
            dist = distance.euclidean((alt_x, alt_y), (ref_x, ref_y))
            # Save this distance in set of dictionaries
            distances_of_set[alt_key] = [dist]
    distances["aspiration"] = distances_of_set

    for ref_key, ref_value in status_quo_points.items():
        ref_x = status_quo_points["cena-ref"]
        ref_y = status_quo_points["pojemnosc-ref"]

        distances_of_set = {}
        for alt_key, alt_value in alternatives.items():
            alt_x = alt_value['cena']
            alt_y = alt_value['pojemnosc']

            # calculate the distance between reference point and given alternative
            dist = distance.euclidean((alt_x, alt_y), (ref_x, ref_y))
            # Save this distance in set of dictionaries
            distances_of_set[alt_key] = [dist]
    distances["status_quo"] = distances_of_set

    for ref_key, ref_value in optimum_limit_points.items():
        ref_x = optimum_limit_points["cena-gran"]
        ref_y = optimum_limit_points["pojemnosc-gran"]

        distances_of_set = {}
        for alt_key, alt_value in alternatives.items():
            alt_x = alt_value['cena']
            alt_y = alt_value['pojemnosc']

            # calculate the distance between reference point and given alternative
            dist = distance.euclidean((alt_x, alt_y), (ref_x, ref_y))
            # Save this distance in set of dictionaries
            distances_of_set[alt_key] = [dist]
    distances["optimum_limit"] = distances_of_set

    return distances


def plot_results(alternatives, pareto_set, aspiration_points, status_quo_points, optimum_limit_points):
    plt.figure(figsize=(10, 10))

    # Plot alternatives
    for key, value in alternatives.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Alternative {key}',  color='grey')

    # Plot non dominated alternatives
    for key, value in pareto_set.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Pareto Set Alternative {key}', marker='o', color='red')

    # Plot aspiration points
    x = aspiration_points['cena-asp']
    y = aspiration_points['pojemnosc-asp']
    plt.scatter(x, y, label=f'Aspiration Point', marker='^', color='blue', s=100)

    # Plot Status Quo points
    # x = status_quo_points['cena-ref']
    # y = status_quo_points['pojemnosc-ref']
    # plt.scatter(x, y, label=f'Status Quo Point', marker='^', color='green', s=100)

    # Plot optimum limit points
    x = optimum_limit_points['cena-gran']
    y = optimum_limit_points['pojemnosc-gran']
    plt.scatter(x, y, label=f'Optimum Limit Point', marker='^', color='green', s=100)

    plt.legend()
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Space')
    plt.title('RSM Results Diagram')
    plt.savefig('docs/rsm_result.png')
    plt.show()

# Normalize to range (1, 0)
def normalize(value, min_value, max_value):
    return 1 - (value - min_value) / (max_value - min_value)

def scoring_function(distances):
    status_quo_distances = distances.get('status_quo', {})
    aspiration_distances = distances.get('aspiration', {})

    # Calculating the difference for each alternative
    difference_scores = {}
    for alt_key in status_quo_distances:
        status_quo_distance = status_quo_distances[alt_key][0]
        aspiration_distance = aspiration_distances.get(alt_key, [0])[0]
        difference = abs(status_quo_distance - aspiration_distance)
        difference_scores[alt_key] = difference

    # Normalize the difference_scores to range (0, 1)
    min_difference = min(difference_scores.values())
    max_difference = max(difference_scores.values())
    score = {
        alt_key: normalize(diff, min_difference, max_difference) for alt_key, diff in difference_scores.items()
    }

    # Selecting the alternative with the maximum difference
    best_alternative = min(difference_scores, key=difference_scores.get)

    return difference_scores, score, best_alternative


def main():
    file_path_new = 'example_data/data_rsm.json'
    data = read_json(file_path_new)

    reference_set_method(data)


if __name__ == "__main__":
    main()
