import numpy as np
import matplotlib.pyplot as plt
from file_handler import read_json
from parser import parse_weights2dict

def spcsMethod():
    # Sample data
    alt_size = 20
    num_of_parameters = 2
    np.random.seed(11)
    alt_params = np.random.rand(alt_size, num_of_parameters)
    alternatives = {}

    for i in range(0, alt_size):
        alternatives[i] = alt_params[i]
    # print(alternatives)
    # print(alt_params)
        
    # Step 1 - Delete dominated points
    dominance_filtered_alternatives = remove_dominated_points(alternatives)
    # print("\n Non Dominated")
    # print(dominance_filtered_alternatives)

    # TODO: Extract reference and aspiration points from fucntion parameter
    # Punkt referencyjny to trochę gorszy niż idealny ale wciąż akceptowalny
    # np. idealna cena to 100pln ale referecyjny będzie 130pln
    # reference_points = np.array([[0.88, 0.79], [0.88, 0.79]]) # debug only
    # # Punkt aspiracji to idealna wartość do której ma dążyć
    # aspiration_points = np.array([[0.95, 0.95], [0.95, 0.95]])

    # Przykład użycia
    aspiration_points = {}
    reference_points = {}
    # aspiration_points[0] = np.array([[0.95, 0.95]])
    # reference_points[0] = np.array([[0.88, 0.79]])
    
    for i in range(0, alt_size):
        aspiration_points[i] = np.random.rand(num_of_parameters)
        reference_points[i] = np.random.rand(num_of_parameters)
    # print(reference_points)
    # print(aspiration_points)


    # Step 2 - Consider noise in input data 
    perturbation_range = 0.01  # sample noise value, 
    noisy_dominated_alternatives = add_perturbation(dominance_filtered_alternatives, perturbation_range)
    # print(alternatives)
    # print("\n")
    # print(noisy_alternatives)

    # Step 3 - Calculate Skeleton Curve
    skeleton_curve = construct_skeleton_curve(aspiration_points, reference_points)
    print(skeleton_curve)
    plot_skeleton_curve(alternatives, noisy_dominated_alternatives, reference_points, aspiration_points, skeleton_curve)



def remove_dominated_points(alternatives):
    if len(alternatives) == 0:
        return alternatives

    dominated = {key: False for key in alternatives}
    for key_i, point_i in alternatives.items():
        for key_j, point_j in alternatives.items():
            if key_i != key_j and all(point_i <= point_j):
                dominated[key_i] = True
                break

    return {key: point for key, point in alternatives.items() if not dominated[key]}


def add_perturbation(alternatives, perturbation_range):
    perturbed_alternatives = {}
    for key, point in alternatives.items():
        perturbation = np.random.uniform(low=-perturbation_range, high=perturbation_range, size=len(point))
        perturbed_alternatives[key] = point + perturbation
    return perturbed_alternatives


def construct_skeleton_curve(aspiration_points, reference_points):
    skeleton_curve = {}
    
    for key in aspiration_points:
        t_values = np.linspace(0, 1, len(aspiration_points[key]))
        curve_points = []

        for t, ai, ri in zip(t_values, aspiration_points[key], reference_points[key]):
            interpolated_point = (1 - t) * ai + t * ri
            curve_points.append(interpolated_point)

        skeleton_curve[key] = np.array(curve_points)

    return skeleton_curve

def plot_skeleton_curve(alternatives, noisy_dominated_alternatives, reference_points, aspiration_points, skeleton_curve):
    # Wizualizacja krzywej szkieletowej dla słownikowej postaci danych
    plt.figure(figsize=(8, 6))

    # for key, value in alternatives.items():
    #     plt.scatter(value[0], value[1], label=f'Alternative {key}', alpha=0.7)

    for key, value in noisy_dominated_alternatives.items():
        plt.scatter(value[0], value[1], label=f'Non-dominated Alternative {key}', marker='x', color='red', s=100)

    #  Visualize reference and aspitration points
    plt.scatter([value[0] for key, value in reference_points.items()], [value[1] for key, value in reference_points.items()], label='Reference Points', marker='s', color='green', s=100)
    plt.scatter([value[0] for key, value in aspiration_points.items()], [value[1] for key, value in aspiration_points.items()], label='Aspiration Points', marker='s', color='blue', s=100)
    
    # Dodanie krzywych szkieletowych dla wszystkich punktów
    xs, ys = zip(*skeleton_curve.values())
    keyes = skeleton_curve.keys() 
    points = []
    for key, x, y in zip(keyes, xs, ys):
        points.append([x, y, key])
        # plt.scatter(x, y, label=f'Skeleton Curve ({key})', linestyle='dashed', alpha=0.7)

    print(points)        
    if points:
        plt.plot(points[0], points[1], label=f'Skeleton Curve ({points[2]})', linestyle='dashed', alpha=0.7)
    else:
        print("Brak punktów")

    plt.legend()
    plt.xlabel('Parameter 1')
    plt.ylabel('Parameter 2')
    plt.title('Skeleton Curve Construction for Dictionary Data')
    plt.show()




spcsMethod()


# file_path_new = 'static/data20rand.json'
# data_new = read_json(file_path_new)
# result = spcsMethod(data_new)

# print("Rankings:")
# print(result)
# for rank, score in result:
#     rounded_score = round(score, 3)
#     print(f"{rank}: {rounded_score}") 













# # Krok 6: Znalezienie rzutu punktu F(u) na krzywej łamanej przy użyciu metryki Czebyszewa
# def find_projection(point, curve):
#     distances = np.max(np.abs(curve - point), axis=1)
#     closest_index = np.argmin(distances)
#     return curve[closest_index]

# # Przykładowy punkt do znalezienia rzutu
# sample_point = np.array([0.5, 0.5])
# projection = find_projection(sample_point, skeleton_curve)

# # Krok 7: Identyfikacja punktu kompromisowego
# compromise_point = remove_dominated_points(np.vstack((dominance_filtered_alternatives, projection.reshape(1, -1))))

# # Krok 8: Ocena wartości funkcji skoringowej
# scoring_function_value = np.sum(np.abs(compromise_point - sample_point))

# # Krok 9: Analiza wyników i ewaluacja
# print(f'Projection of {sample_point} onto the skeleton curve: {projection}')
# print(f'Compromise Point: {compromise_point}')
# print(f'Scoring Function Value: {scoring_function_value}')

# # Wizualizacja punktu kompromisowego
# plt.scatter(alternatives[:, 0], alternatives[:, 1], label='Alternatives')
# plt.scatter(dominance_filtered_alternatives[:, 0], dominance_filtered_alternatives[:, 1], label='Non-dominated Alternatives')
# plt.scatter(reference_points[:, 0], reference_points[:, 1], label='Reference Points', marker='s', color='red')
# plt.scatter(aspiration_points[:, 0], aspiration_points[:, 1], label='Aspiration Points', marker='s', color='green')
# plt.plot(skeleton_curve[:, 0], skeleton_curve[:, 1], label='Skeleton Curve', linestyle='dashed', color='orange')
# plt.scatter(projection[0], projection[1], label='Projection', marker='o', color='purple')
# plt.scatter(compromise_point[:, 0], compromise_point[:, 1], label='Compromise Point', marker='x', color='black')
# plt.scatter(sample_point[0], sample_point[1], label='Sample Point', marker='*', color='blue')
# plt.legend()
# plt.xlabel('Parameter 1')
# plt.ylabel('Parameter 2')
# plt.title('Compromise Point Identification')
# plt.show()
