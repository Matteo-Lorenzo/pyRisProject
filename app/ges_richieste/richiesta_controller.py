from app.ges_richieste.richiesta_model import RichiestaModel


class RichiestaController():

    def __init__(self, model: RichiestaModel):
        self.model = model

    def cerca_prestazioni(self):
        self.model.qs_prestazioni = self.model.prestazione.objects.filter(esame=self.model.esame_corrente)
