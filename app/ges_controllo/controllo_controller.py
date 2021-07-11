from app.ges_controllo.controllo_model import ControlloModel
from django.utils import timezone
from datetime import datetime


class ControlloController():

    def __init__(self, model: ControlloModel):
        self.model = model

    def carica_worklist_controllo(self, diagnostica, dalla_data, alla_data, acc_non_es, es_non_ref, ref_non_fir):
        start = datetime.combine(dalla_data, datetime.min.time()).astimezone(timezone.get_default_timezone())
        stop = datetime.combine(alla_data, datetime.max.time()).astimezone(timezone.get_default_timezone())
        self.model.qs_esami = self.model.esame.objects.all()
        if diagnostica is not None:
            self.model.qs_esami = self.model.qs_esami.filter(attrezzatura=diagnostica)
        if acc_non_es:
            self.model.qs_esami = self.model.qs_esami.filter(stato_avanzamento__gte=1, stato_avanzamento__lte=3, data_ora_schedulato__range=[start, stop])
        if es_non_ref:
            self.model.qs_esami = self.model.qs_esami.filter(stato_avanzamento=4, data_ora_completato__range=[start, stop])
        if ref_non_fir:
            self.model.qs_esami = self.model.qs_esami.filter(stato_avanzamento=5, data_ora_trascrizione__range=[start, stop])
