import math
from file_handler import read_json
import matplotlib.pyplot as plt

def spcs(data):
    weights = {key: value for key, value in data.get("weights", {}).items() if value != 0 and isinstance(value, (int, float))}

    if not weights:
        print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
        return

    numeric_parameters = ["cena", "pojemnosc"]

    alternatives = {
        key: {
            param: value for param, value in data[key].items() if param in numeric_parameters and isinstance(value, (int, float))
        } for key in data if key not in ["weights"]
    }

    if not alternatives:
        print("Brak prawidłowych danych. Algorytm nie może być wykonany.")
        return

    non_dominated_alternatives = remove_dominants(alternatives)

    # TODO:
    # for web app it has to be included in form and merged with the alternatives in the json
    aspiration_points = define_aspiration_points()
    
def remove_dominants(alternatives):
    non_dominated_alternatives = {}

    for alt1_name, alt1_vector in alternatives.items():
        is_dominated = False

        for alt2_name, alt2_vector in alternatives.items():
            if alt1_name != alt2_name:
                is_dominated = all(alt1_vector[criterion] <= alt2_vector[criterion] for criterion in alt1_vector)

                if is_dominated:
                    break 

        if not is_dominated:
            non_dominated_alternatives[alt1_name] = alt1_vector

    return non_dominated_alternatives

def define_aspiration_points():
    try:
        cena_aspiracja = float(input("Podaj punkt aspiracji dla ceny: "))
        pojemnosc_aspiracja = float(input("Podaj punkt aspiracji dla pojemności: "))
        return cena_aspiracja, pojemnosc_aspiracja
    except ValueError:
        print("Wprowadzona wartość nie jest liczbą.")
        return None

def construct_skeleton_curves(aspiration_points, status_quo):
    cena_aspiracja, pojemnosc_aspiracja = aspiration_points
    cena_status_quo, pojemnosc_status_quo = status_quo

    # Konstrukcja krzywych szkieletowych
    skeleton_curve_x = [cena_aspiracja, cena_status_quo]
    skeleton_curve_y = [pojemnosc_aspiracja, pojemnosc_status_quo]

    # Wyświetlenie wykresu
    plt.plot(skeleton_curve_x, skeleton_curve_y, marker='o', label='Krzywa szkieletowa')
    plt.scatter([cena_aspiracja, cena_status_quo], [pojemnosc_aspiracja, pojemnosc_status_quo], color='red')
    plt.text(cena_aspiracja, pojemnosc_aspiracja, ' Aspiracja', fontsize=10, ha='right')
    plt.text(cena_status_quo, pojemnosc_status_quo, ' Status Quo', fontsize=10, ha='right')

    plt.xlabel('Cena')
    plt.ylabel('Pojemność')
    plt.title('Krzywe Szkieletowe')
    plt.legend()
    plt.grid(True)
    plt.show()



file_path = 'static/data20rand.json'

data = read_json(file_path)


aspiration_points = (1000, 2000)  # Przykładowe punkty aspiracji
status_quo = (1500, 1800)        # Przykładowy punkt status quo

construct_skeleton_curves(aspiration_points, status_quo)



# spcs(data)

# print("Algorithm: SP-CS")
# print("Rankings:")
# for rank, score in result:
#     rounded_score = round(score, 3)
#     print(f"{rank}: {rounded_score}")