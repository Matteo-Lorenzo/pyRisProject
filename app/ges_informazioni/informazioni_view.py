from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from store.models import Paziente, Esame
from .informazioni_ui import Ui_Dialog_informazioni
from ..utils import Stati, Ambiente, Applicazioni as App
from django.utils import timezone

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class InformazioniView(Ui_Dialog_informazioni, QDialog):
    def __init__(self, esame_corrente, parent=None):
        super(InformazioniView, self).__init__(parent)
        self.setupUi(self)
        self.esame_corrente : Esame = esame_corrente
        self.setWindowTitle(f'Paziente: {str(self.esame_corrente.paziente.codice_paziente)} {self.esame_corrente.paziente.cognome} {self.esame_corrente.paziente.nome}     Nato il: {self.esame_corrente.paziente.data_nascita.strftime("%d/%m/%Y")}')
        self.popola()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente informazioni')
        event.accept()

    def annulla(self):
        self.close()

    def popola(self):
        if self.esame_corrente.data_ora_prenotato is not None:
            self.data_ora_prenotato.setEnabled(True)
            self.data_ora_prenotato.setDateTime(self.esame_corrente.data_ora_prenotato.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.prenotato_da is not None:
            self.prenotato_da.setText(self.esame_corrente.prenotato_da.username)
        if self.esame_corrente.data_ora_accettato is not None:
            self.data_ora_accettato.setEnabled(True)
            self.data_ora_accettato.setDateTime(self.esame_corrente.data_ora_accettato.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.accettato_da is not None:
            self.accettato_da.setText(self.esame_corrente.accettato_da.username)
        if self.esame_corrente.data_ora_schedulato is not None:
            self.data_ora_schedulato.setEnabled(True)
            self.data_ora_schedulato.setDateTime(self.esame_corrente.data_ora_schedulato.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.schedulato_da is not None:
            self.schedulato_da.setText(self.esame_corrente.schedulato_da.username)
        if self.esame_corrente.data_ora_inizio is not None:
            self.data_ora_iniziato.setEnabled(True)
            self.data_ora_iniziato.setDateTime(self.esame_corrente.data_ora_inizio.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.iniziato_da is not None:
            self.iniziato_da.setText(self.esame_corrente.iniziato_da.username)
        if self.esame_corrente.data_ora_completato is not None:
            self.data_ora_completato.setEnabled(True)
            self.data_ora_completato.setDateTime(self.esame_corrente.data_ora_completato.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.completato_da is not None:
            self.completato_da.setText(self.esame_corrente.completato_da.username)
        if self.esame_corrente.data_ora_trascrizione is not None:
            self.data_ora_trascritto.setEnabled(True)
            self.data_ora_trascritto.setDateTime(self.esame_corrente.data_ora_trascrizione.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.trascritto_da is not None:
            self.trascritto_da.setText(self.esame_corrente.trascritto_da.username)
        if self.esame_corrente.data_ora_firma is not None:
            self.data_ora_firmato.setEnabled(True)
            self.data_ora_firmato.setDateTime(self.esame_corrente.data_ora_firma.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.firmato_da is not None:
            self.firmato_da.setText(self.esame_corrente.firmato_da.username)
        if self.esame_corrente.data_ora_consegna is not None:
            self.data_ora_consegnato.setEnabled(True)
            self.data_ora_consegnato.setDateTime(self.esame_corrente.data_ora_consegna.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.consegnato_da is not None:
            self.consegnato_da.setText(self.esame_corrente.consegnato_da.username)
        if self.esame_corrente.data_ora_annullato is not None:
            self.data_ora_annullato.setEnabled(True)
            self.data_ora_annullato.setDateTime(self.esame_corrente.data_ora_annullato.astimezone(timezone.get_default_timezone()))
        if self.esame_corrente.annullato_da is not None:
            self.annullato_da.setText(self.esame_corrente.annullato_da.username)
        if self.esame_corrente.consegnato_a is not None:
            self.consegnato_a.setText(self.esame_corrente.consegnato_a)
        if self.esame_corrente.data_ora_consegna is not None:
            self.data_ora_consegna.setEnabled(True)
            self.data_ora_consegna.setDateTime(self.esame_corrente.data_ora_consegna.astimezone(timezone.get_default_timezone()))
