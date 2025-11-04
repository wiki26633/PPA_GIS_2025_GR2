# -*- coding: utf-8 -*-
"""
Analiza zmian pokrycia terenu 2014 → 2020
- Automatyczne tworzenie warstw PT_2014, PT_2020 i PT_2014_2020
- Analiza zmian na podstawie kodów X_KOD
- Wykresy: słupkowy (top 15 + inne) i kołowy (zmiana vs bez zmian)
- Zapis wykresów do plików JPG
"""
 
import arcpy
from collections import defaultdict
import matplotlib.pyplot as plt
import os
 
# =============================================================================
# KONFIGURACJA
# =============================================================================
arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"
output_2014 = "PT_2014"
output_2020 = "PT_2020"
inter = "PT_2014_2020"
 
# Ścieżki do zapisu wykresów
output_dir = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\wyniki"
os.makedirs(output_dir, exist_ok=True)  # Utwórz folder, jeśli nie istnieje
 
plot_bar_path = os.path.join(output_dir, "zmiany_slupkowy.jpg")
plot_pie_path = os.path.join(output_dir, "zmiany_kolowy.jpg")
 
# =============================================================================
# KROK 1: Sprawdzenie i utworzenie warstw PT_2014 i PT_2020 (Merge)
# =============================================================================
def create_merged_layer(year, pattern_year, output_name):
    """Tworzy warstwę połączoną dla danego roku, jeśli nie istnieje."""
    if arcpy.Exists(output_name):
        print(f"Warstwa istnieje: {output_name}")
        return True
 
    print(f"Tworzenie warstwy: {output_name} (rok {year})...")
    inputs = []
    for fc in arcpy.ListFeatureClasses():
        if pattern_year in fc and "GDA2014" in fc and "OT_PT" in fc:
            inputs.append(fc)
 
    if not inputs:
        print(f"Nie znaleziono warstw dla roku {year} (szukano: {pattern_year})")
        return False
 
    arcpy.management.Merge(inputs, output_name)
    print(f"Utworzono: {output_name} ({len(inputs)} warstw)")
    return True
 
 
# Tworzenie warstw dla 2014 i 2020
if not create_merged_layer("2014", "2014", output_2014):
    raise RuntimeError("Nie udało się utworzyć warstwy PT_2014")
 
if not create_merged_layer("2020", "2020", output_2020):
    raise RuntimeError("Nie udało się utworzyć warstwy PT_2020")
 
 
# =============================================================================
# KROK 2: Sprawdzenie i utworzenie warstwy przecięcia (Intersect)
# =============================================================================
if arcpy.Exists(inter):
    print(f"Warstwa przecięcia istnieje: {inter}")
else:
    print(f"Tworzenie warstwy przecięcia: {inter}...")
    arcpy.analysis.Intersect(
        in_features=[f"{output_2014} #", f"{output_2020} #"],
        out_feature_class=inter,
        join_attributes="ALL",
        cluster_tolerance=None,
        output_type="INPUT"
    )
    print(f"Utworzono: {inter}")
 
 
# =============================================================================
# KROK 3: Analiza zmian pokrycia terenu (X_KOD vs X_KOD_1)
# =============================================================================
area_by_pair = defaultdict(float)
area_all = 0.0
area_change = 0.0
 
print("Odczytywanie danych z warstwy przecięcia...")
with arcpy.da.SearchCursor(inter, ["X_KOD", "X_KOD_1", "Shape_Area"]) as cursor:
    for kod1, kod2, area in cursor:
        area_all += area
        if kod1 != kod2:
            area_by_pair[(kod1, kod2)] += area
            area_change += area
 
# Obliczenie procentów
if area_all > 0:
    percent_no_change = ((area_all - area_change) / area_all) * 100
    percent_change = (area_change / area_all) * 100
else:
    percent_no_change = percent_change = 0.0
 
print(f"Powierzchnia bez zmian: {percent_no_change:.2f}%")
print(f"Powierzchnia ze zmianą: {percent_change:.2f}%")
 
 
# =============================================================================
# KROK 4: Przygotowanie danych do wykresu (top 15 + "inne")
# =============================================================================
area_by_pair_sort = sorted(area_by_pair.items(), key=lambda x: x[1], reverse=True)
separator = 15
top_changes = []
other_percent = 0.0
 
for i, (pair, area) in enumerate(area_by_pair_sort):
    percent = (area / area_change) * 100 if area_change > 0 else 0
    label = f"{pair[0]}-{pair[1]}"
 
    if i < separator:
        top_changes.append([label, percent])
    else:
        other_percent += percent
 
if other_percent > 0:
    top_changes.append(["inne", other_percent])
 
 
# =============================================================================
# KROK 5: Wykres słupkowy – zapis do JPG
# =============================================================================
plt.figure(figsize=(13, 7))
wartosci = [x[1] for x in top_changes]
etykiety = [x[0] for x in top_changes]
 
bars = plt.bar(etykiety, wartosci, color='skyblue', edgecolor='navy', linewidth=0.8)
plt.xlabel("Zmiana pokrycia terenu (2014 → 2020)", fontsize=12)
plt.ylabel("Udział w zmianach [%]", fontsize=12)
plt.title("15 największych zmian powierzchni pokrycia terenu i reszta", fontsize=14, pad=20)
plt.xticks(rotation=75, ha='right', fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
 
# Dodanie wartości na słupkach
for bar in bars:
    height = bar.get_height()
    if height > 0.5:  # Tylko jeśli >0.5%
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                 f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
 
plt.tight_layout()
plt.savefig(plot_bar_path, dpi=300, bbox_inches='tight', format='jpg')
print(f"Zapisano wykres słupkowy: {plot_bar_path}")
plt.close()
 
 
# =============================================================================
# KROK 6: Wykres kołowy – udział zmian vs bez zmian – zapis do JPG
# =============================================================================
plt.figure(figsize=(8, 8))
wartosci_pie = [percent_no_change, percent_change]
etykiety_pie = ['Bez zmian', 'Zmiana']
colors_pie = ['#90EE90', '#FFB6C1']  # jasnozielony, różowy
 
wedges, texts, autotexts = plt.pie(
    wartosci_pie,
    labels=etykiety_pie,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_pie,
    textprops={'fontsize': 12},
    wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
)
 
# Pogrubienie etykiet procentowych
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)
 
plt.axis('equal')
plt.title("Udział zmian pokrycia terenu (2014 vs 2020)", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig(plot_pie_path, dpi=300, bbox_inches='tight', format='jpg')
print(f"Zapisano wykres kołowy: {plot_pie_path}")
plt.close()
 
 
# =============================================================================
# KONIEC
# =============================================================================
print("KONIEC analizy. Wszystkie pliki zostały zapisane.")