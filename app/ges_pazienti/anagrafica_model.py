import orm_setup
from django.forms import model_to_dict
from store.models import Paziente


class AnagraficaModel():

    def __init__(self):
        self.paziente = Paziente  # Il prototipo del paziente preso dal modello django
        self.qs = None  # Il QuerySet per le ricerche
        self.paziente_corrente = self.paziente()  # Un oggetto della classe paziente
        self.originale = None  # Una variabile ausiliaria per tenersi una copia e fare il controllo del modificato

    def setta_originale(self):  # Copia sotto forma di dizionario il paziente corrente al momento della chiamata del metodo
        self.originale = model_to_dict(self.paziente_corrente)
        print(self.originale)

    def is_modified(self):  # Notifica se sono state fatte modifiche ai dati
        print(self.originale)
        print(model_to_dict(self.paziente_corrente))
        if self.originale is None:
            return False
        return self.originale != model_to_dict(self.paziente_corrente)
