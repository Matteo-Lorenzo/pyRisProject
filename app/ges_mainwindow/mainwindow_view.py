from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QMdiSubWindow, QMessageBox

from app.ges_pazienti.anagrafica_view import AnagraficaView
from .mainwindow_ui import Ui_MainWindow
from .mainwindow_model import MainWindowModel
from .mainwindow_controller import MainWindowController
from ..ges_consegna.consegna_controller import ConsegnaController
from ..ges_consegna.consegna_model import ConsegnaModel
from ..ges_consegna.consegna_view import ConsegnaView
from ..ges_controllo.controllo_controller import ControlloController
from ..ges_controllo.controllo_model import ControlloModel
from ..ges_controllo.controllo_view import ControlloView
from ..ges_esame.esame_controller import EsameController
from ..ges_esame.esame_model import EsameModel
from ..ges_esame.esame_view import EsameView
from ..ges_firma.firma_controller import FirmaController
from ..ges_firma.firma_model import FirmaModel
from ..ges_firma.firma_view import FirmaView
from ..ges_pazienti.anagrafica_controller import AnagraficaController
from ..ges_pazienti.anagrafica_model import AnagraficaModel
from ..ges_preferenze.preferenze_controller import PreferenzeController
from ..ges_preferenze.preferenze_model import PreferenzeModel
from ..ges_preferenze.preferenze_view import PreferenzeView
from ..ges_prenotazioni.prenotazioni_controller import PrenotazioniController
from ..ges_prenotazioni.prenotazioni_model import PrenotazioniModel
from ..ges_prenotazioni.prenotazioni_view import PrenotazioniView
from ..ges_refertazione.refertazione_controller import RefertazioneController
from ..ges_refertazione.refertazione_model import RefertazioneModel
from ..ges_refertazione.refertazione_view import RefertazioneView
from ..utils import Stati, Applicazioni as App


class MainWindowView(Ui_MainWindow, QMainWindow):

    def __init__(self, model: MainWindowModel, controller: MainWindowController, parent=None):
        super(MainWindowView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)
        # self.menubar_pyris.triggered[QAction].connect(self.menu_manager)
        self.actionGestione_pazienti.triggered.connect(self.actionGestione_pazienti_listener)
        self.actionPrenotazioni.triggered.connect(self.actionPrenotazioni_listener)
        self.actionConsegna.triggered.connect(self.actionConsegna_listener)
        self.actionPreferenze.triggered.connect(self.actionPreferenze_listener)
        self.actionEsecuzione_esame.triggered.connect(self.actionEsecuzione_esame_listener)
        self.actionRefertazione.triggered.connect(self.actionRefertazione_listener)
        self.actionFirma.triggered.connect(self.actionFirma_listener)
        self.actionControllo.triggered.connect(self.actionControllo_listener)
        self.finestra_corrente = None
        # aggiungere tutti gli altri necessari (non servono più)

    '''
        Gestione menu File
    '''

    def actionGestione_pazienti_listener(self):
        self.apri_nuovo(App.GESTIONE_PAZIENTI.value, AnagraficaView, AnagraficaController, AnagraficaModel)

    def actionPrenotazioni_listener(self):
        self.apri_nuovo(App.PRENOTAZIONI.value, PrenotazioniView, PrenotazioniController, PrenotazioniModel)

    def actionConsegna_listener(self):
        self.apri_nuovo(App.CONSEGNA.value, ConsegnaView, ConsegnaController, ConsegnaModel)

    def actionPreferenze_listener(self):
        self.apri_nuovo(App.PREFERENZE.value, PreferenzeView, PreferenzeController, PreferenzeModel)

    '''
        Gestione menu Worklist
    '''

    def actionEsecuzione_esame_listener(self):
        self.apri_nuovo(App.ESECUZIONE_ESAME.value, EsameView, EsameController, EsameModel)

    def actionRefertazione_listener(self):
        self.apri_nuovo(App.REFERTAZIONE.value, RefertazioneView, RefertazioneController, RefertazioneModel)

    def actionFirma_listener(self):
        self.apri_nuovo(App.FIRMA.value, FirmaView, FirmaController, FirmaModel)

    def actionControllo_listener(self):
        self.apri_nuovo(App.CONTROLLO.value, ControlloView, ControlloController, ControlloModel)

    '''
        Organizzazione disposizione finestre nell'interfaccia
    '''

    def before_apertura_nuova_vista(self):  # FUNZIONE NON PIU' UTILIZZATA ATTUALMENTE
        # vede qual è il componente attualmente mostrato e, se necessario, lo chiude
        # questo metodo deve ritornare un booleano, a seconda che la .close() di una certa finestra sia andata a buon fine o meno
        if (self.finestra_corrente is not None) and self.is_ok_to_switch():
            # controlli intermedi prima della chiusura se necessari (forse li può fare già l'oggetto stesso alla chiamata del .close())
            self.finestra_corrente.close()
        # return un or di tutti i flag booleani delle finestre a disposizione (se falso sono effettivamente tutte chiuse)

    def apri_nuovo(self, applicazione, vista, controllore, modello):
        # if self.model.stati[applicazione] == Stati.CHIUSO: # se il componente richiesto non è già mostrato | NON SERVE PIU'
        if self.is_ok_to_switch():
            # self.before_apertura_nuova_vista()  # vede qual è il componente attualmente mostrato e, se necessario, lo chiude
            self.model.stati[applicazione] = Stati.APERTO # imposta ad APERTO lo stato del componente richiesto
            il_modello = modello()
            il_controllore = controllore(il_modello)
            self.finestra_corrente = vista(self.model, il_modello, il_controllore) # istanzia il componente richiesto
            # popolare la finestra come da modello

            self.finestra_corrente.setParent(self.centralwidget)
            self.finestra_corrente.show()
        else:
            QMessageBox.warning(self, 'Attenzione', "Terminare l'attività corrente")

    def is_ok_to_switch(self):
        # ritorna True se i componenti sono tutti chiusi
        count = 0
        for stato in self.model.stati:
            if self.model.stati[stato] is not Stati.CHIUSO:
                count = count+1
        print(count)
        return count == 0

    def closeEvent(self, event: QCloseEvent):
        if self.is_ok_to_switch():
            event.accept()
        else:
            QMessageBox.warning(self, 'Attenzione', "Terminare l'attività corrente")
            event.ignore()
        # prevedere la non accettazione della chiusura per modifiche non salvate

# print(MainWindow.__mro__)
# print(QMainWindow.__mro__)
