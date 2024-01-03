import numpy as np
import matplotlib.pyplot as plt
from file_handler import read_json
from parser import parse_weights2dict
from scipy.spatial.distance import cdist


def spcs_method(data):
    #  Unpack algorithm settings and alternatives from input data
    algo_settings, alternatives = parse_weights2dict(data)

    aspiration_points = algo_settings[0]
    # norm_aspiration_points = normalize_points(aspiration_points)

    reference_points = algo_settings[1]
    # norm_reference_points = normalize_points(reference_points)

    # Step 1 - Delete dominated points
    minimize_criteria = {'cena': True, 'pojemnosc': False, 'predkosc_odczytu': False, 'predkosc_zapisu': False}
    dominance_filtered_alternatives = remove_dominated_points(alternatives, minimize=minimize_criteria)

    # Step 2 - Consider noise in input data
    perturbation_range = 0  # sample noise value,
    noisy_dominated_alternatives = add_perturbation(dominance_filtered_alternatives, perturbation_range)

    # Step 3 - Calculate Skeleton Curve and plot all points and curves
    skeleton_curve = construct_skeleton_curve(reference_points, aspiration_points)

    # Step 4 - Find projection of non-dominated alternatives set on the skeleton curves
    projected_points = find_projection(noisy_dominated_alternatives, skeleton_curve)

    # Step 5 - Find compromise point and value of scoring function for all non-dominated alternatives
    distances, score, compromise_point = scoring_function(projected_points, noisy_dominated_alternatives)

    comp_point_x = noisy_dominated_alternatives[compromise_point]['cena']
    comp_point_y = noisy_dominated_alternatives[compromise_point]['pojemnosc']
    compromise_point_cords = [comp_point_x, comp_point_y]

    # Step 6 - Plot all points and skeleton curves
    plot_curves_and_points(alternatives, noisy_dominated_alternatives, reference_points, aspiration_points,
                           skeleton_curve, compromise_point_cords)
    print("Distances:", distances)
    print("Score:", score)
    print("Best Alternative:", compromise_point)


def remove_dominated_points(alternatives, minimize=None):
    if len(alternatives) == 0:
        return alternatives

    if minimize is None:
        minimize = {key: True for key in next(iter(alternatives.values()))}

    dominated = {key: False for key in alternatives}
    for key_i, point_i in alternatives.items():
        for key_j, point_j in alternatives.items():
            if key_i != key_j:
                dominates_i = all(
                    (point_i[key] <= point_j[key] if minimize[key] else point_i[key] >= point_j[key])
                    for key in point_i
                )
                dominates_j = all(
                    (point_j[key] <= point_i[key] if minimize[key] else point_j[key] >= point_i[key])
                    for key in point_j
                )

                if dominates_i and not dominates_j:
                    dominated[key_i] = True
                    break

    return {key: point for key, point in alternatives.items() if not dominated[key]}


def add_perturbation(alternatives, perturbation_range):
    perturbed_alternatives = {}
    for key, point in alternatives.items():
        perturbation = {param: np.random.uniform(low=-perturbation_range, high=perturbation_range) for param in point}
        perturbed_alternatives[key] = {param: value + perturbation[param] for param, value in point.items()}
    return perturbed_alternatives


def construct_skeleton_curve(reference_points, aspiration_points):
    skeleton_curve = {}

    # Perform linear interpolation
    t = np.linspace(0, 1, 100)
    aspiration_x, aspiration_y = aspiration_points['cena-asp'], aspiration_points['pojemnosc-asp']
    reference_x, reference_y = reference_points['cena-ref'], reference_points['pojemnosc-ref']

    interp_x = np.interp(t, [0, 1], [aspiration_x, reference_x])
    interp_y = np.interp(t, [0, 1], [aspiration_y, reference_y])

    skeleton_curve[0] = {'interp_x': interp_x, 'interp_y': interp_y}

    return skeleton_curve


def plot_curves_and_points(alternatives, non_dominated_alternatives, reference_points, aspiration_points,
                           skeleton_curve, compromise_point):
    plt.figure(figsize=(10, 10))

    # Plot alternatives
    for key, value in alternatives.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Alternative {key}', color='grey')

    # Plot non dominated alternatives
    for key, value in non_dominated_alternatives.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Non-Dominated Alternative {key}', marker='o', color='red')

    # Plot reference points
    x = reference_points['cena-ref']
    y = reference_points['pojemnosc-ref']
    plt.scatter(x, y, label=f'Reference Point', marker='^', color='green', s=100)

    # Plot aspiration points
    x = aspiration_points['cena-asp']
    y = aspiration_points['pojemnosc-asp']
    plt.scatter(x, y, label=f'Aspiration Point', marker='^', color='blue', s=100)

    # Plot skeleton curves
    for i, curve_data in skeleton_curve.items():
        plt.plot(curve_data['interp_x'], curve_data['interp_y'], linestyle='--', label=f'Skeleton Curve')

    # Plot compromise point
    plt.scatter(compromise_point[0], compromise_point[1], label=f'Compromise Point', marker='x', color='yellow', s=100)

    plt.legend()
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Space')
    plt.title('SP-CS Result Diagram')
    plt.savefig('docs/spcs_result.png')
    plt.show()


def normalize_points(points):
    max_value = max(points.values())
    min_value = min(points.values())

    norm_points = {key: (value - min_value) / (max_value - min_value) for key, value in points.items()}

    return norm_points


def chebyshev_distance(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def find_projection(noisy_dominated_alternatives, skeleton_curve):
    projected_points = {}

    for key, curve_data in skeleton_curve.items():
        skeleton_x = curve_data['interp_x']
        skeleton_y = curve_data['interp_y']

        for alt_key, alt_value in noisy_dominated_alternatives.items():
            alt_x = alt_value['cena']
            alt_y = alt_value['pojemnosc']

            # Find the projection of the alternative onto the skeleton curve
            projection = np.argmin(
                [chebyshev_distance(alt_x, alt_y, skeleton_x[i], skeleton_y[i]) for i in range(len(skeleton_x))])

            # Calculate the coordinates of the projected point
            projected_x = skeleton_x[projection]
            projected_y = skeleton_y[projection]

            # Store the projected point
            projected_points[alt_key] = {'projected_x': projected_x, 'projected_y': projected_y}

    return projected_points


# Normalize from 1 to 0
def normalize(value, min_value, max_value):
    return 1 - (value - min_value) / (max_value - min_value)


def scoring_function(projected_points, non_dominated_points):
    distances = {}
    for key, proj_data in projected_points.items():
        proj_x = proj_data['projected_x']
        proj_y = proj_data['projected_y']

        alt_x = non_dominated_points[key]['cena']
        alt_y = non_dominated_points[key]['pojemnosc']
        # Calculate distance from alternative to the projected point on the curve
        distances[key] = cdist(np.array([[proj_x, proj_y]]), np.array([[alt_x, alt_y]]))

    # Znalezienie punktu kompromisowego (minimalnej wartości funkcji skoringowej)
    min_key = min(distances, key=lambda k: distances[k])
    compromise_point = min_key

    # Normalize the distances to range (0, 1)
    min_difference = min(distances.values())
    max_difference = max(distances.values())
    score = {
        alt_key: normalize(diff, min_difference, max_difference) for alt_key, diff in distances.items()
    }
    return distances, score, compromise_point


def main():
    file_path_new = 'example_data/data_spcs.json'
    data = read_json(file_path_new)

    spcs_method(data)


if __name__ == "__main__":
    main()
