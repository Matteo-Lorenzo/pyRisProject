from enum import Enum

from store.models import Utente, Radiologia, AziendaRefertazione, SalaDiagnostica, Attrezzatura


class Stati(Enum):
    APERTO = 1
    MODIFICATO = 2
    CHIUSO = 3


class Applicazioni(Enum):
    GESTIONE_PAZIENTI = 'gestionepazienti'
    PRENOTAZIONI = 'prenotazioni'
    CONSEGNA = 'consegna'
    PREFERENZE = 'preferenze'
    ESECUZIONE_ESAME = 'esecuzioneesame'
    REFERTAZIONE = 'refertazione'
    FIRMA = 'firma'
    CONTROLLO = 'controllo'


class Ambiente():
    # Possibili stati: aperto | chiuso | modificato
    stati = {
        'gestionepazienti': Stati.CHIUSO,
        'prenotazioni': Stati.CHIUSO,
        'consegna': Stati.CHIUSO,
        'preferenze': Stati.CHIUSO,
        'esecuzioneesame': Stati.CHIUSO,
        'refertazione': Stati.CHIUSO,
        'firma': Stati.CHIUSO,
        'controllo': Stati.CHIUSO,
    }
    # Un ambiente di default che si popola quando viene effettuato il login
    app = None
    utente_corrente: Utente = None
    radiologia_corrente: Radiologia = None
    azienda_refertazione_corrente: AziendaRefertazione = None
    sale_diagnostiche_correnti: SalaDiagnostica = None
    modalita_correnti = []
    main_window = None
    visualizzazione = {'stile': "Fusion",
                       'tema': "scuro"}
    piattaforma = ''

    @staticmethod
    def set_ambiente():
        Ambiente.radiologia_corrente = Ambiente.utente_corrente.radiologia
        Ambiente.azienda_refertazione_corrente = Ambiente.utente_corrente.azienda_refertazione
        Ambiente.sale_diagnostiche_correnti = Ambiente.utente_corrente.sale_diagnostiche.all()
        Ambiente.modalita_correnti.clear()
        for sala_diagnostica in Ambiente.sale_diagnostiche_correnti:
            for attrezzatura in sala_diagnostica.attrezzature.all():
                Ambiente.modalita_correnti.append(attrezzatura)
