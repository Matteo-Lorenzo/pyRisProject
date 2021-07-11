from PyQt5.QtGui import QCloseEvent

from .firma_controller import FirmaController
from .firma_model import FirmaModel
from .firma_ui import Ui_Firma
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from datetime import datetime, timedelta
from django.utils import timezone

from ..ges_referti.referto_controller import RefertoController
from ..ges_referti.referto_model import RefertoModel
from ..ges_referti.referto_view import RefertoView
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class FirmaView(Ui_Firma, QWidget):
    def __init__(self, model: FirmaModel, controller: FirmaController, parent=None):
        super(FirmaView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.dalla_data.setDate(datetime.today() - timedelta(days=7))
        self.alla_data.setDate(datetime.today())
        delegate = QStyledItemDelegate()
        self.diagnostiche.setItemDelegate(delegate)
        self.diagnostiche.addItem('Tutte le Modalità', -1)
        for attrezzatura in Ambiente.modalita_correnti:
            self.diagnostiche.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)
        self.inizializza_lista_firma()
        self.aggiorna_worklist()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente firma referto')
        Ambiente.stati[App.FIRMA.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        Ambiente.stati[App.FIRMA.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.FIRMA.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def inizializza_lista_firma(self):
        self.lista_firma.setColumnCount(6)
        self.lista_firma.setHorizontalHeaderLabels(['Codice paziente', 'Nome', 'Codice Esame', 'Descrizione', 'Data Esame', 'Modalità'])
        self.lista_firma.setColumnWidth(0, 105)
        self.lista_firma.setColumnWidth(1, 290)
        self.lista_firma.setColumnWidth(2, 100)
        self.lista_firma.setColumnWidth(3, 400)
        self.lista_firma.setColumnWidth(4, 170)
        self.lista_firma.setColumnWidth(5, 105)

    def aggiorna_worklist(self):
        if self.diagnostiche.currentIndex() == 0:
            diagnostica = None
        else:
            diagnostica = Ambiente.modalita_correnti[self.diagnostiche.currentIndex()-1]
        self.controller.carica_worklist_firma(diagnostica, self.dalla_data.date().toPyDate(),
                                                     self.alla_data.date().toPyDate(), self.urgenti.isChecked())
        self.lista_firma.setRowCount(len(self.model.qs_esami))
        index = 0
        for esame in self.model.qs_esami:
            self.lista_firma.setItem(index, 0, QTableWidgetItem(str(esame.paziente.codice_paziente)))
            self.lista_firma.setItem(index, 1, QTableWidgetItem(esame.paziente.cognome + ' ' + esame.paziente.nome))
            self.lista_firma.setItem(index, 2, QTableWidgetItem(str(esame.codice_esame)))
            self.lista_firma.setItem(index, 3, QTableWidgetItem(esame.descrizione_esame))
            if esame.data_ora_completato is not None:
                self.lista_firma.setItem(index, 4, QTableWidgetItem(esame.data_ora_completato.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            if esame.attrezzatura is not None:
                self.lista_firma.setItem(index, 5, QTableWidgetItem(esame.attrezzatura.dicom_ae_title))
            index = index + 1

    def firma_esame(self):
        #  Funzione che richiama la dialog di refertazione popolandola con i dati già esistenti
        self.model.esame_corrente = self.model.qs_esami[self.lista_firma.currentRow()]
        referto_model = RefertoModel(self.model.esame_corrente)  # passo l'esame corrente al referto
        referto_controller = RefertoController(referto_model)
        referto_view = RefertoView(referto_model, referto_controller)
        if referto_view.exec_():
            self.aggiorna_worklist()

    def firma_in_blocco(self):
        for index in self.lista_firma.selectedIndexes():
            esame = self.model.qs_esami[index.row()]
            esame.firmato_da = Ambiente.utente_corrente
            esame.data_ora_firma = timezone.localtime()
            esame.stato_avanzamento = 6
            esame.save()
        self.aggiorna_worklist()
