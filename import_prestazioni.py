import orm_setup
import xml.etree.ElementTree as ET

from store.models import Prestazione, NomenclatorePrestazioni, Esame

tree = ET.parse('../da_importare/prestazioni.xml')
root = tree.getroot()

def import_prestazioni():
    Prestazione.objects.all().delete()
    for prestazione in root:
        try:
            p = Prestazione()
            n = NomenclatorePrestazioni.objects.get(codice_interno=prestazione.find('Prestazione').text)
            e = Esame.objects.get(codice_esame=prestazione.find('CodiceReferto').text)
            p.esame = e
            p.procedura = n
            p.modificatore = prestazione.find('DescrizioneSpec').text
            p.save()
            print(p)
        except:
            pass


if __name__ == '__main__':
    import_prestazioni()