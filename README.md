
# Skrypty ArcPy do analizy GIS (PPA Gr2)

Witaj! To repozytorium zawiera dwa skrypty Python (ArcPy) do przetwarzania danych GIS w ArcGIS Pro. Skrypty automatyzują analizę zmian pokrycia terenu i import shapefile'ów do geobazy.

## Zawartość
- **analiza_zmian.py**: Analizuje zmiany pokrycia terenu między latami 2014 a 2020.
  - Tworzy warstwy połączone (Merge) i przecięcia (Intersect).
  - Oblicza procent zmian i wizualizuje na wykresach (słupkowy + kołowy, zapis do JPG).
  - Wymagania: ArcGIS Pro, matplotlib.
  
- **import_shapefiles.py**: Importuje shapefile'e do geobazy z poprawą nazw plików.
  - Kopiuje i czyści nazwy (zamienia kropki na podkreślenia).
  - Eksportuje do geobazy tylko nowe warstwy (sprawdza istnienie).
  - Bezpieczna obsługa błędów i logowanie.

## Jak uruchomić
1. Zainstaluj ArcGIS Pro i Python (z ArcPy).
2. Ustaw ścieżki w kodzie (np. geobaza, foldery SHP).
3. Uruchom w Python Window ArcGIS lub jako skrypt `.py`.

## Wymagania
- Python 3.11.11 z ArcPy 3.5.2
- Biblioteki: `arcpy`, `matplotlib`, `os`, `shutil`.
- Dane: Geobaza `.gdb` i foldery z shapefile'ami.

## Autor


## Licencja
MIT License – swobodne użycie i modyfikacja.

Dzięki za wizytę! Jeśli masz sugestie, otwórz issue. 🚀
