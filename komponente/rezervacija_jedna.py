from flask import Blueprint, render_template
from datetime import datetime

from metode.sheets import plahte

pregled_rezervacije = Blueprint('pregled_rezervacije', __name__, 
                                template_folder='templates')

wks = plahte()

@pregled_rezervacije.route('/rezervacija/<broj>', methods=['get', 'post'])
def jedna_rezervacija(broj):

    svi_retci = wks.get_all_records()
 
    trazeni_redak = None
    for redak in svi_retci:
        if redak['redni_broj'] == int(broj):
            trazeni_redak = redak
            break

    dolazak = trazeni_redak['dolazak']
    odlazak = trazeni_redak['odlazak']
  
    datum1 = datetime.strptime(dolazak, "%d.%m.%Y")
    datum2 = datetime.strptime(odlazak, "%d.%m.%Y")

    razlika_datuma = abs(datum2 - datum1)
    broj_noci = razlika_datuma.days      

    ukupno = broj_noci * trazeni_redak['cijena']

    if trazeni_redak['placeno'] != '':    
        doplatiti = ukupno - trazeni_redak['placeno']
    else:
        doplatiti = ukupno
       
    return render_template('rezervacija.html', 
                           trazeni_redak=trazeni_redak,
                           broj_noci=broj_noci, 
                           ukupno=ukupno, 
                           doplatiti=doplatiti
                           )
