from PyQt5.QtGui import QCloseEvent

from .consegna_controller import ConsegnaController
from .consegna_model import ConsegnaModel
from .consegna_ui import Ui_Consegna
from PyQt5.QtWidgets import QWidget, QMessageBox
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class ConsegnaView(Ui_Consegna, QWidget):
    def __init__(self, model: ConsegnaModel, controller: ConsegnaController, parent=None):
        super(ConsegnaView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente consegna')
        Ambiente.stati[App.CONSEGNA.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        Ambiente.stati[App.CONSEGNA.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.CONSEGNA.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()
