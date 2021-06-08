from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog

from .richiesta_controller import RichiestaController
from .richiesta_model import RichiestaModel
from .richiesta_ui import Ui_Dialog_Richiesta
from ..utils import Stati


class RichiestaView(Ui_Dialog_Richiesta, QDialog):
    def __init__(self, model: RichiestaModel, controller: RichiestaController, parent=None):
        super(RichiestaView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)
        self.stato = Stati.CHIUSO

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura dialog richiesta')
        self.stato = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.stato = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        self.close()

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
