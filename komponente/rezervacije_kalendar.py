from flask import Blueprint, render_template
import re

from metode.sheets import plahte
from metode.kalendar import dolazak_odlazak, kreiranje_zauzetosti, spajanje_u_ovisnosti, izvlacenje_aktivnih

kalendar = Blueprint('kalendar', __name__,
                         template_folder='templates')

wks = plahte() 

# vraća rječnik dana u mjesecu i aktivnih dana u mjesecu
def kreiranje_rjecnika_zauzetosti(lista1, lista2):
    ključevi_json = ['aktivni', 'dani']
    kalendar = [{ključ: vrijednost for ključ, vrijednost in zip(ključevi_json, vrijednosti)} 
                for vrijednosti in zip(lista1, lista2)] 
    return kalendar

# kreiranje rječnika s mjesecima
key = 'mjesec'
mjesec = ['Lipanj', 'Srpanj', 'Kolovoz', 'Rujan']
mjeseci = []
for i in range(len(mjesec)):
    mjeseci.append({key: mjesec[i]})

# lista apartmana
apartman = ['tamnoplavi', 
            'smeđi', 
            'stan', 
            'svijetloplavi', 
            'zeleni']

link = ['/calendar/tamnoplavi', 
        '/calendar/smeđi',
        '/calendar/stan',
        '/calendar/svijetloplavi',
        '/calendar/zeleni'
        ]

kljucevi_json = ['link', 'apartman']
linkovi = [{kljuc: vrijednost for kljuc, vrijednost in zip(kljucevi_json, vrijednosti)} 
                for vrijednosti in zip(link, apartman)] 

# GLAVNA RUTA
@kalendar.route('/calendar/<color>')
def haha(color):

    sadrzaj_celija = wks.get_all_values()
    sve_retke = wks.get_all_records()

    lista = []
    # Pretraži sadržaj ćelija
    for redak_index, redak in enumerate(sadrzaj_celija, start=1):
        for stupac_index, ćelija in enumerate(redak, start=1):
            if re.search(fr'\b{color}\b', ćelija, flags=re.IGNORECASE):              
                lista.append(redak_index)  
   
    rjecnik6 = {}
    rjecnik7 = {}
    rjecnik8 = {}
    rjecnik9 = {}

    dani6 = []
    dani7 = []
    dani8 = []
    dani9 = []

    '''for i in range(len(lista)):
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
            rjecnik9['lista' + str(i)] = aktivni9'''
    
    rjecnik6, rjecnik7, rjecnik8, rjecnik9, dani6, dani7, dani8, dani9 = izvlacenje_aktivnih(sve_retke, lista)
    

    
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
        
    return render_template('calendar.html',
                           linkovi=linkovi, 
                           apartman=apartman, 
                           boja=color, 
                           mjeseci=mjeseci, 
                           kalendar6=kalendar6, 
                           kalendar7=kalendar7, 
                           kalendar8=kalendar8, 
                           kalendar9=kalendar9                     
                           )
