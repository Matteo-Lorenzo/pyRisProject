from PyQt5.QtGui import QCloseEvent

from .controllo_controller import ControlloController
from .controllo_model import ControlloModel
from .controllo_ui import Ui_Controllo
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from datetime import datetime
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class ControlloView(Ui_Controllo, QWidget):
    def __init__(self, model: ControlloModel, controller: ControlloController, parent=None):
        super(ControlloView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.dalla_data.setDate(datetime.today())
        self.alla_data.setDate(datetime.today())
        self.rb_acc_non_es.setChecked(True)
        delegate = QStyledItemDelegate()
        self.diagnostiche.setItemDelegate(delegate)
        self.diagnostiche.addItem('Tutte le Modalità', -1)
        self.model.modalita.clear()
        for sala_diagnostica in Ambiente.radiologia_corrente.sale_diagnostiche.all():
            for attrezzatura in sala_diagnostica.attrezzature.all():
                self.model.modalita.append(attrezzatura)
                self.diagnostiche.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)  # tutte le attrezzature del centro radiologico
        self.inizializza_lista_controllo()
        self.aggiorna_worklist()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente controllo')
        Ambiente.stati[App.CONTROLLO.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.CONTROLLO.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def inizializza_lista_controllo(self):
        self.lista_controllo.setColumnCount(5)
        self.lista_controllo.setHorizontalHeaderLabels(['Codice paziente', 'Nome', 'Codice Esame', 'Descrizione', 'Modalità'])
        self.lista_controllo.setColumnWidth(0, 105)
        self.lista_controllo.setColumnWidth(1, 290)
        self.lista_controllo.setColumnWidth(2, 100)
        self.lista_controllo.setColumnWidth(3, 505)
        self.lista_controllo.setColumnWidth(4, 170)

    def aggiorna_worklist(self):
        if self.diagnostiche.currentIndex() == 0:
            diagnostica = None
        else:
            diagnostica = self.model.modalita[self.diagnostiche.currentIndex()-1]
        self.controller.carica_worklist_controllo(diagnostica, self.dalla_data.date().toPyDate(),
                                                     self.alla_data.date().toPyDate(),
                                                     self.rb_acc_non_es.isChecked(), self.rb_es_non_ref.isChecked(),
                                                     self.rb_ref_non_fir.isChecked())
        self.lista_controllo.setRowCount(len(self.model.qs_esami))
        index = 0
        for esame in self.model.qs_esami:
            self.lista_controllo.setItem(index, 0, QTableWidgetItem(str(esame.paziente.codice_paziente)))
            self.lista_controllo.setItem(index, 1, QTableWidgetItem(esame.paziente.cognome + ' ' + esame.paziente.nome))
            self.lista_controllo.setItem(index, 2, QTableWidgetItem(str(esame.codice_esame)))
            self.lista_controllo.setItem(index, 3, QTableWidgetItem(esame.descrizione_esame))
            if esame.attrezzatura is not None:
                self.lista_controllo.setItem(index, 4, QTableWidgetItem(esame.attrezzatura.dicom_ae_title))
            index = index + 1
