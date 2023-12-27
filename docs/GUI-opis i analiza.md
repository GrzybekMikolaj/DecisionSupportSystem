# GUI dla SWD | Analiza działania metod TOPSIS i SP-CS
*Mikołaj Grzybek*

- [GUI dla SWD | Analiza działania metod TOPSIS i SP-CS](#gui-dla-swd--analiza-działania-metod-topsis-i-sp-cs)
  - [Aplikacja GUI ](#aplikacja-gui-)
    - [Budowa](#budowa)
    - [Sposób użycia](#sposób-użycia)
    - [Znane problemy i ograniczenia aplikacji](#znane-problemy-i-ograniczenia-aplikacji)
  - [Zbiór danych](#zbiór-danych)
  - [Wyniki działania zaimplementowanych algorytmów](#wyniki-działania-zaimplementowanych-algorytmów)
    - [Algorytm TOPSIS](#algorytm-topsis)
    - [Algorytm SP-CS](#algorytm-sp-cs)


## Aplikacja GUI <a name="sekcja-1"></a>

### Budowa
GUI zostało zaimplementowane w formie aplikacji webowej, gdzie część aplikacji działająca po stronie przeglądarki została napisana w "czystym" JavaScript i HTML.

Backend został oparty o framework FastAPI w języku python. Pozwala to na łatwe dodawanie nowych algorytmów i funkcjonalności, których implementacja w języku python jest o wiele łatwiejsza niż w przypadku JavaScript. Dzięki tej decyzji projektowej uniknięto korzystania z dużych i zawiłych frameworków JavaScript. 

Można to było również zaimplementować w 100% w JS tak aby wszystko działało lokalnie w przeglądarce lecz wolałem uniknąć zbyt dużej ilości kodu w tym języku na rzecz znanego mi dobrze Pythona.

Kod aplikacji jest dostępny na moim repozytorium GitHub: [GrzybekMikolaj/DecisionSupportSystem](https://github.com/GrzybekMikolaj/DecisionSupportSystem)

Aplikacja została również uruchomiona i dostępna z internetu pod adresem: [DecisionSupportSystem Koyeb.app](https://decisionsupportsystem-grzybek-private.koyeb.app/)

Aplikację można również uruchomić lokalnie, jedynym wymaganiem jest python w wersji 3.10 lub wyżej
W folderze z kodem należy wykonać następujące komendy:
``` powershell
# Należy zainstalować FastAPI
pip install -r ".\requirements.txt"

# Uruchomić serwer
uvicorn main:app --reload

# Serwer będzie dostępny z przeglądarki pod adresem 
127.0.0.1:8000
```

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
Aplikacja ma problemy z resetowaniem cache-u na przeglądarce Firefox. Inne przeglądarki oparte o Chromium nie mają tego problemu, strona zachowa się tak samo po "odświeżeniu" jak i po ponownym wejściu z nowej karty.

Aplikacja nie nadpisuje już wpisanych parametrów algorytmu. W celu ponownego obliczenia wyników z np. innymi wagami należy odświeżyć stronę. 



## Zbiór danych
Analizie zostały podjęte zewnętrzne dyski. Na potrzeby wyboru najlepszego, 
spisano parametry sześciu różnych dysków, takie jak cena, pojemność, prędkość odczytu i zapisu. 

Parametry, które algorytm będzie brał pod uwagę to cena, pojemność dysku oraz prędkość zapisu i odczytudanych.
Zbiór został dołączony do zadania w postaci pliku .csv gotowego do podania aplikacji


id | marka |  cena  | pojemnosc  | prędkosc-odczytu | predkosc-zapisu
---- | ---- | ---- | ---- | ---- | ---- |
M1 | lexar-sl200 | 300 | 1000   | 550 |      400
M2 |  adata-elitr-se880 |   300 |     1000 |        2000 |      2000
M3 |  samsungh-t7 | 405 |  1000   |   1050 |       1000
M4 | samsung-t7 |   420 |  1000 | 1050 |             1000
M5 | sandisk-extreme | 400 |  1000 | 1050 |            1000
M6 |  sandisk-extreme-pro |     625 |     1000 |        2000 | 2000




## Wyniki działania zaimplementowanych algorytmów
Przyjęto poniższe wagi

Cena  | Pojemność  | Prędkość Odczytu | Prędkość Zapisu
| ---- | ---- | ---- | ---- |
0.6 | 0.3 | 0.05 | 0.05



### Algorytm TOPSIS

Wynikiem działania tego algorytmu przedstawiono poniżej:

Pozycja | Nazwa | Wynik 
---- | ---- | ----
1 | M2 | 1.0 
2 | M1 | 0.9719
3 | M5 | 0.8194 
4 | M3 | 0.7990 
5 | M4 | 0.7305
6 | M6 | 0.0280

### Algorytm SP-CS

Wynikiem działania tego algorytmu przedstawiono poniżej:

Pozycja | Nazwa | Wynik 
---- | ---- | ----
1 | M2 | 1.0 
2 | M1 | 0.9719
3 | M5 | 0.8194 
4 | M3 | 0.7990 
5 | M4 | 0.7305
6 | M6 | 0.0280