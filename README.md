# SUML_PowerCast_App
**Opis problemu, założenia projektu, cele i osiągnięcia**
Projekt został stworzony w celu analizy danych pogodowych, ich przekształcania oraz opracowania modelu, który umożliwi przewidywanie zużycia energii elektrycznej na podstawie nowych danych. Program może pomóc w optymalizacji zużycia energii elektrycznej w domach i firmach, umożliwiając lepsze planowanie wykorzystania urządzeń na podstawie prognoz zużycia. Dzięki temu użytkownicy mogą obniżyć rachunki za prąd i zmniejszyć negatywny wpływ na środowisko.

Główne założenia obejmują:
- Przetwarzanie danych pogodowych, które mogą mieć wpływ na zużycie energii elektrycznej.
- Tworzenie modeli predykcyjnych prognozujących zużycie w przyszłości.
- Implementację graficznego interfejsu użytkownika (GUI) z wykorzystaniem biblioteki Tkinter, która umożliwia   interakcję użytkownika z modelami.

W ramach projektu udało się:
- Opracować spójny potok przetwarzania danych i trenowania modeli w oparciu o framework Kedro.
- Zaimplementować skuteczne modele predykcyjne przy użyciu AutoGluon.
- Zintegrować aplikację Streamlit z potokiem danych.

**Instrukcja instalacji i uruchomienia**

1. **Klonowanie repozytorium:**
   ```bash
   git clone https://github.com/1nKokoreva/SUML_PowerCast_App.git
   ```

2. **Instalacja zależności:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchamianie potoku Kedro:**
   ```bash
   kedro run
   ```

**Struktura potoku**

Potok oparty na Kedro składa się z trzech głównych komponentów:

1. **Data Analysis and Preprocessing:**
   - Wczytywanie i wstępne przetwarzanie danych surowych.
   - Normalizacja i transformacja danych wejściowych zgodnie z ustalonymi parametrami.

2. **Model Training and Evaluation:**
   - Podział danych na zbiory treningowy i testowy.
   - Trenowanie modeli (m.in. regresja, drzewa decyzyjne).
   - Ewaluacja wyników modeli.

3. **Application Deployment:**
   - Uruchamianie API umożliwiającego wykonywanie predykcji na podstawie natrenowanego modelu.
   - Integracja aplikacji desktopowej z API, umożliwiająca interaktywne wizualizacje i użytkowanie przez końcowych użytkowników.

Potok Kedro zapewnia modularność procesu przetwarzania danych oraz trenowania modeli, umożliwia to łatwą rozbudowę projektu o kolejne funkcjonalności.
