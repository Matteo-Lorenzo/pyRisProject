from app.ges_archivio.archivio_model import ArchivioModel


class ArchivioController():

    def __init__(self, model: ArchivioModel):
        self.model = model

    def cerca_prestazioni(self):
        self.model.qs_prestazioni = self.model.prestazione.objects.filter(esame=self.model.esame_corrente)
