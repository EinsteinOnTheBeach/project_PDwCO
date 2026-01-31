# Kappa Traffic Flow: Strumieniowa Analiza Przepływu Pojazdów

## 📌 Przegląd Projektu
Projekt realizuje end-to-end potok danych w **architekturze Kappa**, służący do analizy symulowanego strumienia danych o ruchu pojazdów w Krakowie. System monitoruje przemieszczanie się pojazdów między strefami miejskimi (Centrum, Kazimierz, Bronowice itd.) i oblicza bilans pojazdów w czasie rzeczywistym.

### 🏗 Schemat i Uzadafnienie Wyboru Architektury
Wybór architektury Kappa wynika z priorytetu przetwarzania danych w czasie rzeczywistym oraz dążenia do uproszczenia struktury systemu. W monitorowaniu ruchu drogowego kluczowy jest najniższy możliwy czas latencji (opóźnienia), co czyni Kappę rozwiązaniem optymalnym ze względu na rezygnację z powolnej warstwy wsadowej (batch). Dzięki zastosowaniu silnika Spark Structured Streaming oraz technologii Delta Lake, system zapewnia pełną spójność danych przy użyciu jednego kodu źródłowego dla danych bieżących i historycznych. Pozwala to na błyskawiczną reakcję na zdarzenia drogowe i eliminuje ryzyko rozbieżności wyników, które występuje w architekturze Lambda.


Architektura została podzielona na trzy główne warstwy, z których każda odpowiada za inny etap cyklu życia danych:

1. WARSTWA UNIFIED LOG (Ingestia)
Jest to punkt wejścia dla wszystkich danych systemowych. Służy jako niezmienny rejestr zdarzeń, który przechowuje surowy strumień informacji przed ich przetworzeniem.

Funkcja: Przyjmowanie komunikatów JSON o ruchu pojazdów i zapewnienie ich trwałości.

Zasoby: Wykorzystanie usługi Azure Event Hubs, która umożliwia wielokrotny odczyt tego samego strumienia (istotne przy ewentualnym przeliczaniu danych historycznych).

2. WARSTWA PROCESSING (Przetwarzanie)
W tej warstwie odbywa się cała logika analityczna systemu. Dane są pobierane ze strumienia i przekształcane w użyteczne informacje biznesowe.

Funkcja: Filtrowanie i walidacja formatu przychodzących danych.

Grupowanie zdarzeń w oknach czasowych (Windowing).

Obliczanie bilansu pojazdów w poszczególnych strefach w czasie rzeczywistym.

Zarządzanie stanem przetwarzania (Checkpointing), co pozwala na wznowienie pracy systemu po awarii bez utraty danych.

3. WARSTWA STORAGE (Składowanie)
Końcowy etap, w którym przetworzone wyniki są zapisywane w sposób trwały i uporządkowany.

Funkcja: Utrwalanie wyników analizy w formacie gotowym do raportowania.

Zasoby: Wykorzystanie formatu Delta Lake na magazynie danych Azure. Zapewnia to transakcyjność oraz wysoką wydajność przy odczycie danych przez narzędzia do wizualizacji.

<img width="1341" height="384" alt="image" src="images/kappa_diagram/jpeg" />
*Diagram architektury Kappa*
---

## 🛠 Komponenty Techniczne

### 1. Ingest Strumieniowy (Azure Event Hubs)
* **Producent:** Skrypt Python `producer_withoutCS.py` symuluje czujniki drogowe, generując zdarzenia JSON (plate_number, speed, from_zone, to_zone).
* **Broker:** Azure Event Hubs przyjmuje dane na porcie strumieniowym `inputstream`.

### 2. Przetwarzanie (Azure Databricks)
Główna logika zawarta w notatniku `obrobka_danych.ipynb` obejmuje:
* **Watermarking:** Ustawiony na 15 sekund w celu stabilizacji danych spóźnionych.
* **Sliding Window:** Okno 2-minutowe przesuwane co 30 sekund.
* **Logika Bilansowa:** Zastosowanie transformacji `unionByName` dla wjazdów (+1) i wyjazdów (-1), co pozwala na uzyskanie rzeczywistej liczby aut w danej strefie w czasie rzeczywistym.

### 3. Warstwa Składowania (Delta Lake)
* Dane wynikowe są zapisywane w formacie **Delta Lake** na Azure Data Lake Storage Gen2.
* Wykorzystanie formatu Delta zapewnia transakcyjność ACID oraz wysoką wydajność odczytu.

### 4. Infrastruktura jako Kod (IaC)
* Folder `/iac` zawiera plik `main.tf`.
* Automatyzacja obejmuje stworzenie grupy zasobów oraz Storage Account w regionie **Poland Central**.

### 5. Automatyzacja CI/CD
* Wdrożono potok **GitHub Actions** (`ci_pipeline.yml`), który przy każdym wypchnięciu kodu sprawdza składnię skryptów Python oraz poprawność plików Terraform.

---

## 📊 Wizualizacje i Dowody Działania

### Bilans pojazdów w strefach (Real-time Bar Chart)
<img width="1341" height="384" alt="image" src="images/pipeline_running.png" />
*Wykres przedstawia dynamiczny bilans aut w dzielnicach Krakowa.*

---

## 🛡 Bezpieczeństwo i Niezawodność
* **Fault Tolerance:** Wykorzystano mechanizm **checkpointing** składowany w lokalizacji `/mnt/checkpoints/traffic_counts`.
* **Security:** Zgodnie z najlepszymi praktykami, wszystkie klucze dostępu i parametry połączenia zostały usunięte z plików przed ich publikacją w repozytorium.

---

## 🚀 Instrukcja Uruchomienia
1. **Infrastruktura:** Uruchom `terraform apply` w folderze `/iac`.
2. **Konfiguracja:** Uruchom notatnik `delta_lake_konfiguracja.ipynb`, aby zamontować zasoby Azure.
3. **Analiza:** Uruchom notatnik `obrobka_danych.ipynb`.
4. **Generator:** Uruchom lokalnie `python producer_withoutCS.py`.

