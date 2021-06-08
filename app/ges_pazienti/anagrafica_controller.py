from app.ges_pazienti.anagrafica_model import AnagraficaModel


class AnagraficaController():

    def __init__(self, model: AnagraficaModel):
        self.model = model

    def cerca_paziente(self, codice_paziente, cognome, nome):
        # Metodo per la ricerca dei pazienti, popola il QuerySet con i pazienti che soddisfano i criteri di ricerca
        print(f'{codice_paziente} {cognome} {nome}')
        if codice_paziente != '':
            self.model.qs_pazienti = self.model.paziente.objects.filter(codice_paziente=codice_paziente)
        else:
            self.model.qs_pazienti = self.model.paziente.objects.filter(cognome__istartswith=cognome, nome__istartswith=nome)
        self.model.originale = None  # Fatta una nuova ricerca risetto a nullo il modello originale per il confronto

    def cerca_richieste(self):
        self.model.qs_richieste = self.model.esame.objects.filter(paziente=self.model.paziente_corrente)  # Aggiungere altro filtro di selezione dello stato

    def cerca_refertazione(self):
        self.model.qs_refertazione = self.model.esame.objects.filter(paziente=self.model.paziente_corrente)  # Aggiungere altro filtro di selezione dello stato

    def cerca_archivio(self):
        self.model.qs_archivio = self.model.esame.objects.filter(paziente=self.model.paziente_corrente)  # Aggiungere altro filtro di selezione dello stato