import datetime

from django.apps import AppConfig
from django.db.models.signals import post_migrate



def create_required_objects(sender, **kwargs):
    from .models import Utente
    from .models import Radiologia
    from .models import SalaDiagnostica
    from .models import Attrezzatura
    from django.contrib.auth.hashers import make_password





    sale = [
            {'nome': 'Diagnostica RX', 'desc': 'Sala Raggi'},
            {'nome': 'Diagnostica CT', 'desc': 'Sala TAC'},
            {'nome': 'Diagnostica MR', 'desc': 'Sala Risonanza'},
            {'nome': 'Diagnostica US', 'desc': 'Sala Ecografia'},
          ]

    attrazzatura = [
        {'marca': 'MegaCorp', 'modello': 'RX123', 'descrizione': 'Digitale Diretta', 'modality': 'RX', 'sala': 'Diagnostica RX', 'ae': 'AERX01'},
        {'marca': 'MegaCorp', 'modello': 'CT391', 'descrizione': 'TAC Multislice', 'modality': 'CT', 'sala': 'Diagnostica CT', 'ae': 'AECT01'},
        {'marca': 'MegaCorp', 'modello': 'MR9911', 'descrizione': 'Risonanza 1.5  Tesla', 'modality': 'MR', 'sala': 'Diagnostica MR', 'ae': 'AEMR01'},
        {'marca': 'MegaCorp', 'modello': 'US4C1', 'descrizione': 'Ecografo 3D', 'modality': 'US', 'sala': 'Diagnostica US', 'ae': 'AEUS01'},
    ]



    # creazione radiologia
    if not Radiologia.objects.filter(nome='RADIOLOGIA').exists():
        r = Radiologia()
        r.nome = 'RADIOLOGIA'
        r.ragione_sociale = 'Centro Radiologico'
        r.save()

    #cur_rad = Radiologia.objects.get(nome='RADIOLOGIA')

    # creazione sale diagnostiche
    for sala in sale:
        if not SalaDiagnostica.objects.filter(nome=sala['nome']).exists():
            s = SalaDiagnostica()
            s.nome = sala['nome']
            s.descrizione = sala['desc']
            s.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
            s.save()

    # creazione attrezzature
    for equipment in attrazzatura:
        if not Attrezzatura.objects.filter(dicom_ae_title=equipment['ae']).exists():
            a = Attrezzatura()
            a.marca = equipment['marca']
            a.modello = equipment['modello']
            a.descrizione = equipment['descrizione']
            a.modality = equipment['modality']
            a.sala_diagnostica = SalaDiagnostica.objects.get(nome=equipment['sala'])
            a.dicom_ae_title = equipment['ae']
            a.anno_acquisto = datetime.date.today()
            a.save()

    # creazione utenti di default
    if not Utente.objects.filter(username='admin').exists():
        u = Utente()
        u.username = 'admin'
        u.password = make_password('admin')
        u.email = 'admin@admin.com'
        u.is_staff = True
        u.is_superuser = True
        u.is_active = True
        u.save()

    if not Utente.objects.filter(username='medico').exists():
        u = Utente()
        u.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
        u.username = 'medico'
        u.password = make_password('medico')
        u.email = 'medico@medico.com'
        u.first_name = 'Pico'
        u.last_name = 'Della Mirandola'
        u.titolo = 'Dott. '
        u.tipo = 'MED'
        u.skill_referti = 'W'
        u.skill_anagrafica_pazienti = 'W'
        u.flag_accettazione_clinica = True
        u.flag_revisione_referto = True
        u.flag_firma_referto = True
        u.flag_completamento_esame = True
        u.flag_schedulazione_esame = True
        u.flag_cartella_radiologica = True
        u.save()
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica RX'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica CT'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica MR'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica US'))
        u.save()

    if not Utente.objects.filter(username='tecnico').exists():
        u = Utente()
        u.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
        u.username = 'tecnico'
        u.password = make_password('tecnico')
        u.email = 'tecnico@tecnico.com'
        u.first_name = 'Mario'
        u.last_name = 'Rossi'
        u.titolo = ''
        u.tipo = 'TEC'
        u.skill_referti = 'R'
        u.skill_anagrafica_pazienti = 'R'
        u.flag_accettazione_clinica = False
        u.flag_revisione_referto = False
        u.flag_firma_referto = False
        u.flag_completamento_esame = True
        u.flag_schedulazione_esame = False
        u.flag_cartella_radiologica = True
        u.save()
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica RX'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica CT'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica MR'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica US'))
        u.save()

    if not Utente.objects.filter(username='segretaria').exists():
        u = Utente()
        u.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
        u.username = 'segretaria'
        u.password = make_password('segretaria')
        u.email = 'segretaria@segretaria.com'
        u.first_name = 'Anna'
        u.last_name = 'Bianchi'
        u.titolo = ''
        u.tipo = 'AMM'
        u.skill_referti = 'W'
        u.skill_anagrafica_pazienti = 'W'
        u.flag_accettazione_clinica = True
        u.flag_revisione_referto = False
        u.flag_firma_referto = False
        u.flag_completamento_esame = False
        u.flag_schedulazione_esame = True
        u.flag_cartella_radiologica = True
        u.save()
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica RX'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica CT'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica MR'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica US'))
        u.save()

    if not Utente.objects.filter(username='donkey').exists():
        u = Utente()
        u.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
        u.username = 'donkey'
        u.password = make_password('donkey')
        u.email = 'donkey@donkey.com'
        u.first_name = 'Armindo'
        u.last_name = 'Schinchirimini'
        u.titolo = ''
        u.tipo = 'AMM'
        u.skill_referti = 'R'
        u.skill_anagrafica_pazienti = 'R'
        u.flag_accettazione_clinica = True
        u.flag_revisione_referto = False
        u.flag_firma_referto = False
        u.flag_completamento_esame = False
        u.flag_schedulazione_esame = True
        u.flag_cartella_radiologica = False
        u.save()
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica RX'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica CT'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica MR'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica US'))
        u.save()

    if not Utente.objects.filter(username='amministratore').exists():
        u = Utente()
        u.radiologia = Radiologia.objects.get(nome='RADIOLOGIA')
        u.username = 'amministratore'
        u.password = make_password('amministratore')
        u.email = 'amministratore@amministratore.com'
        u.first_name = 'Pino'
        u.last_name = 'Verde'
        u.titolo = ''
        u.tipo = 'AMS'
        u.skill_referti = 'R'
        u.skill_anagrafica_pazienti = 'R'
        u.flag_accettazione_clinica = False
        u.flag_revisione_referto = False
        u.flag_firma_referto = False
        u.flag_completamento_esame = False
        u.flag_schedulazione_esame = False
        u.flag_cartella_radiologica = False
        u.save()
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica RX'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica CT'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica MR'))
        u.sale_diagnostiche.add(SalaDiagnostica.objects.get(nome='Diagnostica US'))
        u.save()

    print("Configurazione iniziale attiva")


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        post_migrate.connect(create_required_objects, sender=self)

