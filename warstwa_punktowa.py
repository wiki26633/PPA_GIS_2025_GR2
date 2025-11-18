import arcpy

arcpy.env.workspace = r"C:\Users\wiki2\Documents\PP_aplikacjeGIS\Mój_projekt\Mój_projekt.gdb"
warstwa_punktowa = "GDA2020OT_OIPR_P" #"GDA2020_OT_OIPR_P_COPY"

def odczytywanie_wspolrzednych(warstwa):
    lista_wsp =[]
    with arcpy.da.SearchCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            #print(f'{row[0]}, {row[1]}')
            lista_wsp.append([row[0], row[1]])
    return lista_wsp


def aktualizacja_wspolrzednych(warstwa):
    lista_wsp =[]
    with arcpy.da.UpdateCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            #print(f'{row[0]}, {row[1]}')
            row[0] += 1000
            row[1] += 1000      
            cursor.updateRow(row)

def wstawianie_wspolrzednych(warstwa, lista_wsp):
    lista_wsp =[]
    with arcpy.da.InsertCursor(warstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
        for wsp in lista_wsp:    
           # cursor.insertRow([wsp[0], wsp[1]])
           cursor.insertRow(wsp)
         
    
#lista_wsp_pkt = odczytywanie_wspolrzednych(warstwa_punktowa)[:100]
##tworzenie nowej pustej warstwy
#nowa_warstwa_pkt = "GDA2020_OT_OIPR_P_100Pierwszych"
#arcpy.management.CreateFeatureclass(arcpy.env.workspace, nowa_warstwa_pkt, "POINT","", "DISABLED","DISABLED" ,warstwa_punktowa)


##aktualizacja_wspolrzednych(warstwa_punktowa)
#aktualizacja_wspolrzednych(nowa_warstwa_pkt, lista_wsp_pkt)
##puscic ten kod z wyzej z tym co zakomentowaneP
##przetwarzanie pliku tekstowego warstwy punktowej
dz,dy,dz = 470879,741121,0
with open('data.txt,r') as f:
    points = [
    [float(v)+dx if i ==0 else
     float(v)+dy if i==1 else
     float(v)+dz
     for line in f
     if line.strip() and not line.startswith('#') and len(line.split())==3
    ]]
print("Koniec")