from app.ges_firma.firma_model import FirmaModel
from datetime import datetime, date
from django.utils import timezone

from app.utils import Ambiente


class FirmaController():

    def __init__(self, model: FirmaModel):
        self.model = model

    def carica_worklist_firma(self, diagnostica, dalla_data, alla_data, urgenti):
        start = datetime.combine(dalla_data, datetime.min.time()).astimezone(timezone.get_default_timezone())
        stop = datetime.combine(alla_data, datetime.max.time()).astimezone(timezone.get_default_timezone())
        self.model.qs_esami = self.model.esame.objects.filter(stato_avanzamento=5, data_ora_completato__range=[start, stop], medico_esecutore=Ambiente.utente_corrente)
        if diagnostica is not None:
            self.model.qs_esami = self.model.qs_esami.filter(attrezzatura=diagnostica)
        if urgenti:
            self.model.qs_esami = self.model.qs_esami.filter(flag_urgente=True)
