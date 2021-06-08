import orm_setup
import xml.etree.ElementTree as ET

from store.models import Metodica, Apparato, Organo

tree = ET.parse('/Users/matteolorenzo/Desktop/da_importare/nomenclatore.xml')
root = tree.getroot()

def import_metodiche():
    for nomenclatore in root:
        codice = nomenclatore.find('CodPrestazione').text
        metodica = int(nomenclatore.find('Metodica').text)
        apparato = nomenclatore.find('Apparato').text
        organo = int(nomenclatore.find('Organo').text)
        esame = int(nomenclatore.find('Esame').text)
        descrizione = nomenclatore.find('Descrizione').text

        if metodica < 0:
            print('Metodica: ' + descrizione)
            metodica = -metodica
            met = Metodica.objects.filter(codice=metodica).first()
            if (met is None):
                met = Metodica()
                print(f'Creo la metodica {descrizione}')
                met.codice = metodica
                met.descrizione = descrizione
                met.save()


def import_apparto():
    Apparato.objects.all().delete()
    for nomenclatore in root:
        codice = nomenclatore.find('CodPrestazione').text
        metodica = int(nomenclatore.find('Metodica').text)
        apparato = nomenclatore.find('Apparato').text
        organo = int(nomenclatore.find('Organo').text)
        esame = int(nomenclatore.find('Esame').text)
        descrizione = nomenclatore.find('Descrizione').text

        if metodica > 0 and organo == 0 and esame == 0:
            met = Metodica.objects.filter(codice=metodica).first()
            print(f'Metodica: {met.descrizione} Appaarato: {descrizione}')
            app = Apparato()
            app.codice = apparato
            app.descrizione = descrizione
            app.metodica = met
            app.save()


def import_organo():
    Organo.objects.all().delete()
    for nomenclatore in root:
        codice = nomenclatore.find('CodPrestazione').text
        metodica = int(nomenclatore.find('Metodica').text)
        apparato = nomenclatore.find('Apparato').text
        organo = int(nomenclatore.find('Organo').text)
        esame = int(nomenclatore.find('Esame').text)
        descrizione = nomenclatore.find('Descrizione').text

        if metodica > 0 and apparato != 0 and organo != 0 and esame == 0:
            met = Metodica.objects.filter(codice=metodica).first()
            app = Apparato.objects.filter(metodica=met).filter(codice=apparato).first()
            org = Organo()
            org.codice = organo
            org.descrizione = descrizione
            org.apparato = app
            org.save()

if __name__ == '__main__':
    import_metodiche()
    import_apparto()
    import_organo()
