from PyQt5.QtGui import QCloseEvent

from .refertazione_controller import RefertazioneController
from .refertazione_model import RefertazioneModel
from .refertazione_ui import Ui_Refertazione
from PyQt5.QtWidgets import QWidget, QMessageBox
from ..utils import Stati, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class RefertazioneView(Ui_Refertazione, QWidget):
    def __init__(self, ambiente: MainWindowModel, model: RefertazioneModel, controller: RefertazioneController, parent=None):
        super(RefertazioneView, self).__init__(parent)
        self.ambiente = ambiente
        self.model = model
        self.controller = controller
        self.setupUi(self)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente refertazione')
        self.ambiente.stati[App.REFERTAZIONE.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.ambiente.stati[App.REFERTAZIONE.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if self.ambiente.stati[App.REFERTAZIONE.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()
