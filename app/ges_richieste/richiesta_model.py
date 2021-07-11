from store.models import Esame, Prestazione, SalaDiagnostica, Attrezzatura, Utente


class RichiestaModel():
    def __init__(self, esame_corrente: Esame):
        self.prestazione = Prestazione
        self.utente = Utente

        self.qs_prestazioni = None
        self.qs_sale_diagnostiche = None
        self.qs_attrezzature = None
        self.qs_medici = None
        self.qs_tecnici = None

        self.esame_corrente = esame_corrente  # L'esame corrente passato dall'esterno su cui lavorare
