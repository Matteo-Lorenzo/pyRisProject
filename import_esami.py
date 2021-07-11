import orm_setup
import xml.etree.ElementTree as ET

from store.models import Radiologia, Paziente, Esame, Utente, Attrezzatura

radiologia = Radiologia.objects.all().first()
attrezzatura = Attrezzatura.objects.all().first()

tree = ET.parse('../da_importare/referti.xml')
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
        # imporatre sala diagnostica
        e.attrezzatura = attrezzatura
        e.sala_diagnostica = attrezzatura.sala_diagnostica
        e.contenuto_richiesta = esame.find('ContenutoRichiesta').text
        e.motivo_esame = esame.find('MotivoEsame').text
        e.descrizione_esame = esame.find('Riassunto').text
        # imporatre flag urgente
        stato = int(esame.find('StatoReferto').text)
        if stato == 0:
            e.stato_avanzamento = 2 #schedulato
        elif stato == 1:
            e.stato_avanzamento = 4 #completato
        elif stato == 2:
            e.stato_avanzamento = 5 #trascritto
        elif stato == 6:
            e.stato_avanzamento = 6 #firmato
        elif stato == 7:
            e.stato_avanzamento = 7 #archiviato

        # Informazioni di prenotazione 0
        if esame.find('dataPrenotazione').text != '0000-00-00':
            e.data_ora_prenotato = esame.find('dataPrenotazione').text + " " + esame.find('oraPrenotazione').text[11:16]
        e.prenotato_da = Utente.objects.filter(username=esame.find('Prenotato_da').text).first()
        # Informazioni di accettazione 1
        if esame.find('dataAccettazione').text != '0000-00-00':
            e.data_ora_accettato = esame.find('dataAccettazione').text + " " + esame.find('oraAccettazione').text[11:16]
        e.accettato_da = Utente.objects.filter(username=esame.find('Accettato_da').text).first()
        # Informazioni di schedulazione 2
        if esame.find('dataCheckIn').text != '0000-00-00':
            e.data_ora_schedulato = esame.find('dataCheckIn').text + " " + esame.find('oraCheckIn').text[11:16]
        e.schedulato_da = Utente.objects.filter(username=esame.find('CheckIn_da').text).first()
        # Informazioni inizio 3
        #   nulla da importare
        # Informazioni completamento 4
        if esame.find('dataCompleto').text != '0000-00-00':
            e.data_ora_completato = esame.find('dataCompleto').text + " " + esame.find('oraCompleto').text[11:16]
        e.completato_da = Utente.objects.filter(username=esame.find('Completato_da').text).first()
        # Informazioni trascrizione 5
        if esame.find('dataRefertato').text != '0000-00-00':
            e.data_ora_trascrizione = esame.find('dataRefertato').text + " " + esame.find('oraRefertato').text[11:16]
        e.trascritto_da = Utente.objects.filter(username=esame.find('Refertato_da').text).first()
        e.testo_referto = esame.find('TestoReferto').text
        # Informazioni firma 6
        if esame.find('dataFirmato').text != '0000-00-00':
            e.data_ora_firma = esame.find('dataFirmato').text + " " + esame.find('oraFirmato').text[11:16]
        e.firmato_da = Utente.objects.filter(username=esame.find('Firmato_da').text).first()
        # Informazioni consegna elaborati 7
        if esame.find('DataConsegna').text != '0000-00-00':
            e.data_ora_consegna = esame.find('DataConsegna').text + " " + esame.find('oraConsegna').text[11:16]
        e.consegnato_da = Utente.objects.filter(username=esame.find('Consegnato_da').text).first()
        e.save()
if __name__ == '__main__':
    import_esami()
