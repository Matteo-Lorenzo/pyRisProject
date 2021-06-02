import orm_setup
import xml.etree.ElementTree as ET

from store.models import Radiologia, Paziente

# Your script code

radiologia = Radiologia.objects.all().first()

tree = ET.parse('/Users/matteolorenzo/Desktop/anagrafica.xml')
root = tree.getroot()

#for x in range(0):
#    anagrafica = root[x]
for anagrafica in root:
    p = Paziente()
    #p.nome
    p.radiologia = radiologia
    p.codice_paziente = anagrafica.find('Codice').text
    p.codice_fiscale = anagrafica.find('CodFiscale').text
    p.tessera_sanitaria = anagrafica.find('CodiceReg').text
    p.cognome = anagrafica.find('SoloCognome').text
    p.nome = anagrafica.find('SoloNome').text
    if anagrafica.find('DataNascita').text != '0000-00-00':
        p.data_nascita = anagrafica.find('DataNascita').text
    if anagrafica.find('Sesso').text == '0':
        p.sesso = "M"
    else:
        p.sesso = "F"
    p.indirizzo = anagrafica.find('Indirizzo').text
    p.cap = anagrafica.find('CAP').text
    p.citta = anagrafica.find('Citta').text
    p.provincia = anagrafica.find('Provincia').text
    p.email = anagrafica.find('email').text
    p.telefono = anagrafica.find('Telefono').text
    p.anamnesi_remota = anagrafica.find('AnamnesiRemota').text
    p.save()
    print(p.codice_paziente)


