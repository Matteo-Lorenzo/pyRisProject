from store.models import Metodica, Apparato, Organo, NomenclatorePrestazioni


class PrestazioniModel():

    def __init__(self):
        self.metodica = Metodica  # Il prototipo della Metodica preso dal modello django
        self.apparato = Apparato  # Il prototipo dell'Apparato
        self.organo = Organo  # Il prototipo dell'Organo
        self.nomenclatore = NomenclatorePrestazioni  # Il prototipo del Nomenclatore
        # Queryset per effettuare le ricerche
        self.qs_metodiche = None
        self.qs_apparati = None
        self.qs_organi = None
        self.qs_prestazioni = None
        # Oggetti correnti delle classi sopra riportate, valorizzati di volta in volta dopo una selezione
        self.metodica_corrente = self.metodica()
        self.apparato_corrente = self.apparato()
        self.organo_corrente = self.organo()
        self.prestazione_corrente = self.nomenclatore()
