from flask import Blueprint, render_template
import pygsheets

from metode.sheets import plahte

pregled_rezervacija = Blueprint('pregled_rezervacija', __name__, 
                                template_folder='templates')

wks = plahte()

@pregled_rezervacija.route('/rezervacije/', methods=['get', 'post'])
def sve_rezervacije():  

    svi_retci = wks.get_all_records()    
        
    # TODO
    return render_template('rezervacije.html', sve_retke=svi_retci)
