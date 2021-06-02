from enum import Enum


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
