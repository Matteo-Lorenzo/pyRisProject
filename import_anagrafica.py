import orm_setup
import xml.etree.ElementTree as ET

from store.models import Radiologia, Paziente
from datetime import datetime

# Your script code

radiologia = Radiologia.objects.all().first()

tree = ET.parse('../da_importare/anagrafica.xml')
root = tree.getroot()

def import_anagrafica():
    Paziente.objects.all().delete()
    for anagrafica in root:
        p = Paziente()
        p.codice_paziente = anagrafica.find('Codice').text
        p.codice_esterno = anagrafica.find('CodiceDipartim').text
        #p.codice_fiscale = anagrafica.find('CodFiscale').text
        p.codice_fiscale = anagrafica.find('CodiceReg').text
        #p.tessera_sanitaria = anagrafica.find('CodiceReg').text
        p.nome = anagrafica.find('SoloNome').text
        p.cognome = anagrafica.find('SoloCognome').text
        if anagrafica.find('DataNascita').text != '0000-00-00':
            p.data_nascita = anagrafica.find('DataNascita').text
        if anagrafica.find('Sesso').text == '0':
            p.sesso = "M"
        else:
            p.sesso = "F"
        p.comune_nascita = anagrafica.find('ComuneNascita').text
        p.codice_comune_nascita = anagrafica.find('CodComuneNasc').text

        p.indirizzo_residenza = anagrafica.find('Indirizzo').text
        p.cap_residenza = anagrafica.find('CAP').text
        p.comune_residenza = anagrafica.find('Citta').text
        p.provincia_residenza = anagrafica.find('Provincia').text

        p.indirizzo_domicilio = anagrafica.find('IndirDom').text
        p.cap_domicilio = anagrafica.find('CapDom').text
        p.comune_domicilio = anagrafica.find('CittaDom').text
        p.provincia_domicilio = anagrafica.find('ProvDom').text

        p.email = anagrafica.find('email').text
        p.telefono = anagrafica.find('Telefono').text
        p.anamnesi_remota = anagrafica.find('AnamnesiRemota').text
        p.radiologia = radiologia
        p.save()
        print(p.codice_paziente)

if __name__ == '__main__':
    import_anagrafica()
