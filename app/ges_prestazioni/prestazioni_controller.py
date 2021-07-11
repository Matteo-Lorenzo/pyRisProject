from app.ges_prestazioni.prestazioni_model import PrestazioniModel


class PrestazioniController():

    def __init__(self, model: PrestazioniModel):
        self.model = model

    def carica_metodiche(self):
        self.model.qs_metodiche = self.model.metodica.objects.all().order_by('codice')

    def carica_apparati(self):
        self.model.qs_apparati = self.model.apparato.objects.filter(metodica=self.model.metodica_corrente).order_by('codice')

    def carica_organi(self):
        self.model.qs_organi = self.model.organo.objects.filter(apparato=self.model.apparato_corrente).order_by('codice')

    def carica_prestazioni(self):
        self.model.qs_prestazioni = self.model.nomenclatore.objects.filter(organo=self.model.organo_corrente).order_by('esame')