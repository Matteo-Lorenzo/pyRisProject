from PyQt5.QtGui import QCloseEvent

from .esame_controller import EsameController
from .esame_model import EsameModel
from .esame_ui import Ui_Esame
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate

from ..ges_richieste.richiesta_controller import RichiestaController
from ..ges_richieste.richiesta_model import RichiestaModel
from ..ges_richieste.richiesta_view import RichiestaView
from ..utils import Stati, Ambiente, Applicazioni as App
from django.utils import timezone

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class EsameView(Ui_Esame, QWidget):
    def __init__(self, model: EsameModel, controller: EsameController, parent=None):
        super(EsameView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        delegate = QStyledItemDelegate()
        self.diagnostiche.setItemDelegate(delegate)
        self.diagnostiche.addItem('Tutte le Modalità', -1)
        for attrezzatura in Ambiente.modalita_correnti:
            self.diagnostiche.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)
        self.inizializza_lista_esecuzione()
        self.aggiorna_worklist()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente esecuzione esame')
        Ambiente.stati[App.ESECUZIONE_ESAME.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.ESECUZIONE_ESAME.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def inizializza_lista_esecuzione(self):
        self.lista_esecuzione.setColumnCount(6)
        self.lista_esecuzione.setHorizontalHeaderLabels(['Codice paziente', 'Nome', 'Codice Esame', 'Descrizione', 'Schedulazione', 'Modalità'])
        self.lista_esecuzione.setColumnWidth(0, 105)
        self.lista_esecuzione.setColumnWidth(1, 290)
        self.lista_esecuzione.setColumnWidth(2, 100)
        self.lista_esecuzione.setColumnWidth(3, 400)
        self.lista_esecuzione.setColumnWidth(4, 170)
        self.lista_esecuzione.setColumnWidth(5, 105)

    def aggiorna_worklist(self):
        if self.diagnostiche.currentIndex() == 0:
            self.controller.carica_worklist_esecuzione()
        else:
            self.controller.carica_worklist_esecuzione(Ambiente.modalita_correnti[self.diagnostiche.currentIndex()-1])
        self.lista_esecuzione.setRowCount(len(self.model.qs_esami))
        index = 0
        for esame in self.model.qs_esami:
            self.lista_esecuzione.setItem(index, 0, QTableWidgetItem(str(esame.paziente.codice_paziente)))
            self.lista_esecuzione.setItem(index, 1, QTableWidgetItem(esame.paziente.cognome + ' ' + esame.paziente.nome))
            self.lista_esecuzione.setItem(index, 2, QTableWidgetItem(str(esame.codice_esame)))
            self.lista_esecuzione.setItem(index, 3, QTableWidgetItem(esame.descrizione_esame))
            if esame.data_ora_schedulato is not None:
                self.lista_esecuzione.setItem(index, 4, QTableWidgetItem(esame.data_ora_schedulato.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            if esame.attrezzatura is not None:
                self.lista_esecuzione.setItem(index, 5, QTableWidgetItem(esame.attrezzatura.dicom_ae_title))
            index = index + 1

    def completa_esame(self):
        #  Funzione che richiama la dialog di richiesta popolandola con i dati di una già esistente
        self.model.esame_corrente = self.model.qs_esami[self.lista_esecuzione.currentRow()]
        richiesta_model = RichiestaModel(self.model.esame_corrente)  # passo l'esame corrente alla richiesta
        richiesta_controller = RichiestaController(richiesta_model)
        richiesta_view = RichiestaView(richiesta_model, richiesta_controller)
        richiesta_view.tabWidget.setCurrentIndex(3)
        if richiesta_view.exec_():
            self.aggiorna_worklist()
