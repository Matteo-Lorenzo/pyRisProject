import orm_setup
import xml.etree.ElementTree as ET

from store.models import Radiologia, Utente

radiologia = Radiologia.objects.all().first()

tree = ET.parse('/Users/matteolorenzo/Desktop/da_importare/utenti.xml')
root = tree.getroot()

def import_utenti():
    for utente in root:
        u = Utente.objects.filter(username=utente.find('UserID').text).first()
        if (u is None):
            u = Utente()
            print(utente.find('UserID').text)
            u.username = utente.find('UserID').text
            u.radiologia = radiologia
            u.is_active = (utente.find('Disattivo').text == 'false')
            u.last_name = utente.find('Nome').text
            tipologia = utente.find('Tipologia').text
            # 1 = medico
            # 2 = tecnico
            # 3 = infermiere
            # 4 = amministrativo
            # 5 = Personale di Supporto
            # 6 = medico non strutturato(specializzando)
            if tipologia == '5':
                u.tipo = 'AMS'
            if tipologia == '1':
                u.tipo = 'MED'
                u.flag_firma_referto = True
                u.flag_revisione_referto = True
                u.flag_accettazione_clinica = True
            if tipologia == '2':
                u.tipo = 'TEC'
                u.flag_completamento_esame = True
                u.flag_schedulazione_esame = True
            if tipologia == '4':
                u.tipo = 'AMM'
                u.flag_schedulazione_esame = True
                u.flag_accettazione_clinica = True
            if tipologia == '3':
                u.tipo = 'INF'
                u.flag_schedulazione_esame = True
                u.flag_accettazione_clinica = True
                u.fla
            u.save()

if __name__ == '__main__':
    import_utenti()


