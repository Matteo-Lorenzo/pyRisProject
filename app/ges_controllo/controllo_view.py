from PyQt5.QtGui import QCloseEvent

from .controllo_controller import ControlloController
from .controllo_model import ControlloModel
from .controllo_ui import Ui_Controllo
from PyQt5.QtWidgets import QWidget, QMessageBox
from ..utils import Stati, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class ControlloView(Ui_Controllo, QWidget):
    def __init__(self, ambiente: MainWindowModel, model: ControlloModel, controller: ControlloController, parent=None):
        super(ControlloView, self).__init__(parent)
        self.ambiente = ambiente
        self.model = model
        self.controller = controller
        self.setupUi(self)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente controllo')
        self.ambiente.stati[App.CONTROLLO.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.ambiente.stati[App.CONTROLLO.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if self.ambiente.stati[App.CONTROLLO.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()
