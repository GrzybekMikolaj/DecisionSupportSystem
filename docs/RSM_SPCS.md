# Implementacja i analiza wyników algorytmu Rerence Set Method
*Mikołaj Grzybek*

<!-- TOC -->
* [Implementacja i analiza wyników algorytmu Rerence Set Method](#implementacja-i-analiza-wyników-algorytmu-rerence-set-method)
  * [Zbiór danych](#zbiór-danych)
  * [Algorytm RSM](#algorytm-rsm)
  * [Algorytm SP-CS](#algorytm-sp-cs)
    * [Analiza wyników](#analiza-wyników)
  * [Implementacja algorytmów](#implementacja-algorytmów)
    * [Reference Set Method](#reference-set-method-)
    * [Safety Principal Compromise Selection](#safety-principal-compromise-selection)
<!-- TOC -->


## Zbiór danych
Analizie zostały podjęte dyski zewnętrzne. Na potrzeby wyboru najlepszego, 
spisano parametry sześciu różnych dysków, takie jak cena, pojemność, prędkość odczytu i zapisu. 


| id | marka               | cena | pojemnosc | prędkosc-odczytu | predkosc-zapisu |
|----|---------------------|------|-----------|------------------|-----------------|
| M1 | lexar-sl200         | 300  | 1000      | 550              | 400             |
| M2 | adata-elitr-se880   | 300  | 1000      | 2000             | 2000            |
| M3 | samsungh-t7         | 405  | 1000      | 1050             | 1000            |
| M4 | samsung-t7          | 420  | 1000      | 1050             | 1000            |
| M5 | sandisk-extreme     | 400  | 1000      | 1050             | 1000            |
| M6 | sandisk-extreme-pro | 625  | 1000      | 2000             | 2000            |

Przyjęto poniższe ustawienia parametrów algorytmów

SP-CS

| Cena Aspiracja | Cena Status Quo | Pojemność Aspiracja | Pojemność  Status Quo | Prędkość Odczytu Aspiracja | Prędkość Odczytu Status Quo | Prędkość Zapisu Aspiracja | Prędkość Zapisu Status Quo |
|----------------|-----------------|---------------------|-----------------------|----------------------------|-----------------------------|---------------------------|----------------------------|
| 200            | 400             | 1500                | 500                   | 3500                       | 1500                        | 2500                      | 1500                       |

RSM

| Cena Aspiracja | Cena Granica Optymalności | Pojemność Aspiracja | Pojemność  Granica Optymalności | Prędkość Odczytu Aspiracja | Prędkość Odczytu Granica Optymalności | Prędkość Zapisu Aspiracja | Prędkość Zapisu Granica Optymalności |
|----------------|---------------------------|---------------------|---------------------------------|----------------------------|---------------------------------------|---------------------------|--------------------------------------|
| 200            | 400             | 1500                | 500                   | 3500                       | 1500                        | 2500                      | 1500                       |

## Algorytm RSM

Wynikiem działania tego algorytmu przedstawiono poniżej:

| Pozycja | Nazwa | Wynik |
|---------|-------|-------|
| 1       | M1    | 1.0   |
| 2       | M4    | 0.29  |
| 3       | M6    | 0     |

<br>

![](/home/mikolaj/DecisionSupportSystem/docs/rsm_result.png)
<br> _Rys.1 Wizualizacja alternatyw i punktów referencyjnych w metodzie RSM_

## Algorytm SP-CS

Wynikiem działania tego algorytmu przedstawiono poniżej:

| Pozycja | Nazwa | Wynik |
|---------|-------|-------|
| 1       | M1    | 1.0   |
| 2       | M4    | 0.64  |
| 3       | M6    | 0.0   |

<br>

![](/home/mikolaj/DecisionSupportSystem/docs/spcs_result.png)
<br> _Rys.2 Wizualizacja alternatyw i punktów referencyjnych w metodzie SP-CS_

### Analiza wyników
Dla obu metod zastosowano tą samą pozycję punktu aspiracji oraz statusu qou(granicy optymalności).
Dzięki temu możemy użyć wyników do oceny metod niezależnie od postawionego im problemu.

Same wyniki są znormalizowaną do przedziału [0, 1] odległością zdefiniowaną w dla obu metod na różny sposób.

W obu metodach zastosowano tą samą metodę wyznaczenia zbioru Pareto. W związku z tym punkty M2, M3 i M5,
zostały uznane jako zdominowane.



## Implementacja algorytmów

### Reference Set Method 

```python
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
        plt.scatter(x, y, label=f'Pareto Set Alternative {key}', marker='x', color='red')

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
    plt.scatter(x, y, label=f'Optimum Limit Point', marker='^', color='purple', s=100)

    plt.legend()
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Space')
    plt.title('RMS Results Diagram')
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
 
```

###  Safety Principal Compromise Selection

```python
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
    plt.figure(figsize=(8, 6))

    # Plot alternatives
    for key, value in alternatives.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Alternative {key}', alpha=0.7, color='grey')

    # Plot non dominated alternatives
    for key, value in non_dominated_alternatives.items():
        x = value['cena']
        y = value['pojemnosc']
        plt.scatter(x, y, label=f'Non-Dominated Alternative {key}', marker='x', color='red', alpha=0.7)

    # Plot reference points
    x = reference_points['cena-ref']
    y = reference_points['pojemnosc-ref']
    plt.scatter(x, y, label=f'Reference Point', marker='s', color='green', s=100)

    # Plot aspiration points
    x = aspiration_points['cena-asp']
    y = aspiration_points['pojemnosc-asp']
    plt.scatter(x, y, label=f'Aspiration Point', marker='^', color='blue', s=100)

    # Plot skeleton curves
    for i, curve_data in skeleton_curve.items():
        plt.plot(curve_data['interp_x'], curve_data['interp_y'], linestyle='--', label=f'Skeleton Curve', alpha=0.5)

    # Plot compromise point
    plt.scatter(compromise_point[0], compromise_point[1], label=f'Compromise Point', marker='^', color='red', s=100)

    plt.legend()
    plt.grid()
    plt.xlabel('Price')
    plt.ylabel('Space')
    plt.title('Skeleton Curves Diagram')
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

```