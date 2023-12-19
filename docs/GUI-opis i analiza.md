# GUI dla SWD | Analiza działania metod TOPSIS i SP-CS
*Mikołaj Grzybek*

- [GUI dla SWD | Analiza działania metod TOPSIS i SP-CS](#gui-dla-swd--analiza-działania-metod-topsis-i-sp-cs)
  - [Aplikacja GUI ](#aplikacja-gui-)
    - [Budowa](#budowa)
    - [Sposób użycia](#sposób-użycia)
    - [Znane problemy i ograniczenia aplikacji](#znane-problemy-i-ograniczenia-aplikacji)
  - [Zbiór danych](#zbiór-danych)
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


## Aplikacja GUI <a name="sekcja-1"></a>

### Budowa
GUI zostało zaimplementowane w formie aplikacji webowej, gdzie część aplikacji działająca po stronie przeglądarki została napisana w "czystym" JavaScript i HTML.

Backend został oparty o framework FastAPI w języku python. Pozwala to na łatwe dodawanie nowych algorytmów i funkcjonalności, których implementacja w języku python jest o wiele łatwiejsza niż w przypadku JavaScript. Dzięki tej decyzji projektowej uniknięto korzystania z dużych i zawiłych frameworków JavaScript. 

Można to było również zaimplementować w 100% w JS tak aby wszystko działało lokalnie w przeglądarce lecz wolałem uniknąć zbyt dużej ilości kodu w tym języku na rzecz znanego mi dobrze Pythona.

Kod aplikacji jest dostępny na moim repozytorium GitHub: [GrzybekMikolaj/DecisionSupportSystem](https://github.com/GrzybekMikolaj/DecisionSupportSystem)

Aplikacja została również uruchomiona i dostępna z internetu pod adresem: [DecisionSupportSystem Koyeb.app](https://decisionsupportsystem-grzybek-private.koyeb.app/)


### Sposób użycia
Aplikacja jest bardzo prosta w obsłudze. Najpierw wnleży załadować plik z danymi poprzez przeciągniecię go we wskazane pole lub kliknięcie w nie i wybranie z systemowego menadżera plików. (Rys. 1)

![alt](rys1.jpg)
<br> *Rys.1 Pole do wrzucenia pliku*

![alt](rys1_2.jpg)
<br> *Rys.1.2 Pomyślnie załadowany plik*

Następnym krokiem jest wybranie algorytmu z listy rozwijanej. Po wybraniu żądanego algorytmu wyświetlą się możliwe do wprowadzenia parametry. Zestaw parametrów zostanie wyświetlony automatycznie na podstawie wprowadzonych do systemu danych. Przy innych zestawach danych niż ten dołączony systemem mogą wystąpić pewne problemy po stronie serwera. Usprawnienie tego jest przedmiotem dalszych prac nad GUI. (Rys. 2)

![alt](rys2.jpg)
<br> *Rys.2 Wybrany algorytm z uzupełnionymi parametrami.*

Po uzupełnieniu wszystkich informacji użytkownik powinien przycisnąć przycisk  "Optymalizuj". Strona automatycznie przewinie się w dół, a na środku ekranu zostanie wyświetlona tabela z wynikami działa algorytmu (Rys.3)

![alt](rys3.jpg)
<br> *Rys.3 Tabela z wynikami działania algorytmu*

### Znane problemy i ograniczenia aplikacji
Aplikacja ma problemy z resetowaniem cache-u na przeglądarce Firefox. Inne przeglądarki oparte o Chromium nie mają tego problemu, strona zachowa się tak samo po "odświerzeniu" jak i po ponownym wejściu z nowej karty.

Aplikacja nie nadpisuje już wpisanych parametrów algorytmu. W celu ponownego obliczenia wyników z np. innymi wagami należy odświerzyć stronę. 



## Zbiór danych
Analizie zostały podjęte zewnętrzne dyski. Na potrzeby wyboru najlepszego, 
spisano parametry sześciu różnych dysków, takie jak cena, pojemność, prędkość odczytu i zapisu. 

Parametry, które algorytm będzie brał pod uwagę to cena, pojemność dysku oraz prędkość zapisu i odczytudanych.
Zbiór został dołączony do zadania w postaci pliku .csv gotowego do podania aplikacji

``` csv
id, marka,                  cena,   pojemnosc,  prędkosc-odczytu,   predkosc-zapisu
M1, lexar-sl200,            300,    1000,       550,                400
M2, adata-elitr-se880,      300,    1000,       2000,               2000
M3, samsungh-t7,            405,    1000,       1050,               1000
M4, samsung-t7,             420,    1000,       1050,               1000
M5, sandisk-extreme,        400,    1000,       1050,               1000
M6, sandisk-extreme-pro,    625,    1000,       2000,               2000
```











## Wyniki metody TOPSIS <a name="sekcja-12"></a>
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