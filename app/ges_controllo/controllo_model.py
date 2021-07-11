from store.models import Esame


class ControlloModel():
    def __init__(self):
        self.esame = Esame

        self.qs_esami = None
        self.modalita = []

        self.esame_corrente = self.esame()
