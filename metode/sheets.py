import pygsheets

def plahte():
    gc = pygsheets.authorize(service_file='creds.json')
    sh = gc.open('baza')
    wks = sh.sheet1
    return wks