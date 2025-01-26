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
- Zintegrować GUI z potokiem danych.

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