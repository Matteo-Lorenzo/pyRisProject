import orm_setup
import xml.etree.ElementTree as ET

from store.models import Radiologia, Paziente, Esame, Utente

radiologia = Radiologia.objects.all().first()

tree = ET.parse('/Users/matteolorenzo/Desktop/da_importare/referti.xml')
root = tree.getroot()


def import_esami():
    Esame.objects.all().delete()
    for esame in root:
        e = Esame()
        e.codice_esame = esame.find('CodiceReferto').text
        e.study_instace_uid = esame.find('StudyInstanceUID').text
        e.paziente = Paziente.objects.filter(codice_paziente=esame.find('CodicePz').text).first()
        e.radiologia = radiologia
        e.anamnesi = esame.find('Anamnesi').text
        e.contenuto_richiesta = esame.find('ContenutoRichiesta').text
        e.motivo_esame = esame.find('MotivoEsame').text
        e.descrizione_esame = esame.find('Riassunto').text
        e.stato_avanzamento = 6
        if esame.find('dataRefertato').text != '0000-00-00':
            e.data_ora_refertazione = esame.find('dataRefertato').text
        e.refertato_da = Utente.objects.filter(username=esame.find('Refertato_da').text).first()
        e.testo_referto = esame.find('TestoReferto').text
        e.save()

if __name__ == '__main__':
    import_esami()
