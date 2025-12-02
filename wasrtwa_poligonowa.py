import arcpy


# =============================================================================
# KONFIGURACJA DANYCH WEJŚCIOWYCH
# =============================================================================
arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"
warstwa_poligonowa = "Budynek"

## [Linia1[pkt1[x1, y1], pkt2[x2, y2]....], Linia2[]...]
## [Poligon1[graniece[pkt1[x1, y1], pkt2[x2, y2]....], dziure[pkt1[x1, y1], pkt2[x2, y2]....]], ...]
def odczytywanie_wspolrzednych_poligonu(warstwa):
    lista_ob = []
    lista_centr = []
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:
            # print(row)
            lista_centr.append(row[1])
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
    return lista_ob, lista_centr

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

listaPOLIGONU, listaCENTROID = odczytywanie_wspolrzednych_poligonu(warstwa_poligonowa)

print(listaPOLIGONU)
print(listaCENTROID)

i = 0
for ob in listaPOLIGONU:
    for part in ob:
        for pkt in part:
            pkt[0] = (pkt[0] - listaCENTROID[i][0])*(0.5+i*0.1) + listaCENTROID[i][0]
            pkt[1] = (pkt[1] - listaCENTROID[i][1])*(0.5+i*0.1) + listaCENTROID[i][1]
    i += 1

print(listaPOLIGONU)
print(listaCENTROID)
NowyBudynek = "Budynki02"
wstawianie_wspolrzednych_poligonu(NowyBudynek, warstwa_poligonowa, listaPOLIGONU)

print("KONIEC")