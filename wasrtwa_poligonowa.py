import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"D:\GIS\Rok_2025_26\PPA_ArcGIS\PPA_Gr2.gdb"
warstwa_poligonowa = "Budynek"

# =============================================================================
# DEFINIOWAINE FUNKCJI DLA WARSTWY PUNKTOWEJ
# =============================================================================

## [Linia1[pkt1[x1, y1], pkt2[x2, y2]....], Linia2[]...]
## [Poligon1[graniece[pkt1[x1, y1], pkt2[x2, y2]....], dziure[pkt1[x1, y1], pkt2[x2, y2]....]], ...]
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@"]) as cursor:
        for row in cursor:
            # print(row)
            list_part = []
            for part in row[0]:
                # print(part)
                lista_pkt = []
                for pnt in part:
                    # print(pnt)
                    if pnt:
                        lista_pkt.append([pnt.X, pnt.Y])
                    else:
                        list_part.append(lista_pkt)
                        lista_pkt = []
                list_part.append(lista_pkt)
            lista_ob.append(list_part)
    return lista_ob

def wstawianie_wspolrzednych_poligonu(nowa_warstwa, uklad_wsp, lista_obiektow):
    arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa, "POLYGON", "", "DISABLED", "DISABLED", uklad_wsp)
    with arcpy.da.InsertCursor(nowa_warstwa, ["SHAPE@"]) as cursor:
        pnt = arcpy.Point()
        part = arcpy.Array()
        array = arcpy.Array()
        for ob in lista_obiektow:
            for cze in ob:
                for pkt in cze:
                    pnt.X = pkt[0]
                    pnt.Y = pkt[1]
                    part.add(pnt)
                array.add(part)
                part.removeAll()
            pol = arcpy.Polygon(array)
            array.removeAll()
            # cursor.insertRow([wsp[0], wsp[1]])
            cursor.insertRow([pol])

listaPOLIGONU = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)

print(listaPOLIGONU)

NowyBudynek = "Budynek01"
wstawianie_wspolrzednych_poligonu(NowyBudynek, warstwa_poligonowa, listaPOLIGONU)

print("KONIEC")