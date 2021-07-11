from app.ges_referti.referto_model import RefertoModel


class RefertoController():

    def __init__(self, model: RefertoModel):
        self.model = model

    def cerca_prestazioni(self):
        self.model.qs_prestazioni = self.model.prestazione.objects.filter(esame=self.model.esame_corrente)
