from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

from komponente.rezervacije_kalendar import kalendar
from komponente.posalji_podatak import poslji_podatak
from komponente.rezervacija_dodaj import dodaj_rezervaciju
from komponente.rezervacija_jedna import pregled_rezervacije
from komponente.rezervacije_sve import pregled_rezervacija

app = Flask(__name__)
bootstrap = Bootstrap(app)
datepicker(app)
#datepicker(app=app, local=['static/js/bootstrap.js', 'static/css/bootstrap.solar.min.css'])
#datepicker(app=app, local=['static/js/jquery-ui.js', 'static/css/jquery-ui.css'])
app.register_blueprint(kalendar)
app.register_blueprint(poslji_podatak)
app.register_blueprint(dodaj_rezervaciju)
app.register_blueprint(pregled_rezervacije)
app.register_blueprint(pregled_rezervacija)

# 1. Index
@app.route('/')
def index():
    return render_template('index.html')
# https://localhost:5000

# 5. Control structures - macros
@app.route("/macro-alone/")
def cs_macro_alone():
    comments = ['Odlično', 'Ne razumijem', 'Nije loše']
    return render_template('cs-macro-alone.html', comments=comments)
# http://localhost:5000/macro-alone

# 6. Control structures - import, macros
@app.route("/macro-import/")
def cs_macro_import():
    comments = ['Odlično', 'Ne razumijem', 'Nije loše']
    return render_template('cs-macro-import.html', comments=comments)
# http://localhost:5000/macro-import

@app.route('/links/')
def links():
    links = ['https://www.thegardencroatia.com/event/love-international-2024',
             'https://www.thegardencroatia.com/event/defected-croatia-2024', 
             'https://www.thegardencroatia.com/event/dekmantel-selectors-2024']
    
    ključevi_json = ['link', 'naziv']

    ključevi = ['Love International 2024', 'Defected Croatia 2024', 'Dekmantel Selectors 2024']

    
    # Spajanje ključeva i vrijednosti u obliku rječnika
    rezultat = [{ključ: vrijednost for ključ, vrijednost in zip(ključevi_json, vrijednosti)} for vrijednosti in zip(ključevi, links)]

    return render_template('links.html', links=rezultat)

# template inheritance 1
@app.route("/base/")
def base():
    return render_template('base.html')
# http://localhost:5000/base

# template inheritance 2
@app.route("/base1/")
def base1():
    return render_template('base1.j2')
# http://localhost:5000/base1

# error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# error pages
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)
