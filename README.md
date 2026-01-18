# Kappa Traffic Flow: Strumieniowa Analiza Przepływu Pojazdów

## 📌 Przegląd Projektu
Projekt realizuje end-to-end potok danych w **architekturze Kappa**, służący do analizy symulowanego strumienia danych o ruchu pojazdów w Krakowie. System monitoruje przemieszczanie się pojazdów między strefami miejskimi (Centrum, Kazimierz, Bronowice itd.) i oblicza bilans pojazdów w czasie rzeczywistym.

### 🏗 Schemat Architektury


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
<img width="1341" height="384" alt="image" src="https://github.com/user-attachments/assets/01fd66fa-5b83-4041-8a9c-c38495ba2107" />
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

