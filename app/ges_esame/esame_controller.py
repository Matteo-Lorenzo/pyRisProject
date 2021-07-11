from app.ges_esame.esame_model import EsameModel
from datetime import datetime, date

from app.utils import Ambiente


class EsameController():

    def __init__(self, model: EsameModel):
        self.model = model

    def carica_worklist_esecuzione(self, modalita=None):
        start = datetime.combine(date.today(), datetime.min.time())  # Dalla mezzanotte di oggi
        stop = datetime.combine(date.today(), datetime.max.time())  # Alle 23•59 di oggi
        if modalita is None:
            self.model.qs_esami = self.model.esame.objects.filter(attrezzatura__in=Ambiente.modalita_correnti, stato_avanzamento__gte=2, stato_avanzamento__lte=3,
                                                              data_ora_schedulato__range=[start, stop])
        else:
            self.model.qs_esami = self.model.esame.objects.filter(attrezzatura=modalita, stato_avanzamento__gte=2, stato_avanzamento__lte=3,
                                                                  data_ora_schedulato__range=[start, stop])
