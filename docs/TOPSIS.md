# Metoda TOPSIS - Analiza i Implementacja 
*Mikołaj Grzybek*

- [Metoda TOPSIS - Analiza i Implementacja](#metoda-topsis---analiza-i-implementacja)
  - [Metoda TOPSIS ](#metoda-topsis-)
    - [Dane podlegające analzie ](#dane-podlegające-analzie-)
    - [Wyniki metody TOPSIS ](#wyniki-metody-topsis-)
      - [Wariant #1 wag ](#wariant-1-wag-)
      - [Wariant #2 wag ](#wariant-2-wag-)
      - [Wariant #3 wag ](#wariant-3-wag-)
      - [Wariant #4 wag ](#wariant-4-wag-)
      - [Wariant #5 wag ](#wariant-5-wag-)
    - [Podsumowanie wyników ](#podsumowanie-wyników-)
  - [Implementacja TOPSIS ](#implementacja-topsis-)
    - [Algorytm ](#algorytm-)
    - [Przykładowe dane wejściowe ](#przykładowe-dane-wejściowe-)
    - [Wynik działania algorytmu  ](#wynik-działania-algorytmu--)


## Metoda TOPSIS <a name="sekcja-1"></a>

### Dane podlegające analzie <a name="sekcja-11"></a>
Analizie zostały podjęte zewnętrzne dyski. Na potrzeby wyboru najlepszego, 
spisano parametry sześciu różnych dysków, takie jak cena, pojemność, prędkość odczytu i zapisu. 
``` csv
id, marka,                  cena,   pojemnosc,  prędkosc-odczytu,   predkosc-zapisu
M1, lexar-sl200,            300,    1000,       550,                400
M2, adata-elitr-se880,      300,    1000,       2000,               2000
M3, samsungh-t7,            405,    1000,       1050,               1000
M4, samsung-t7,             420,    1000,       1050,               1000
M5, sandisk-extreme,        400,    1000,       1050,               1000
M6, sandisk-extreme-pro,    625,    1000,       2000,               2000
```
### Wyniki metody TOPSIS <a name="sekcja-12"></a>
#### Wariant #1 wag <a name="sekcja-121"></a>
Użyto następujących wartości wag dla pierwszej analizy wielokryterialnej:
```
cena,	pojemnosc,	predkosc-odczytu,	predkosc-zapisu
0.6,	0.3,		0.05,				0.05
```
Dla powyższych wag uzyskano następujące wyniki:
``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.992
M1: 0.968
M5: 0.817
M3: 0.797
M4: 0.728
M6: 0.032
```

#### Wariant #2 wag <a name="sekcja-122"></a>
Użyto następujących wartości wag dla pierwszej analizy wielokryterialnej:
```
cena,	pojemnosc,	predkosc-odczytu,	predkosc-zapisu
0.5,	0.3,		0.1,				0.1
```
Dla powyższych wag uzyskano następujące wyniki:
``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.959
M1: 0.839
M5: 0.744
M3: 0.725
M4: 0.663
M6: 0.161
```

#### Wariant #3 wag <a name="sekcja-123"></a>
Użyto następujących wartości wag dla pierwszej analizy wielokryterialnej:
```
cena,	pojemnosc,	predkosc-odczytu,	predkosc-zapisu
0.35,	0.3,		0.1,				0.25
```
Dla powyższych wag uzyskano następujące wyniki:
``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.958
M6: 0.581
M5: 0.51
M3: 0.498
M4: 0.462
M1: 0.419
```

#### Wariant #4 wag <a name="sekcja-124"></a>
Użyto następujących wartości wag dla pierwszej analizy wielokryterialnej:
```
cena,	pojemnosc,	predkosc-odczytu,	predkosc-zapisu
0.5,	0.25,		0.1,				0.15
```
Dla powyższych wag uzyskano następujące wyniki:
``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.963
M1: 0.764
M5: 0.704
M3: 0.686
M4: 0.628
M6: 0.236
```

#### Wariant #5 wag <a name="sekcja-125"></a>
Użyto następujących wartości wag dla pierwszej analizy wielokryterialnej:
```
cena,	pojemnosc,	predkosc-odczytu,	predkosc-zapisu
0.4,	0.3,		0.1,				0.2
```
Dla powyższych wag uzyskano następujące wyniki:
``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.956
M5: 0.599
M3: 0.584
M1: 0.576
M4: 0.537
M6: 0.424
```



### Podsumowanie wyników <a name="sekcja-13"></a>
Z powyższych wyników można wysunąć wniosek, że algorytm poprawnie wybrał najbardziej optymalny dysk, którym jest "M2". Należy zwrócić uwagę, że jest to najtańszy wybór, który przy okazji ma pozostałe parametry nie gorsze niż reszta alternatyw. 

Przy zmianie wag i przesunięciu wartości z "cena" na jakikolwiek inny, znaczny wzrost pozycji w rankigu zalicza dysk "M6". Jest to spodziewany efekt, gdyż ten dysk ma dokładnie takie same parametry jak "M2" poza cena, która jest dwukrotnie większa. 


## Implementacja TOPSIS <a name="sekcja-2"></a>
Algorytm, napisany w języku python został zaprojektowany tak aby wystarczyło wywołać funkcję ```topsis()``` podając jako jedyny argument, rozpakowany funkcją ```read_json()``` plik z danymi.

Funkcje wyliczające wszystkie parametry potrzebne metodzie TOPSIS zostały zaimplementowane zgodnie z przykładem podanym w pliku Excel.

### Algorytm <a name="sekcja-21"></a>
``` python {bgcolor="#f0f0f0"}
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
```

### Przykładowe dane wejściowe <a name="sekcja-22"></a>
Algorytm przyjmuje dane w formacie który funkcja ```json_load()``` jest w stanie rozpakować. Implementacja traktuje parametr wejściowy jako słownik zagnieżdżony, gdzie pierwszą warstawą jest jeden obiekt jako który sam jest słownikiem parametrów i ich wartości dla danego obiektu. 

W tej samej strukturze danych znajduję się też obiekt ```weights``` gdzie opisane są wagi dla każdego z dostępnych parametrów.

``` json {bgcolor="#f0f0f0"}
{
   "M1": {
     "company": "lexar",
     "name": "sl200",
     "cena": 300,
     "pojemnosc": 1000,
     "predkosc_odczytu": 550,
     "predkosc_zapisu": 400
   },
    ...
    "weights": {
     "company": 0,
     "name": 0,
     "cena": 0.6,
     "pojemnosc": 0.3,
     "predkosc_odczytu": 0.05,
     "predkosc_zapisu": 0.05
   }
 }
```

### Wynik działania algorytmu  <a name="sekcja-23"></a>
Wynikiem działania algorytmu będzie wyświetlenie w terminalu rankigu obiektów wraz z odległością między alternatywami w przestrzeni kryteriów (miara separacji).

Sama funkja ```topsis()``` zwraca słownik z obiektem i wartością miary separacji co umożliwia łatwą jej integrację z większym systemem.

``` {bgcolor="#f0f0f0"}
Rankings:
M2: 0.992
M1: 0.968
M5: 0.817
M3: 0.797
M4: 0.728
M6: 0.032
```