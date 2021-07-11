from PyQt5.QtGui import QCloseEvent

from .refertazione_controller import RefertazioneController
from .refertazione_model import RefertazioneModel
from .refertazione_ui import Ui_Refertazione
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate

from ..ges_referti.referto_controller import RefertoController
from ..ges_referti.referto_model import RefertoModel
from ..ges_referti.referto_view import RefertoView
from ..utils import Stati, Ambiente, Applicazioni as App
from datetime import datetime
from django.utils import timezone

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class RefertazioneView(Ui_Refertazione, QWidget):
    def __init__(self, model: RefertazioneModel, controller: RefertazioneController, parent=None):
        super(RefertazioneView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.dalla_data.setDate(datetime.today())
        self.alla_data.setDate(datetime.today())
        self.rb_tutti.setChecked(True)
        self.user_capabilities()
        delegate = QStyledItemDelegate()
        self.diagnostiche.setItemDelegate(delegate)
        self.diagnostiche.addItem('Tutte le Modalità', -1)
        for attrezzatura in Ambiente.modalita_correnti:
            self.diagnostiche.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)
        self.inizializza_lista_refertazione()
        self.aggiorna_worklist()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente refertazione')
        Ambiente.stati[App.REFERTAZIONE.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.REFERTAZIONE.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def inizializza_lista_refertazione(self):
        self.lista_refertazione.setColumnCount(6)
        self.lista_refertazione.setHorizontalHeaderLabels(['Codice paziente', 'Nome', 'Codice Esame', 'Descrizione', 'Data Esame', 'Modalità'])
        self.lista_refertazione.setColumnWidth(0, 105)
        self.lista_refertazione.setColumnWidth(1, 290)
        self.lista_refertazione.setColumnWidth(2, 100)
        self.lista_refertazione.setColumnWidth(3, 400)
        self.lista_refertazione.setColumnWidth(4, 170)
        self.lista_refertazione.setColumnWidth(5, 105)

    def aggiorna_worklist(self):
        print(self.urgenti.isChecked(), self.rb_tutti.isChecked(), self.rb_specialista.isChecked(), self.rb_spec_non_attrib.isChecked())
        if self.diagnostiche.currentIndex() == 0:
            diagnostica = None
        else:
            diagnostica = Ambiente.modalita_correnti[self.diagnostiche.currentIndex()-1]
        self.controller.carica_worklist_refertazione(diagnostica, self.dalla_data.date().toPyDate(),
                                                     self.alla_data.date().toPyDate(), self.urgenti.isChecked(),
                                                     self.rb_tutti.isChecked(), self.rb_specialista.isChecked(),
                                                     self.rb_spec_non_attrib.isChecked())
        self.lista_refertazione.setRowCount(len(self.model.qs_esami))
        index = 0
        for esame in self.model.qs_esami:
            self.lista_refertazione.setItem(index, 0, QTableWidgetItem(str(esame.paziente.codice_paziente)))
            self.lista_refertazione.setItem(index, 1, QTableWidgetItem(esame.paziente.cognome + ' ' + esame.paziente.nome))
            self.lista_refertazione.setItem(index, 2, QTableWidgetItem(str(esame.codice_esame)))
            self.lista_refertazione.setItem(index, 3, QTableWidgetItem(esame.descrizione_esame))
            if esame.data_ora_completato is not None:
                self.lista_refertazione.setItem(index, 4, QTableWidgetItem(esame.data_ora_completato.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            if esame.attrezzatura is not None:
                self.lista_refertazione.setItem(index, 5, QTableWidgetItem(esame.attrezzatura.dicom_ae_title))
            index = index + 1

    def referta_esame(self):
        #  Funzione che richiama la dialog di refertazione popolandola con i dati già esistenti
        self.model.esame_corrente = self.model.qs_esami[self.lista_refertazione.currentRow()]
        referto_model = RefertoModel(self.model.esame_corrente)  # passo l'esame corrente al referto
        referto_controller = RefertoController(referto_model)
        referto_view = RefertoView(referto_model, referto_controller)
        if referto_view.exec_():
            self.aggiorna_worklist()

    def user_capabilities(self):
        self.groupBox.setEnabled(Ambiente.utente_corrente.tipo == 'MED')
        if Ambiente.utente_corrente.tipo == 'MED':
            self.titolo.setText('Worklist di Refertazione')
        else:
            self.titolo.setText('Worklist di Trascrizione')
