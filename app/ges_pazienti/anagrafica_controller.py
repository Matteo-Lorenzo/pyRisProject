from app.ges_pazienti.anagrafica_model import AnagraficaModel


class AnagraficaController():

    def __init__(self, model: AnagraficaModel):
        self.model = model

    def cerca_paziente(self, codice_paziente, cognome, nome):
        # Metodo per la ricerca dei pazienti, popola il QuerySet con i pazienti che soddisfano i criteri di ricerca
        print(f'{codice_paziente} {cognome} {nome}')
        if codice_paziente != '':
            self.model.qs = self.model.paziente.objects.filter(codice_paziente=codice_paziente)
        else:
            self.model.qs = self.model.paziente.objects.filter(cognome__istartswith=cognome, nome__istartswith=nome)
        self.model.originale = None  # Fatta una nuova ricerca risetto a nullo il modello originale per il confronto
