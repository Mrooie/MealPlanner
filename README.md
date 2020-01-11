<img alt="Logo" src="http://coderslab.pl/svg/logo-coderslab.svg" width="400">

# ScrumLab Python

## Czym jest ScrumLab?

ScrumLab to projekt, którego celem jest nauczenie Cię pracy w zespole programistów. Symuluje on realne zadania
w projekcie aplikacji webowej. Podczas tego tygodnia będziesz uczestniczyć w codziennych spotkaniach, rozwiązywać 
problemy, robić *code review* i integrować swój kod z kodem kolegów.

## Opis projektu

Pani Maria Iksińska napisała książkę kucharską, która stała się bestsellerem na rynku książek kucharskich w Polsce i zwróciła się do nas z prośba o przygotowanie dla jej czytelników aplikacji do planowania posiłków. Książka Pani Iksińskiej promuje zdrowe odżywianie i podkreśla jak ważną rolę odgrywa w nim planowanie posiłków. Chce zacząć przeprowadzać w całym kraju warsztaty, na których będzie uczyć uczestników planowania posiłków.

Pani Maria chce rozwijać swój biznes, a do zrealizowania swoich celów potrzebuje strony-wizytówki oraz prostej aplikacji do planowania posiłków.

Przed przystąpieniem do pracy przeczytaj poniższe wskazówki

## Jak zacząć?

1. Stwórz [*fork*](https://guides.github.com/activities/forking/) repozytorium.
2. Sklonuj repozytorium na swój komputer. Użyj do tego komendy `git clone adres_repozytorium`
Adres repozytorium możesz znaleźć na stronie repozytorium po naciśnięciu w guzik "Clone or download".
3. Rozwiąż zadania i skomituj zmiany do swojego repozytorium. Użyj do tego komend `git add nazwa_pliku`.
Jeżeli chcesz dodać wszystkie zmienione pliki użyj `git add .` 
Pamiętaj że kropka na końcu jest ważna!
Następnie skommituj zmiany komendą `git commit -m "nazwa_commita"`
4. Wypchnij zmiany do swojego repozytorium na GitHubie.  Użyj do tego komendy `git push origin master`
5. Stwórz [*pull request*](https://help.github.com/articles/creating-a-pull-request) do oryginalnego repozytorium, gdy skończysz wszystkie zadania.


## Plan tego repozytorium

* `scrumlab` – katalog z projektem Django. Znajdują się w nim pliki 
  - `settings.py` – ustawienia projektu,
  - `urls.py` – dane URL-i,
  - `local_settings.py.example` – ustawienia lokalne; po szczegóły zajrzyj do rozdziału **Konfiguracja projektu**,
* `jedzonko` – katalog aplikacji Django, nad którą będziesz pracował.
* `static` – katalog z plikami statycznymi; po szczegóły zajrzyj do rozdziału **Konfiguracja projektu**

## Konfiguracja projektu

### Co skonfigurowaliśmy za Ciebie?

- szablony
  - umieszczaj je w aplikacji **jedzonko** w katalogu **templates**,
- pliki statyczne
  - pliki statyczne (czyli wszystkie pliki, które są serwowane przez aplikację: obrazki, pliki CSS, JS itp.)
  umieszczaj w katalogu **static**, który znajduje się w głównym katalogu projektu.

### Czego nie skonfigurowaliśmy?

- bazy danych (ze względów bezpieczeństwa)

**Pamiętaj:** nie należy trzymać danych wrażliwych pod kontrolą Gita! Takimi danymi wrażliwymi
są m. in. dane do połączenia z bazą danych. Te dane trzymamy w pliku **local_settings.py**,
którego nie znajdziesz w tym repozytorium (plik jest dodany do **.gitignore**)!

Zajrzyj do pliku **settings.py**, znajdziesz w nim następującą sekcję:

```python
try:
    from scrumlab.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)
```

Oznacza to, że Django podczas każdego uruchomienia będzie próbowało zaimportować
stałą `DATABASES` z pliku **local_settings.py**. Tam trzymaj dane do połączenia.
Nie umieszczaj tego pliku pod kontrolą Gita. Aby ułatwić Ci pracę, przygotowaliśmy 
plik **local_settings.py.example**, w którym znajdziesz przygotowane odpowiednie dane.
Wystarczy tylko, że zmienisz plikowi **local_settings.py.example** nazwę na  **local_settings.py** 
i uzupełnisz go.

--- 

Jeśli wszystko skonfigurowałeś poprawnie, to pod adresem http://localhost:8000/index zobaczysz przykładową stronę.
