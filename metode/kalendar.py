# vraća datum dolaska i datum odlaska
# vraća i listu datuma u rasponu
def dolazak_odlazak(sve_retke, redak):
    dolazak = sve_retke[redak]['dolazak']
    odlazak = sve_retke[redak]['odlazak']
    lista = []
    for i in range(int(dolazak[0:2]), int(odlazak[0:2]) + 1):
        lista.append(i)
    return dolazak, odlazak, lista

# vraća listu dana u mjesecu
# vraća listu aktivnih dana i praznih stringova
def kreiranje_zauzetosti(lista, mjesec): 
    dani = []
    aktivni = []
    if mjesec == 6 or mjesec == 9:
        broj = 31
    else:
        broj = 32
    
    for i in range(1, broj):
        dani.append(i)
        if i in lista:
            aktivni.append('active')
        else:
            aktivni.append('')
    return dani, aktivni

# vraća spojene dane za određeni mjesec i za određeni apartman
def spajanje_noci_dinamicki(liste):
    
    broj_listi = len(liste)
    rezultat = []

    for elementi in zip(*liste):
        # Provjera za spoj dviju lista
        if broj_listi == 2:
            elem1, elem2 = elementi
            if elem1 == '' and elem2 != '':
                rezultat.append(elem2)
            else:
                rezultat.append(elem1)
        # Provjera za spoj tri liste
        elif broj_listi == 3:
            elem1, elem2, elem3 = elementi
            if elem1 == '' and elem2 != '':
                rezultat.append(elem2)
            elif elem1 == '' and elem3 != '':
                rezultat.append(elem3)
            else:
                rezultat.append(elem1)
        # Provjera za spajanje četiri liste
        elif broj_listi == 4:
            elem1, elem2, elem3, elem4 = elementi
            if elem1 == '' and elem2 != '':
                rezultat.append(elem2)
            elif elem1 == '' and elem3 != '':
                rezultat.append(elem3)
            elif elem1 == '' and elem4 != '':
                rezultat.append(elem4)
            else:
                rezultat.append(elem1)
        # Provjera za spajanje pet lista
        elif broj_listi == 5:
            elem1, elem2, elem3, elem4, elem5 = elementi
            if elem1 == '' and elem2 != '':
                rezultat.append(elem2)
            elif elem1 == '' and elem3 != '':
                rezultat.append(elem3)
            elif elem1 == '' and elem4 != '':
                rezultat.append(elem4)
            elif elem1 == '' and elem5 != '':
                rezultat.append(elem5)
            else:
                rezultat.append(elem1)

    return rezultat

def spajanje_u_ovisnosti(rjecnik):
  
  rezultat = []
  
  if len(rjecnik) == 2:   
    rezultat = spajanje_noci_dinamicki([rjecnik[list(rjecnik.keys())[0]], 
                                        rjecnik[list(rjecnik.keys())[1]]])
  elif len(rjecnik) == 3:
    rezultat = spajanje_noci_dinamicki([rjecnik[list(rjecnik.keys())[0]], 
                                        rjecnik[list(rjecnik.keys())[1]], 
                                        rjecnik[list(rjecnik.keys())[2]]])
  elif len(rjecnik) == 4:
    rezultat = spajanje_noci_dinamicki([rjecnik[list(rjecnik.keys())[0]], 
                                        rjecnik[list(rjecnik.keys())[1]], 
                                        rjecnik[list(rjecnik.keys())[2]], 
                                        rjecnik[list(rjecnik.keys())[3]]])  
  elif len(rjecnik) == 5:
    rezultat = spajanje_noci_dinamicki([rjecnik[list(rjecnik.keys())[0]], 
                                        rjecnik[list(rjecnik.keys())[1]], 
                                        rjecnik[list(rjecnik.keys())[2]], 
                                        rjecnik[list(rjecnik.keys())[3]], 
                                        rjecnik[list(rjecnik.keys())[4]]])  
  else:
    print('Imaš više od 5 rezervacija!')  
  
  return rezultat

def izvlacenje_aktivnih(sve_retke, lista):
    rjecnik6 = {}
    rjecnik7 = {} 
    rjecnik8 = {}
    rjecnik9 = {}
    dani6 = []
    dani7 = []
    dani8 = []
    dani9 = []

    for i in range(len(lista)):
        dolazak, odlazak, lista_dana = dolazak_odlazak(sve_retke, lista[i] - 2)
        # Dolazak i odlazak u 6. mjesecu
        if dolazak[3:5] == '06':
            dani6, aktivni6 = kreiranje_zauzetosti(lista_dana, 6)
            rjecnik6['lista' + str(i)] = aktivni6
        # Dolazak u 6. mjesecu, odlazak u 7. mjesecu
        if dolazak[3:5] == '06' and odlazak[3:5] == '07':
            if int(dolazak[0:2]) <= 30 and dolazak[3:5] == '06':
                lista_brojeva = list(range(int(dolazak[0:2]), 31))
                dani6, aktivni6 = kreiranje_zauzetosti(lista_brojeva, 6)        
                rjecnik6['lista'+ str(i)] = aktivni6
            if int(odlazak[0:2]) >= 1 and odlazak[3:5] == '07':
                lista_brojeva = list(range(1, int(odlazak[0:2]) + 1))
                dani7, aktivni7 = kreiranje_zauzetosti(lista_brojeva, 7)
                rjecnik7['lista' + str(i)] = aktivni7
        # Dolazak i odlazak u 7. mjesecu
        if dolazak[3:5] == '07':
            dani7, aktivni7 = kreiranje_zauzetosti(lista_dana, 7)
            rjecnik7['lista' + str(i)] = aktivni7
        # Dolazak u 7. mjesecu, odlazak u 8. mjesecu
        if dolazak[3:5] == '07' and odlazak[3:5] == '08':
            if int(dolazak[0:2]) <= 31 and dolazak[3:5] == '07':
                lista_brojeva = list(range(int(dolazak[0:2]), 32))
                dani7, aktivni7 = kreiranje_zauzetosti(lista_brojeva, 7)        
                rjecnik7['lista'+ str(i)] = aktivni7
            if int(odlazak[0:2]) >= 1 and odlazak[3:5] == '08':
                lista_brojeva = list(range(1, int(odlazak[0:2]) + 1))
                dani8, aktivni8 = kreiranje_zauzetosti(lista_brojeva, 8)
                rjecnik8['lista' + str(i)] = aktivni8
        # Dolazak i odlazak u 8. mjesecu
        if dolazak[3:5] == '08':
            dani8, aktivni8 = kreiranje_zauzetosti(lista_dana, 8)
            rjecnik8['lista' + str(i)] = aktivni8
        # Dolazak u 8. mjesecu, odlazak u 9. mjesecu
        if dolazak[3:5] == '08' and odlazak[3:5] == '09':
            if int(dolazak[0:2]) <= 31 and dolazak[3:5] == '08':
                lista_brojeva = list(range(int(dolazak[0:2]), 32))
                dani8, aktivni8 = kreiranje_zauzetosti(lista_brojeva, 8)        
                rjecnik8['lista'+ str(i)] = aktivni8
            if int(odlazak[0:2]) >= 1 and odlazak[3:5] == '09':
                lista_brojeva = list(range(1, int(odlazak[0:2]) + 1))
                dani9, aktivni9 = kreiranje_zauzetosti(lista_brojeva, 9)
                rjecnik9['lista' + str(i)] = aktivni9
        # Dolazak i odlazak u 9. mjesecu
        if dolazak[3:5] == '09':
            dani9, aktivni9 = kreiranje_zauzetosti(lista_dana, 9)
            rjecnik9['lista' + str(i)] = aktivni9
        
    return rjecnik6, rjecnik7, rjecnik8, rjecnik9, dani6, dani7, dani8, dani9
    

    