from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from store.models import Paziente
from .anamnesi_remota_ui import Ui_Dialog_anamnesi
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class AnamnesiRemotaView(Ui_Dialog_anamnesi, QDialog):
    def __init__(self, testo_anamnesi, parent=None):
        super(AnamnesiRemotaView, self).__init__(parent)
        self.setupUi(self)
        self.anamnesi_remota.setPlainText(testo_anamnesi)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente anamnesi remota')
        event.accept()
