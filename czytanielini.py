import arcpy

# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"
warstwa_2014 = "GDA2014OT_SWRS_L"
warstwa_2020 = "GDA2020OT_SWRS_L"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================
def odczytywanie_wspolrzednych_linii_do_listy(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            print(row)
            list_pkt = []
            for part in row[0]:
                print(part)
                for pnt in part:
                    print(pnt.X, pnt.Y)
                    list_pkt.append([pnt.X, pnt.Y])
            lista_ob.append(list_pkt)
    return lista_ob

def wstawianie_wspolrzednych_linii(nowa_warstwa, uklad_wsp, lista_obiektow):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POLYLINE", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nowa_warstwa, ["SHAPE@"]) as cursor:
        pnt = arcpy.Point()
        array = arcpy.Array()
        for ob in lista_obiektow:
            for pkt in ob:
                pnt.X = pkt[0]
                pnt.Y = pkt[1]
                array.add(pnt)
            pol = arcpy.Polyline(array)
            array.removeAll()
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow([pol])


lista_2014 = odczytywanie_wspolrzednych_linii_do_listy(warstwa_2014)
lista_2020 = odczytywanie_wspolrzednych_linii_do_listy(warstwa_2020)

from collections import defaultdict

from collections import defaultdict

def compare_points_to_list(lista_2014, lista_2020, tolerance=0.01):
    """
    Zwraca listę wszystkich unikalnych punktów w formacie:
    [[x, y, 'both'], [x, y, '2020_only'], [x, y, '2014_only'], ...]
    """
    # Słownik: klucz = zaokrąglone współrzędne, wartość = (oryginalny punkt, zbiór lat)
    point_dict = {}
    
    def rounded(p):
        return (round(p[0] / tolerance) * tolerance,
                round(p[1] / tolerance) * tolerance)
    
    # Przetwarzamy 2014
    for line in lista_2014:
        for point in line:
            key = rounded(point)
            if key not in point_dict:
                point_dict[key] = (point, set())
            point_dict[key][1].add(2014)  # dodajemy rok
    
    # Przetwarzamy 2020
    for line in lista_2020:
        for point in line:
            key = rounded(point)
            if key not in point_dict:
                point_dict[key] = (point, set())
            point_dict[key][1].add(2020)
            # Aktualizujemy oryginalny punkt (z 2020, jeśli istnieje)
            point_dict[key] = (point, point_dict[key][1])
    
    # Tworzymy wynikową listę
    result = []
    for (x, y), years_set in point_dict.values():
        if 2014 in years_set and 2020 in years_set:
            tag = 'both'
        elif 2014 in years_set:
            tag = '2014_only'
        else:
            tag = '2020_only'
        result.append([x, y, tag])
    
    return result

# print(lista_wsp[-1])
# print(len(lista_wsp))

# thinned_lines = [
#     line if len(line) <= 2 else line[::2] + ([line[-1]] if len(line) % 2 == 0 else [])
#     for line in lista_wsp
# ]

lista_roznic = compare_points_to_list(lista_2014, lista_2020, tolerance=0.01)
print(lista_roznic)
# wstawianie_wspolrzednych("Centroidy_SWRS_01", warstwa_liniowa, lista_wsp)
# wstawianie_wspolrzednych_linii("Linie_SWRS_04", warstwa_liniowa, thinned_lines)

print("KONIEC")