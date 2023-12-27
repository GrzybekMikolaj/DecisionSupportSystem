import numpy as np
import matplotlib.pyplot as plt

# Krok 1: Utworzenie zbioru zawierającego 20 alternatyw z dwoma parametrami wybranymi losowo
np.random.seed(11)
alternatives = np.random.rand(20, 2)

def remove_dominated_points(points):
    if len(points) == 0:
        return points

    dominated = [False] * len(points)
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j and all(points[i] <= points[j]):
                dominated[i] = True
                break

    return points[~np.array(dominated)]

dominance_filtered_alternatives = remove_dominated_points(alternatives)

# Krok 3: Zdefiniowanie punktów odniesienia i punktów aspiracji
reference_points = np.array([[0.8, 0.65], [0.75, 0.7]]) # debug only
# print(reference_points)

# Punkt aspiracji to idealna wartość do której ma dążyć
aspiration_points = np.array([[0.85, 0.75], [0.9, 0.5]])

# Krok 4: Uwzględnienie zakłóceń lub niepewności
perturbation = np.random.uniform(low=-0.05, high=0.05, size=alternatives.shape)
noisy_alternatives = alternatives + perturbation

# Krok 5: Konstrukcja krzywych szkieletowych
def construct_skeleton_curve(aspiration, reference):
    t_values = np.linspace(0, 1, len(aspiration))
    skeleton_curve = []
    for t, ai, ri in zip(t_values, aspiration, reference):
        interpolated_point = (1 - t) * ai + t * ri
        skeleton_curve.append(interpolated_point)
    return np.array(skeleton_curve)

skeleton_curve = construct_skeleton_curve(aspiration_points, reference_points)

# Wizualizacja krzywej szkieletowej
plt.scatter(alternatives[:, 0], alternatives[:, 1], label='Alternatives')
plt.scatter(dominance_filtered_alternatives[:, 0], dominance_filtered_alternatives[:, 1], label='Non-dominated Alternatives')
plt.scatter(reference_points[:, 0], reference_points[:, 1], label='Reference Points', marker='s', color='red')
plt.scatter(aspiration_points[:, 0], aspiration_points[:, 1], label='Aspiration Points', marker='s', color='green')
plt.plot(skeleton_curve[:, 0], skeleton_curve[:, 1], label='Skeleton Curve', linestyle='dashed', color='orange')
plt.legend()
plt.xlabel('Parameter 1')
plt.ylabel('Parameter 2')
plt.title('Skeleton Curve Construction')
plt.show()

# Krok 6: Znalezienie rzutu punktu F(u) na krzywej łamanej przy użyciu metryki Czebyszewa
def find_projection(point, curve):
    distances = np.max(np.abs(curve - point), axis=1)
    closest_index = np.argmin(distances)
    return curve[closest_index]

# Przykładowy punkt do znalezienia rzutu
sample_point = np.array([0.5, 0.5])
projection = find_projection(sample_point, skeleton_curve)

# Krok 7: Identyfikacja punktu kompromisowego
compromise_point = remove_dominated_points(np.vstack((dominance_filtered_alternatives, projection.reshape(1, -1))))

# Krok 8: Ocena wartości funkcji skoringowej
scoring_function_value = np.sum(np.abs(compromise_point - sample_point))

# Krok 9: Analiza wyników i ewaluacja
print(f'Projection of {sample_point} onto the skeleton curve: {projection}')
print(f'Compromise Point: {compromise_point}')
print(f'Scoring Function Value: {scoring_function_value}')

# Wizualizacja punktu kompromisowego
plt.scatter(alternatives[:, 0], alternatives[:, 1], label='Alternatives')
plt.scatter(dominance_filtered_alternatives[:, 0], dominance_filtered_alternatives[:, 1], label='Non-dominated Alternatives')
plt.scatter(reference_points[:, 0], reference_points[:, 1], label='Reference Points', marker='s', color='red')
plt.scatter(aspiration_points[:, 0], aspiration_points[:, 1], label='Aspiration Points', marker='s', color='green')
plt.plot(skeleton_curve[:, 0], skeleton_curve[:, 1], label='Skeleton Curve', linestyle='dashed', color='orange')
plt.scatter(projection[0], projection[1], label='Projection', marker='o', color='purple')
plt.scatter(compromise_point[:, 0], compromise_point[:, 1], label='Compromise Point', marker='x', color='black')
plt.scatter(sample_point[0], sample_point[1], label='Sample Point', marker='*', color='blue')
plt.legend()
plt.xlabel('Parameter 1')
plt.ylabel('Parameter 2')
plt.title('Compromise Point Identification')
plt.show()
