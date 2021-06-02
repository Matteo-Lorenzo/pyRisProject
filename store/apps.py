from django.apps import AppConfig
import datetime
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_migrate


def inizializzazione(sender, **kwargs):
    from .models import Utente
    from .models import Radiologia
    from .models import Modality
    from .models import SalaDiagnostica
    from .models import Attrezzatura

    modalities = [{'modality': 'RX', 'desc': 'Radiologia Convenzionale'},
                  {'modality': 'CT', 'desc': 'Tomografia assiale'},
                  {'modality': 'MR', 'desc': 'Risonanza magnetica'},
                  {'modality': 'US', 'desc': 'Ecografia'},
                  ]

    sale = [
        {'nome': 'Diagnostica RX', 'desc': 'Sala Raggi'},
        {'nome': 'Diagnostica CT', 'desc': 'Sala TAC'},
        {'nome': 'Diagnostica MR', 'desc': 'Sala Risonanza'},
        {'nome': 'Diagnostica US', 'desc': 'Sala Ecografia'},
    ]

    attrazzatura = [
        {'marca': 'MegaCorp', 'modello': 'RX123', 'descrizione': 'Digitale Diretta', 'modality': 'RX',
         'sala': 'Diagnostica RX', 'ae': 'AERX01'},
        {'marca': 'MegaCorp', 'modello': 'CT391', 'descrizione': 'TAC Multislice', 'modality': 'CT',
         'sala': 'Diagnostica CT', 'ae': 'AECT01'},
        {'marca': 'MegaCorp', 'modello': 'MR9911', 'descrizione': 'Risonanza 1.5  Tesla', 'modality': 'MR',
         'sala': 'Diagnostica MR', 'ae': 'AEMR01'},
        {'marca': 'MegaCorp', 'modello': 'US4C1', 'descrizione': 'Ecografo 3D', 'modality': 'US',
         'sala': 'Diagnostica US', 'ae': 'AEUS01'},
    ]

    for elem in modalities:
        if not Modality.objects.filter(sigla=elem['modality']).exists():
            m = Modality()
            m.sigla = elem['modality']
            m.descrizione = elem['desc']
            m.save()

    # creazione radiologia
    if not Radiologia.objects.filter(nome='RADIOLOGIA').exists():
        r = Radiologia()
        r.nome = 'RADIOLOGIA'
        r.ragione_sociale = 'Centro Radiologico'
        r.save()

    # cur_rad = Radiologia.objects.get(nome='RADIOLOGIA')

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
            a.modality = Modality.objects.get(sigla=equipment['modality'])
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
        u.tipo = 'MED'
        u.skill_referti = 'W'
        u.flag_accettazione_clinica = True
        u.flag_revisione_referto = True
        u.flag_firma_referto = True
        u.flag_completamento_esame = True
        u.flag_schedulazione_esame = True
        u.save()

    print("Configurazione iniziale attiva")


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        post_migrate.connect(inizializzazione, sender=self)
