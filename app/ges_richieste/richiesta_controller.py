from app.ges_richieste.richiesta_model import RichiestaModel


class RichiestaController():

    def __init__(self, model: RichiestaModel):
        self.model = model
