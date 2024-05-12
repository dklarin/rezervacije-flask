from flask import Blueprint, render_template, request, redirect
from datetime import datetime

from metode.sheets import plahte

dodaj_rezervaciju = Blueprint('dodaj_rezervaciju', __name__,
                              template_folder='templates')

wks = plahte()

@dodaj_rezervaciju.route('/nova_rezervacija/', methods=['get', 'post'])
# TODO
def hihi():
    
    stupac_redni_broj = [value for value in wks.get_col(1) if value]
    posljednja_vrijednost = stupac_redni_broj[-1]
    redni_broj = int(posljednja_vrijednost) + 1   

    stupac_gosti = [value for value in wks.get_col(2) if value]
    gosti = set(stupac_gosti[1:])   

    # TODO
    apartman = ['tamnoplavi', 
                'smeđi', 
                'stan', 
                'svijetloplavi', 
                'zeleni']

    # TODO
    akontacije = ['Da', 'Ne']

    # TODO
    if request.method == 'POST':
        
        gost = request.form['gost']
        apartman = request.form['apartman']

        dolazak = request.form['dolazak']
        datum = datetime.strptime(str(dolazak), '%Y-%m-%d')
        dolazak = datum.strftime('%d.%m.%Y')

        odlazak = request.form['odlazak']
        datum = datetime.strptime(str(odlazak), '%Y-%m-%d')
        odlazak = datum.strftime('%d.%m.%Y') 

        potvrda = request.form['potvrda']   
        predujam = request.form['akontac']     
        placeno = request.form['placeno']  

        novi_red = [redni_broj, gost, apartman, dolazak, odlazak, potvrda, predujam, placeno]
        wks.insert_rows(row=redni_broj, values=[novi_red])    

        # Da ne radi dupli POST prilikom osvježavanja stranice
        return redirect("/nova_rezervacija")
    
    return render_template('nova_rezervacija.html', 
                           gosti=gosti, 
                           redni_broj=redni_broj, 
                           apartmani=apartman, 
                           akontacije=akontacije) 
