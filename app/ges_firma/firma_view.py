from PyQt5.QtGui import QCloseEvent

from .firma_controller import FirmaController
from .firma_model import FirmaModel
from .firma_ui import Ui_Firma
from PyQt5.QtWidgets import QWidget, QMessageBox
from ..utils import Stati, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class FirmaView(Ui_Firma, QWidget):
    def __init__(self, ambiente: MainWindowModel, model: FirmaModel, controller: FirmaController, parent=None):
        super(FirmaView, self).__init__(parent)
        self.ambiente = ambiente
        self.model = model
        self.controller = controller
        self.setupUi(self)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente firma referto')
        self.ambiente.stati[App.FIRMA.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.ambiente.stati[App.FIRMA.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if self.ambiente.stati[App.FIRMA.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()
