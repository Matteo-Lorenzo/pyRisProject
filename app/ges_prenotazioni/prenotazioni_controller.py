from app.ges_prenotazioni.prenotazioni_model import PrenotazioniModel


class PrenotazioniController():

    def __init__(self, model: PrenotazioniModel):
        self.model = model
