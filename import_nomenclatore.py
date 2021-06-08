import orm_setup
import xml.etree.ElementTree as ET

from store.models import NomenclatorePrestazioni, Metodica, Apparato, Organo

tree = ET.parse('/Users/matteolorenzo/Desktop/da_importare/nomenclatore.xml')
root = tree.getroot()

def import_nomenclatore():
    NomenclatorePrestazioni.objects.all().delete()
    for nomenclatore in root:

        codice = nomenclatore.find('CodPrestazione').text
        metodica = int(nomenclatore.find('Metodica').text)
        apparato = nomenclatore.find('Apparato').text
        organo = int(nomenclatore.find('Organo').text)
        esame = int(nomenclatore.find('Esame').text)
        descrizione = nomenclatore.find('Descrizione').text

        if metodica > 0 and organo != 0 and esame != 0:
            met = Metodica.objects.filter(codice=metodica).first()
            app = Apparato.objects.filter(metodica=met).filter(codice=apparato).first()
            org = Organo.objects.filter(apparato=app).filter(codice=organo).first()
            n = NomenclatorePrestazioni()
            n.codice_interno = codice
            n.metodica = met
            n.apparato = app
            n.organo = org
            n.esame = esame
            n.descrizione = descrizione
            n.tempo_esecuzione = int(nomenclatore.find('TempoEsame').text)
            n.save()
            print(descrizione)


if __name__ == '__main__':
    import_nomenclatore()
