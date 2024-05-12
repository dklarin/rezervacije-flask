from flask import Blueprint, render_template, request
import pygsheets
import re
import json

poslji_podatak = Blueprint('poslji_podatak', __name__, 
                            template_folder='templates')

gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('hihi')
wks = sh.sheet1
column_index = 1

stupac_B_vrijednosti = [value for value in wks.get_col(2) if value]
turisti = set(stupac_B_vrijednosti[1:])

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

# vraća rječnik dana u mjesecu i aktivnih dana u mjesecu
def kreiranje_rjecnika_zauzetosti(lista1, lista2):
    ključevi_json = ['aktivni', 'dani']
    kalendar = [{ključ: vrijednost for ključ, vrijednost in zip(ključevi_json, vrijednosti)} 
                for vrijednosti in zip(lista1, lista2)] 
    return kalendar

@poslji_podatak.route('/posalji_podatak')
def posalji_podatak():

    wks = sh.sheet1   
    sadrzaj_celija = wks.get_all_values()
    sve_retke = wks.get_all_records()

    podatak = request.args.get('tekst')  

    dijelovi = podatak.split(':')  
    print("Dijelovi")
    print(dijelovi)

    kliknuti_datum = dijelovi[0]
    boja = dijelovi[1] 
  
    lista = []
    # Pretraži sadržaj ćelija
    for redak_index, redak in enumerate(sadrzaj_celija, start=1):
        for stupac_index, ćelija in enumerate(redak, start=1):
            if re.search(fr'\b{boja}\b', ćelija, flags=re.IGNORECASE):              
                lista.append(redak_index)  
   
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

    # Ako nema nikakve rezervacije u mjesecu
    # Kreiraj listu od 1 do 30
    if len(dani6) == 0:
        dani6, aktivni = kreiranje_zauzetosti([], 6) 

    rez1 = []
    if len(rjecnik6) == 1:        
        rez1 = rjecnik6[list(rjecnik6.keys())[0]]  
    else:
        rez1 = spajanje_u_ovisnosti(rjecnik6) 
    
    # Ako nema nikakve rezervacije u mjesecu
    # Kreiraj listu praznih stringova
    if len(rez1) == 0:
        rez1 = [""] * 30   
    
    rez2 = []
    if len(rjecnik7) == 1:        
        rez2 = rjecnik7[list(rjecnik7.keys())[0]]
    else:        
        rez2 = spajanje_u_ovisnosti(rjecnik7)
    
    rez3 = []
    if len(rjecnik8) == 1:        
        rez3 = rjecnik8[list(rjecnik8.keys())[0]]
    else:
        rez3 = spajanje_u_ovisnosti(rjecnik8)

    rez4 = []
    if len(rjecnik9) == 1:        
        rez4 = rjecnik9[list(rjecnik9.keys())[0]]
    else:
        rez4 = spajanje_u_ovisnosti(rjecnik9) 

    visak6 = ['', '', '', '', '']
    visak7 = []
    visak8 = ['', '', '']
    visak9 = ['', '', '', '', '', '']

    dani66 = visak6 + dani6
    aktivni66 = visak6 + rez1
    dani77 = visak7 + dani7
    aktivni77 = visak7 + rez2
    dani88 = visak8 + dani8
    aktivni88 = visak8 + rez3
    dani99 = visak9 + dani9
    aktivni99 = visak9 + rez4  
    
    kalendar6 = kreiranje_rjecnika_zauzetosti(aktivni66, dani66)
    kalendar7 = kreiranje_rjecnika_zauzetosti(aktivni77, dani77)
    kalendar8 = kreiranje_rjecnika_zauzetosti(aktivni88, dani88)
    kalendar9 = kreiranje_rjecnika_zauzetosti(aktivni99, dani99)

    def pronalazak_aktive(kalendar, visak):
        # Pronađi indeks prvog rječnika s "aktivni" ključem postavljenim na "active" nakon indeksa 20
        indeks_prvog_active_nakon_16 = None
        for i in range(int(kliknuti_datum[8:10]) + visak, len(kalendar)):
            if kalendar[i]["aktivni"] == "active":
                indeks_prvog_active_nakon_16 = i
                print("Indeks prvog rječnika s aktivnim ključem nakon indeksa 20:", indeks_prvog_active_nakon_16)
                zadnji_slobodan_datum = kalendar[indeks_prvog_active_nakon_16]["dani"]
                break            
            else:
                print("Nema više aktive")
                print(kalendar[-1]["dani"])
                zadnji_slobodan_datum = kalendar[-1]["dani"]
        return str(zadnji_slobodan_datum)
  
    if kliknuti_datum[5:7] == '06':      
        zadnji_slobodan_datum = pronalazak_aktive(kalendar6, 4)
        zadnji_slobodan_datum = '06-' + zadnji_slobodan_datum
    elif kliknuti_datum[5:7] == '07':
        zadnji_slobodan_datum = pronalazak_aktive(kalendar7, 0)
        zadnji_slobodan_datum = '07-' + zadnji_slobodan_datum
    elif kliknuti_datum[5:7] == '08':
        zadnji_slobodan_datum = pronalazak_aktive(kalendar8, 2)
        zadnji_slobodan_datum = '08-' + zadnji_slobodan_datum
    else:
        zadnji_slobodan_datum = pronalazak_aktive(kalendar9, 5)     
        zadnji_slobodan_datum = '09-' + zadnji_slobodan_datum

    apartman = ['tamnoplavi', 
            'smeđi', 
            'stan', 
            'svijetloplavi', 
            'zeleni']

    akontacije = ['Da', 'Ne']

    # Izvlačenje sljedećeg rednog broja
    column_values = wks.get_col(column_index, include_tailing_empty=False)
    last_value = column_values[-1]
    redni_broj = int(last_value) + 1

    zadnji_slobodan_datum = '2024-' + zadnji_slobodan_datum

    return render_template('nova_rezervacija.html',
                            redni_broj=redni_broj, 
                            gosti=turisti, 
                            dolazak=kliknuti_datum, 
                            odlazak=zadnji_slobodan_datum,
                            apartmani=apartman, 
                            boja=boja, 
                            akontacije=akontacije)
