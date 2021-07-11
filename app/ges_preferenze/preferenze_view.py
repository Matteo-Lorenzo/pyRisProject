import pickle

import qdarkstyle
from PyQt5.QtGui import QCloseEvent

from .preferenze_controller import PreferenzeController
from .preferenze_model import PreferenzeModel
from .preferenze_ui import Ui_Preferenze
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class PreferenzeView(Ui_Preferenze, QWidget):
    def __init__(self, model: PreferenzeModel, controller: PreferenzeController, parent=None):
        super(PreferenzeView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.inizializza_lista_utenti()
        self.inizializza_lista_sale()
        if Ambiente.piattaforma == 'Darwin':
            self.rb_mac.setEnabled(True)
            self.rb_wvista.setEnabled(False)
        elif Ambiente.piattaforma == 'Windows':
            self.rb_mac.setEnabled(False)
            self.rb_wvista.setEnabled(True)
        else:
            self.rb_mac.setEnabled(False)
            self.rb_wvista.setEnabled(False)
        self.popola()
        self.collega()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente preferenze')
        Ambiente.stati[App.PREFERENZE.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        with open('..config.pickle', 'wb') as f:
            pickle.dump(Ambiente.visualizzazione, f, pickle.HIGHEST_PROTOCOL)
        Ambiente.app.setStyle(Ambiente.visualizzazione['stile'])
        if Ambiente.visualizzazione['tema'] == 'scuro':
            Ambiente.app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            Ambiente.app.setStyleSheet('')
        self.close()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        if Ambiente.stati[App.PREFERENZE.value] == Stati.MODIFICATO:
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def popola(self):
        # tab Radiologia
        self.nome.setText(Ambiente.radiologia_corrente.nome)
        self.ragione_sociale.setText(Ambiente.radiologia_corrente.ragione_sociale)
        self.indirizzo.setText(Ambiente.radiologia_corrente.indirizzo)
        self.cap.setText(Ambiente.radiologia_corrente.cap)
        self.citta.setText(Ambiente.radiologia_corrente.citta)
        self.provincia.setText(Ambiente.radiologia_corrente.provincia)
        self.email.setText(Ambiente.radiologia_corrente.email)
        self.sito_web.setText(Ambiente.radiologia_corrente.sito_web)
        self.telefono.setText(Ambiente.radiologia_corrente.telefono)
        self.p_iva.setText(Ambiente.radiologia_corrente.p_iva)
        self.responsabile.setText(Ambiente.radiologia_corrente.responsabile)
        self.direttore_sanitario.setText(Ambiente.radiologia_corrente.direttore_sanitario)
        self.descrizione.setPlainText(Ambiente.radiologia_corrente.descrizione)
        # tab Utenti
        self.carica_utenti()
        # tab Sale Diagnostiche
        self.carica_sale()
        # tab Configurazioni Workstation
        self.rb_windows.setChecked(Ambiente.visualizzazione['stile'] == 'Windows')
        self.rb_mac.setChecked(Ambiente.visualizzazione['stile'] == 'macintosh')
        self.rb_fusion.setChecked(Ambiente.visualizzazione['stile'] == 'Fusion')
        self.rb_wvista.setChecked(Ambiente.visualizzazione['stile'] == 'windowsvista')
        self.rb_chiaro.setChecked(Ambiente.visualizzazione['tema'] == 'chiaro')
        self.rb_scuro.setChecked(Ambiente.visualizzazione['tema'] == 'scuro')

    def collega(self):
        self.rb_windows.clicked.connect(self.ges_stile)
        self.rb_mac.clicked.connect(self.ges_stile)
        self.rb_fusion.clicked.connect(self.ges_stile)
        self.rb_wvista.clicked.connect(self.ges_stile)
        self.rb_chiaro.clicked.connect(self.ges_tema)
        self.rb_scuro.clicked.connect(self.ges_tema)

    def inizializza_lista_utenti(self):
        self.lista_utenti.setColumnCount(4)
        self.lista_utenti.setHorizontalHeaderLabels(['Username', 'Cognome', 'Nome', 'Tipo'])
        self.lista_utenti.setColumnWidth(0, 268)
        self.lista_utenti.setColumnWidth(1, 268)
        self.lista_utenti.setColumnWidth(2, 268)
        self.lista_utenti.setColumnWidth(3, 268)

    def inizializza_lista_sale(self):
        self.lista_sale.setColumnCount(2)
        self.lista_sale.setHorizontalHeaderLabels(['Nome', 'Descrizione'])
        self.lista_sale.setColumnWidth(0, 200)
        self.lista_sale.setColumnWidth(1, 875)

    def carica_utenti(self):
        qs_utenti = Ambiente.radiologia_corrente.utenti_interni.all()
        self.lista_utenti.setRowCount(len(qs_utenti))
        index = 0
        for utente in qs_utenti:
            self.lista_utenti.setItem(index, 0, QTableWidgetItem(utente.username))
            self.lista_utenti.setItem(index, 1, QTableWidgetItem(utente.last_name))
            self.lista_utenti.setItem(index, 2, QTableWidgetItem(utente.first_name))
            self.lista_utenti.setItem(index, 3, QTableWidgetItem(utente.tipo))
            index = index + 1

    def carica_sale(self):
        qs_sale = Ambiente.radiologia_corrente.sale_diagnostiche.all()
        self.lista_sale.setRowCount(len(qs_sale))
        index = 0
        for sala_diagnostica in qs_sale:
            self.lista_sale.setItem(index, 0, QTableWidgetItem(sala_diagnostica.nome))
            self.lista_sale.setItem(index, 1, QTableWidgetItem(sala_diagnostica.descrizione))
            index = index + 1

    def ges_stile(self):
        if self.rb_windows.isChecked():
            Ambiente.visualizzazione['stile'] = 'Windows'
        elif self.rb_mac.isChecked():
            Ambiente.visualizzazione['stile'] = 'macintosh'
        elif self.rb_fusion.isChecked():
            Ambiente.visualizzazione['stile'] = 'Fusion'
        else:
            Ambiente.visualizzazione['stile'] = 'windowsvista'

    def ges_tema(self):
        if self.rb_chiaro.isChecked():
            Ambiente.visualizzazione['tema'] = 'chiaro'
        else:
            Ambiente.visualizzazione['tema'] = 'scuro'
