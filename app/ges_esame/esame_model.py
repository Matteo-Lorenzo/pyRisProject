from store.models import Esame


class EsameModel():
    def __init__(self):
        self.esame = Esame

        self.qs_esami = None

        self.esame_corrente = self.esame()
