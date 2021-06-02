from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser

# controllare la __str__ in tutte le classi


class Radiologia(models.Model):
    nome = models.CharField(max_length=32, db_index=True)
    ragione_sociale = models.CharField(max_length=32)
    indirizzo = models.CharField(max_length=32)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=32)
    provincia = models.CharField(max_length=2)
    email = models.EmailField()
    sito_web = models.URLField()
    telefono = models.CharField(max_length=15)
    p_iva = models.CharField(max_length=16)
    responsabile = models.CharField(max_length=32)
    direttore_sanitario = models.CharField(max_length=32)
    descrizione = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Radiologia'
        verbose_name_plural = 'Radiologie'

    def __str__(self):
        return f"{self.nome}"


class Modality(models.Model):
    sigla = models.CharField(max_length=3, db_index=True)
    descrizione = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Modality'
        verbose_name_plural = 'Modalities'

    def __str__(self):
        return f"{self.sigla}"


class SalaDiagnostica(models.Model):
    nome = models.CharField(max_length=32, db_index=True)
    descrizione = models.TextField(blank=True)
    radiologia = models.ForeignKey(Radiologia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sala Diagnostica'
        verbose_name_plural = 'Sale Diagnostiche'

    def __str__(self):
        return f"{self.nome}"


class Attrezzatura(models.Model):
    marca = models.CharField(max_length=32)
    modello = models.CharField(max_length=32)
    descrizione = models.TextField(blank=True)
    anno_acquisto = models.DateField()
    data_ultima_manutenzione = models.DateField(blank=True, null=True)
    data_prossima_manutenzione = models.DateField(blank=True, null=True)
    fermo_macchina = models.BooleanField(default=False)
    fine_fermo_macchina = models.DateField(blank=True, null=True)
    telefono_assistenza_tecnica = models.CharField(max_length=15)
    referente_assistenza_tecnica = models.CharField(max_length=32)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)
    sala_diagnostica = models.ForeignKey(SalaDiagnostica, on_delete=models.CASCADE)
    dicom_ae_title = models.CharField(max_length=16) # nome univoco di quella attrezzatura all'interno del network

    class Meta:
        verbose_name = 'Attrezzatura'
        verbose_name_plural = 'Attrezzature'

    def __str__(self):
        return f"{self.marca}, {self.modello}"

'''
class TipologiaUtente(models.Model): # DA TOGLIERE E FAR DIVENTARE SCELTA MULTIPLA DENTRO UTENTE
    # Elenco tipi utente standard:
    # Amministratore di sistema
    # Medico Radiologo
    # Tecnico di Radiologia
    # Amministrativo
    # Infermiere
    
    tipo = models.CharField(max_length=16, unique=True)
    descrizione = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipologia dell'Utente"
        verbose_name_plural = "Tipologie degli Utenti"
'''

class Utente(AbstractUser):

    # Scelte per il tipo di utente
    TIPO_CHOICES = [
        ('AMS', 'Amministratore di sistema'),
        ('MED', 'Medico Radiologo'),
        ('TEC', 'Tecnico di Radiologia'),
        ('AMM', 'Amministrativo'),
        ('INF', 'Infermiere'),
    ]

    # Scelte per le skills dell'utente
    SKILLS_CHOICES = [
        ('N', 'Nessun Accesso'),
        ('R', 'Lettura'),
        ('W', 'Lettura e Scrittura'),
        ('F', 'Accesso completo'),
    ]

    # tipo = models.ForeignKey(TipologiaUtente, on_delete=models.CASCADE, blank=True, null=True) # vecchio legame con TipologiaUtente
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    titolo = models.TextField(blank=True) # titoli onorifici per far contento il medico refertatore
    radiologia = models.ForeignKey(Radiologia, on_delete=models.CASCADE, blank=True, null=True)
    sale_diagnostiche = models.ManyToManyField(SalaDiagnostica)

    #SKILLS:
    skill_anagrafica_pazienti = models.CharField(max_length=1, choices=SKILLS_CHOICES)
    skill_referti = models.CharField(max_length=1, choices=SKILLS_CHOICES)
    #FLAGS:
    flag_firma_referto = models.BooleanField(default=False)
    flag_revisione_referto = models.BooleanField(default=False)
    flag_schedulazione_esame = models.BooleanField(default=False)
    flag_accettazione_clinica = models.BooleanField(default=False)
    flag_completamento_esame = models.BooleanField(default=False)
    #flag_da_aggiungere varie ed eventuali

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

    def __str__(self):
        return f"{self.username}, {self.tipo}"


class Paziente(models.Model):

    # Scelte per il sesso del paziente
    SESSO_CHOICES = [
        ('N', 'Non Assegnato'),
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    ]

    codice_paziente = models.CharField(max_length=16, db_index=True)
    codice_fiscale = models.CharField(max_length=16, blank=True, null=True)
    tessera_sanitaria = models.CharField(max_length=30, blank=True, null=True)
    nome = models.CharField(max_length=40, db_index=True, blank=True, null=True)
    cognome = models.CharField(max_length=40, db_index=True, blank=True, null=True)
    data_nascita = models.DateField(blank=True, null=True)
    sesso = models.CharField(max_length=1, choices=SESSO_CHOICES, default='N')
    indirizzo = models.CharField(max_length=64, blank=True, null=True)
    cap = models.CharField(max_length=5, blank=True, null=True)
    citta = models.CharField(max_length=64, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=64, blank=True, null=True)
    anamnesi_remota = models.TextField(blank=True, null=True)
    medico_di_base = models.CharField(max_length=32, blank=True, null=True)
    radiologia = models.ForeignKey(Radiologia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Paziente'
        verbose_name_plural = 'Pazienti'
        ordering = ('cognome', 'nome')

    def __str__(self):
        return f"{self.codice_paziente}, {self.cognome}, {self.nome}"


class Preparazione(models.Model):
    nome = models.CharField(max_length=20, db_index=True)
    descrizione = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Preparazione'
        verbose_name_plural = 'Preparazioni'

    def __str__(self):
        return f"{self.nome}"


class NomenclatorePrestazioni(models.Model):
    # Queste sono le prestazioni erogabili (divise per modalità)
    codice_interno = models.CharField(max_length=10)
    codice_ministeriale = models.CharField(max_length=10)
    descrizione = models.CharField(max_length=64)
    tariffa = models.DecimalField(max_digits=6, decimal_places=2)
    tempo_esecuzione = models.DurationField(blank=True, null=True) #espresso in minuti
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)
    preparazioni = models.ManyToManyField(Preparazione)

    class Meta:
        verbose_name = 'Prestazione erogabile'
        verbose_name_plural = 'Prestazioni erogabili'

    def __str__(self):
        return f"{self.codice_interno}, {self.descrizione}"


class Esame(models.Model):
    '''
    # Stati avanzamento esame
    class StatiAvanzamento(models.IntegerChoices):
        PRENOTATO = 0
        ACCETTATO = 1
        SCHEDULATO = 2
        INIZIATO = 3
        COMPLETATO = 4
        REFERTATO = 5
        FIRMATO = 6
        CONSEGNATO = 7
        ANNULLATO = 8
    '''
    # Scelte per il giudizio
    GIUDIZIO_CHOICES = [
        ('NV', 'Non Valutato'),
        ('NEG', 'Negativo'),
        ('POS', 'Positivo'),
    ]

    # Scelte per la qualità
    QUALITA_CHOICES = [
        ('NV', 'Non Valutata'),
        ('BAS', 'Bassa'),
        ('BUO', 'Buona'),
        ('OTT', 'Ottima'),
    ]

    # Scelte per lo stato di avanzamento
    STATO_CHOICES = [
        (0, 'Prenotato'),
        (1, 'Accettato'),
        (2, 'Schedulato'),
        (3, 'Iniziato'),
        (4, 'Completato'),
        (5, 'Refertato'),
        (6, 'Firmato'),
        (7, 'Consegnato'),
        (8, 'Annullato'),
    ]

    # Informazioni generali
    codice_esame = models.CharField(max_length=16, db_index=True) # questo diventa l'accession number DICOM
    study_instace_uid = models.CharField(max_length=100, db_index=True, blank=True)
    paziente = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    radiologia = models.ForeignKey(Radiologia, on_delete=models.CASCADE)
    sala_diagnostica = models.ForeignKey(SalaDiagnostica, on_delete=models.CASCADE)
    anamnesi = models.TextField(blank=True)
    contenuto_richiesta = models.TextField(blank=True)
    motivo_esame = models.TextField(blank=True)
    descrizione_esame = models.TextField(blank=True) # Un sunto delle descrizioni delle varie prestazioni associate
    flag_urgente = models.BooleanField(default=False)
    stato_avanzamento = models.IntegerField(choices=STATO_CHOICES, default=0) # Vedere qui sopra per le fasi
    # Informazioni di prenotazione 0
    data_ora_prenotato = models.DateTimeField(blank=True, null=True)
    prenotato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='prenotato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    # Informazioni di accettazione 1
    data_ora_accettato = models.DateTimeField(blank=True, null=True)
    accettato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='accettato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    # Informazioni di schedulazione 2
    data_ora_schedulato = models.DateTimeField(blank=True, null=True)
    schedulato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='schedulato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    # Informazioni inizio 3
    data_ora_inizio = models.DateTimeField(blank=True, null=True)
    iniziato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='iniziato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    # Informazioni completamento 4
    data_ora_completato = models.DateTimeField(blank=True, null=True)
    completato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='completato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    # Informazioni refertazione 5
    data_ora_refertazione = models.DateTimeField(blank=True, null=True)
    refertato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='refertato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    testo_referto = models.TextField(blank=True)
    giudizio = models.CharField(max_length=3, choices=GIUDIZIO_CHOICES, default='NV') # Positivo | Negativo | Non valutato
    qualita_esame = models.CharField(max_length=3, choices=QUALITA_CHOICES, default='NV') # Non Valutata | Bassa | Buona | Ottima
    impressioni = models.TextField(blank=True) # Un'aggiunta al referto che potrebbe anche non essere stampata
    # Informazioni firma 6
    data_ora_firma = models.DateTimeField(blank=True, null=True)
    firmato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='firmato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    flag_firma_digitale = models.BooleanField(default=False)
    # Informazioni consegna elaborati 7
    flag_produzione_CD = models.BooleanField(default=False) # se True deve essere prodotto in automatico
    data_ora_consegna = models.DateTimeField(blank=True, null=True)
    consegnato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='consegnato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)
    consegnato_a = models.TextField(blank=True)
    # Informazioni annullamento 8
    data_ora_annullato = models.DateTimeField(blank=True, null=True)
    annullato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, related_name='annullato_da', to_field=Utente.USERNAME_FIELD, blank=True, null=True)

    class Meta:
        verbose_name = 'Esame'
        verbose_name_plural = 'Esami'

    def __str__(self):
        return f"{self.codice_esame}, {self.descrizione_esame}"


class Prestazione(models.Model):
    prestazione = models.ForeignKey(NomenclatorePrestazioni, on_delete=models.CASCADE)
    modificatore = models.CharField(max_length=16, blank=True)
    commento = models.TextField(blank=True)
    esame = models.ForeignKey(Esame, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'

    def __str__(self):
        return f"{self.esame.codice_esame}, {self.prestazione.descrizione}"


class Revisione(models.Model):

    # Scelte per il tipo di revisione
    TIPO_CHOICES = [
        ('I', 'Integrativa'),
        ('S', 'Sostitutiva'),
        ('A', 'Annullativa'),
    ]

    esame = models.ForeignKey(Esame, on_delete=models.CASCADE)
    numero_revisione = models.IntegerField() # se esiste, la numero O è la copia originale del referto (quindi con 1 revisione ci sono almeno 2 record)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='I') # I (integrativa), S (sostitutiva), A (annullativa)
    data_ora = models.DateTimeField(auto_now_add=True)
    testo = models.TextField()
    revisionato_da = models.ForeignKey(Utente, on_delete=models.DO_NOTHING, to_field=Utente.USERNAME_FIELD)

    class Meta:
        verbose_name = 'Revisione'
        verbose_name_plural = 'Revisioni'

    def __str__(self):
        return f"{self.esame.codice_esame}, {self.numero_revisione}"


class Frasario(models.Model):
    nome = models.CharField(max_length=32)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, to_field=Utente.USERNAME_FIELD)

    class Meta:
        verbose_name = 'Frasario'
        verbose_name_plural = 'Frasari'

    def __str__(self):
        return f"{self.nome}, {self.utente.USERNAME_FIELD}"


class Organo(models.Model):
    nome = models.CharField(max_length=32)
    frasario = models.ForeignKey(Frasario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Organo'
        verbose_name_plural = 'Organi'

    def __str__(self):
        return f"{self.nome}, {self.frasario.nome}"


class Frase(models.Model):
    nome = models.CharField(max_length=32)
    organo = models.ForeignKey(Organo, on_delete=models.CASCADE)
    testo_predefinito = models.TextField()

    class Meta:
        verbose_name = 'Frase'
        verbose_name_plural = 'Frasi'

    def __str__(self):
        return f"{self.nome}, {self.organo.nome}"
