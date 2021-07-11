import orm_setup
from django.forms import model_to_dict
from store.models import Paziente, Esame


class AnagraficaModel():

    def __init__(self):
        self.paziente = Paziente  # Il prototipo del paziente preso dal modello django
        self.esame = Esame  # Il prototipo dell'esame
        self.qs_pazienti = None  # Il QuerySet per le ricerche dei pazienti
        self.qs_richieste = None
        self.qs_refertazione = None
        self.qs_archivio = None
        self.paziente_corrente = self.paziente()  # Un oggetto della classe Paziente
        self.esame_corrente = self.esame()  # Un oggetto della classe Esame
        self.originale = None  # Una variabile ausiliaria per tenersi una copia e fare il controllo del modificato

    def setta_originale(self):  # Copia sotto forma di dizionario il paziente corrente al momento della chiamata del metodo
        self.originale = model_to_dict(self.paziente_corrente)
        print(self.originale)

    def is_modified(self):  # Notifica se sono state fatte modifiche ai dati
        print(self.originale)  # Stampe per avere un po' di console logging
        print(model_to_dict(self.paziente_corrente))  # Stampe per avere un po' di console logging
        if self.originale is None:
            return False
        return self.originale != model_to_dict(self.paziente_corrente)
