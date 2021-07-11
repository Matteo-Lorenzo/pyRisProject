from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog

from .login_controller import LoginController
from .login_model import LoginModel
from .login_ui import Ui_Dialog_Login
from ..utils import Stati, Ambiente


class LoginView(Ui_Dialog_Login, QDialog):
    def __init__(self, model: LoginModel, controller: LoginController, parent=None):
        super(LoginView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura dialog login')
        event.accept()
        # prevedere la non accettazione della chiusura per mancato accesso

    def accetta(self):
        # chiamo django per cercare l'utente
        if self.controller.login(self.utente.text(), self.password.text()):
            Ambiente.set_ambiente()
            Ambiente.main_window.menubar_pyris.show()
            Ambiente.main_window.setWindowTitle('PyRIS - 1.0.0 - ' + Ambiente.utente_corrente.last_name + ' ' + Ambiente.utente_corrente.first_name)
            self.set_menu()
            self.close()  # Chiusa la Dialog di login con "accetta" devo mostrare la finestra principale
        else:
            QMessageBox.information(self, 'Attenzione', 'Nome utente o password errati', QMessageBox.Ok, QMessageBox.Ok)
        self.utente.setText('')
        self.password.setText('')

    def annulla(self):
        # Termino il programma
        Ambiente.app.quit()

    def set_menu(self):
        Ambiente.main_window.actionRefertazione.setText('Trascrizione')
        if Ambiente.utente_corrente.tipo == 'MED':
            # Menu File
            Ambiente.main_window.actionGestione_pazienti.setEnabled(True)
            Ambiente.main_window.actionPrenotazioni.setEnabled(False)
            Ambiente.main_window.actionConsegna.setEnabled(False)
            Ambiente.main_window.actionPreferenze.setEnabled(False)
            # Menu Worklist
            Ambiente.main_window.actionEsecuzione_esame.setEnabled(True)
            Ambiente.main_window.actionRefertazione.setEnabled(True)
            Ambiente.main_window.actionRefertazione.setText('Refertazione')
            Ambiente.main_window.actionFirma.setEnabled(True)
            Ambiente.main_window.actionControllo.setEnabled(False)
        elif Ambiente.utente_corrente.tipo == 'TEC':
            # Menu File
            Ambiente.main_window.actionGestione_pazienti.setEnabled(True)
            Ambiente.main_window.actionPrenotazioni.setEnabled(False)
            Ambiente.main_window.actionConsegna.setEnabled(False)
            Ambiente.main_window.actionPreferenze.setEnabled(False)
            # Menu Worklist
            Ambiente.main_window.actionEsecuzione_esame.setEnabled(True)
            Ambiente.main_window.actionRefertazione.setEnabled(False)
            Ambiente.main_window.actionFirma.setEnabled(False)
            Ambiente.main_window.actionControllo.setEnabled(False)
        elif Ambiente.utente_corrente.tipo == 'AMM':
            # Menu File
            Ambiente.main_window.actionGestione_pazienti.setEnabled(True)
            Ambiente.main_window.actionPrenotazioni.setEnabled(True)
            Ambiente.main_window.actionConsegna.setEnabled(True)
            Ambiente.main_window.actionPreferenze.setEnabled(False)
            # Menu Worklist
            Ambiente.main_window.actionEsecuzione_esame.setEnabled(False)
            Ambiente.main_window.actionRefertazione.setEnabled(True)
            Ambiente.main_window.actionFirma.setEnabled(False)
            Ambiente.main_window.actionControllo.setEnabled(True)
        elif Ambiente.utente_corrente.tipo == 'AMS':
            # Menu File
            Ambiente.main_window.actionGestione_pazienti.setEnabled(False)
            Ambiente.main_window.actionPrenotazioni.setEnabled(False)
            Ambiente.main_window.actionConsegna.setEnabled(False)
            Ambiente.main_window.actionPreferenze.setEnabled(True)
            # Menu Worklist
            Ambiente.main_window.actionEsecuzione_esame.setEnabled(False)
            Ambiente.main_window.actionRefertazione.setEnabled(False)
            Ambiente.main_window.actionFirma.setEnabled(False)
            Ambiente.main_window.actionControllo.setEnabled(True)
        elif Ambiente.utente_corrente.tipo == 'INF':
            # Menu File
            Ambiente.main_window.actionGestione_pazienti.setEnabled(True)
            Ambiente.main_window.actionPrenotazioni.setEnabled(True)
            Ambiente.main_window.actionConsegna.setEnabled(True)
            Ambiente.main_window.actionPreferenze.setEnabled(False)
            # Menu Worklist
            Ambiente.main_window.actionEsecuzione_esame.setEnabled(True)
            Ambiente.main_window.actionRefertazione.setEnabled(False)
            Ambiente.main_window.actionFirma.setEnabled(False)
            Ambiente.main_window.actionControllo.setEnabled(False)
