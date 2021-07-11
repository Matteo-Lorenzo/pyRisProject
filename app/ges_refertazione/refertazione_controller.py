from app.ges_refertazione.refertazione_model import RefertazioneModel
from django.db.models import Q
from datetime import datetime, date
from django.utils import timezone

from app.utils import Ambiente


class RefertazioneController():

    def __init__(self, model: RefertazioneModel):
        self.model = model

    def carica_worklist_refertazione(self, diagnostica, dalla_data, alla_data, urgenti, tutti, specialista, specialista_non_attrib):
        start = datetime.combine(dalla_data, datetime.min.time()).astimezone(timezone.get_default_timezone())
        stop = datetime.combine(alla_data, datetime.max.time()).astimezone(timezone.get_default_timezone())
        self.model.qs_esami = self.model.esame.objects.filter(stato_avanzamento=4, data_ora_completato__range=[start, stop])
        if diagnostica is not None:
            self.model.qs_esami = self.model.qs_esami.filter(attrezzatura=diagnostica)
        if urgenti:
            self.model.qs_esami = self.model.qs_esami.filter(flag_urgente=True)
        if tutti:
            pass
        if specialista:
            self.model.qs_esami = self.model.qs_esami.filter(medico_esecutore=Ambiente.utente_corrente)
        if specialista_non_attrib:
            self.model.qs_esami = self.model.qs_esami.filter(Q(medico_esecutore=Ambiente.utente_corrente) | Q(medico_esecutore=None))
