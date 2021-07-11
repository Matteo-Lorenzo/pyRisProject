from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog, QStyledItemDelegate, QTableWidgetItem
from datetime import datetime
from django.utils import timezone

from .archivio_controller import ArchivioController
from .archivio_model import ArchivioModel
from .archivio_ui import Ui_Dialog_Archivio
from ..ges_informazioni.informazioni_view import InformazioniView
from ..utils import Stati, Ambiente


class ArchivioView(Ui_Dialog_Archivio, QDialog):
    def __init__(self, model: ArchivioModel, controller: ArchivioController, parent=None):
        super(ArchivioView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)  # All'apertura di una richiesta mostro i dati relativi all'esame
        self.stato = Stati.CHIUSO
        self.inizializza_schede_archivio()
        self.popola()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura dialog archivio')
        self.stato = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # Non c'è più bisogno di salvare nulla a questo punto
        self.accept()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if self.stato == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def inizializza_schede_archivio(self):
        # Settaggio dei ComboBox per le selte
        delegate = QStyledItemDelegate()
        self.classe_dose_cumulativa.setItemDelegate(delegate)
        index = 0
        for dose in ['', 'I Classe', 'II Classe', 'III Classe', 'IV Classe']:  # Costruzione ComboBox dose cumulativa
            self.classe_dose_cumulativa.addItem(dose, index)
            index = index + 1
        # Popolare i comboBox tramite Query al DB

    def popola(self):
        self.codice_paziente.setText(str(self.model.esame_corrente.paziente.codice_paziente))
        self.nome_paziente.setText(self.model.esame_corrente.paziente.cognome + ' ' + self.model.esame_corrente.paziente.nome)
        self.codice_esame.setText(str(self.model.esame_corrente.codice_esame))
        self.data_firmato.setDate(self.model.esame_corrente.data_ora_firma.date())
        # tab Referto
        self.descrizione_esame.setText(self.model.esame_corrente.descrizione_esame)
        self.testo_referto.setPlainText(self.model.esame_corrente.testo_referto)
        self.medico_refertatore.setText(f'{self.model.esame_corrente.firmato_da.titolo} {self.model.esame_corrente.firmato_da.first_name} {self.model.esame_corrente.firmato_da.last_name}')
        if self.model.esame_corrente.tecnico_esecutore is not None:
            self.tecnico_esecutore.setText(f'{self.model.esame_corrente.tecnico_esecutore.titolo} {self.model.esame_corrente.tecnico_esecutore.first_name} {self.model.esame_corrente.tecnico_esecutore.last_name}')
        if self.model.esame_corrente.classe_dose_cumulativa is not None:
            self.classe_dose_cumulativa.setCurrentIndex(self.classe_dose_cumulativa.findData(QVariant(self.model.esame_corrente.classe_dose_cumulativa)))
        else:
            self.classe_dose_cumulativa.setCurrentIndex(-1)
        # tab Dati generici
        self.codice_esterno.setText(self.model.esame_corrente.id_cup)
        if self.model.esame_corrente.data_richiesta is not None:
            self.data_richiesta.setDate(self.model.esame_corrente.data_richiesta)
        self.impegnativa.setText(self.model.esame_corrente.numero_impegnativa)
        self.medico_richiedente.setText(self.model.esame_corrente.medico_richiedente)
        # tab Anamnesi
        self.text_anamnesi.setPlainText(self.model.esame_corrente.anamnesi)
        self.text_contenuto_richiesta.setPlainText(self.model.esame_corrente.contenuto_richiesta)
        self.text_motivo_esame.setPlainText(self.model.esame_corrente.motivo_esame)

    def stampa(self):
        print('Sto stampando il referto')

    def mostra_informazioni(self):
        informazioni_view = InformazioniView(self.model.esame_corrente)
        informazioni_view.exec_()
