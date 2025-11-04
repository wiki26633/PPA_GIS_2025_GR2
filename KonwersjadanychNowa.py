# -*- coding: utf-8 -*-
"""
Skrypt: Import shapefile'ów z folderu do geobazy z poprawą nazw
- Kopiuje pliki .shp do nowego folderu, zamienia '.' na '_'
- Eksportuje do geobazy jako: GDA2014_NazwaBezKropki
- Sprawdza, czy warstwa już istnieje w geobazie → pomija, jeśli tak
- Bezpieczne operacje, logowanie, obsługa błędów
"""
 
import arcpy
import os
import shutil
 
# =============================================================================
# KONFIGURACJA ŚCIEŻEK
# =============================================================================
folder_shp=r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\dane\2213_SHP_2020"
folder_new_shp=r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\dane\new_2213_SHP_2020"
arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"         # Geobaza docelowa
rocznik = "2014"
 
arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"

# arcpy.env.overwriteOutput = True  # Pozwala nadpisywać, ale my i tak sprawdzamy istnienie
 
# Utwórz folder roboczy, jeśli nie istnieje
os.makedirs(folder_new_shp, exist_ok=True)
 
# =============================================================================
# KROK 1: Kopiowanie i zmiana nazw (kropka → podkreślenie)
# =============================================================================
print("KROK 1: Kopiowanie i zmiana nazw plików (. → _)")
 
copied_count = 0
for file in os.listdir(folder_shp):
    file_path = os.path.join(folder_shp, file)
    if not os.path.isfile(file_path):
        continue  # Pomijaj foldery
 
    name, ext = os.path.splitext(file)
    # if ext.lower() != ".shp":
    #     continue  # Przetwarzaj tylko .shp
 
    # Zamiana wszystkich kropek w nazwie na podkreślenia
    new_name = name.replace(".", "_") + ext
    dest_path = os.path.join(folder_new_shp, new_name)
 
    try:
        shutil.copy(file_path, dest_path)
        print(f"  Skopiowano: {file} → {new_name}")
        copied_count += 1
    except Exception as e:
        print(f"  BŁĄD kopiowania {file}: {e}")
 
print(f"Zakończono kopiowanie: {copied_count} plików .shp\n")
 
 
# =============================================================================
# KROK 2: Eksport do geobazy – tylko jeśli warstwa NIE istnieje
# =============================================================================
print("KROK 2: Eksport shapefile'ów do geobazy (z pominięciem istniejących)")
 
exported_count = 0
skipped_count = 0
 
for file in os.listdir(folder_new_shp):
    file_path = os.path.join(folder_new_shp, file)
    name, ext = os.path.splitext(file)
 
    if ext.lower() != ".shp":
        continue  # Tylko .shp
 
    # # Usuń potencjalne podwójne podkreślenia po replace
    # clean_name = name.replace("__", "_")
 
    # Pobierz nazwę po "__" (jeśli istnieje) – zakładamy strukturę: coś__GDA2014_...
    if "__" in name:
        try:
            part_after = name.split("__", 1)[1]  # Bierz część po pierwszym "__"
        except:
            part_after = name
    else:
        part_after = name
 
    # Docelowa nazwa w geobazie
    fc_name = f"GDA{rocznik}_" + part_after
 
    # SPRAWDZENIE: czy warstwa już istnieje w geobazie?
    if arcpy.Exists(fc_name):
        print(f"  POMINIĘTO: {fc_name} (już istnieje w geobazie)")
        skipped_count += 1
        continue
 
    # Eksport do geobazy
    try:
        print(f"  Eksportuję: {file} → {fc_name}")
        arcpy.conversion.ExportFeatures(
            in_features=file_path,
            out_features=fc_name
        )
        print(f"    → Utworzono: {fc_name}")
        exported_count += 1
    except arcpy.ExecuteError:
        print(f"    BŁĄD ArcPy przy eksporcie {file}: {arcpy.GetMessages()}")
    except Exception as e:
        print(f"    NIEOCZEKIWANY BŁĄD: {file} → {e}")
 
print(f"\nZakończono eksport:")
print(f"  → Utworzono nowych warstw: {exported_count}")
print(f"  → Pominięto (już istnieją): {skipped_count}")
 
# =============================================================================
# KROK 3: Opcjonalne czyszczenie folderu roboczego (zakomentowane)
# =============================================================================
"""
print("\nCzyszczenie folderu roboczego...")
try:
    shutil.rmtree(folder_new_shp)
    print(f"Usunięto folder: {folder_new_shp}")
except Exception as e:
    print(f"Nie udało się usunąć folderu: {e}")
"""
 
# =============================================================================
# KONIEC
# =============================================================================
print("\nKONIEC przetwarzania. Wszystkie operacje zakończone.")