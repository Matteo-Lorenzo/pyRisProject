from PyQt5.QtCore import QDate, QVariant
from PyQt5.QtGui import QCloseEvent

from store.models import Paziente
from .anagrafica_controller import AnagraficaController
from .anagrafica_model import AnagraficaModel
from .anagrafica_ui import Ui_Anagrafica
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from ..utils import Stati, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class AnagraficaView(Ui_Anagrafica, QWidget):
    def __init__(self, ambiente: MainWindowModel, model: AnagraficaModel, controller: AnagraficaController,
                 parent=None):
        super(AnagraficaView, self).__init__(parent)
        self.ambiente = ambiente
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.frame_paziente.hide()  # Nascondo l'anagrafica dettagliata
        self.inizializza_lista_pazienti()
        self.inizializza_scheda_paziente()

        self.collega()  # Effettuo il binding degli elementi dell'interfaccia con i relativi campi del modello

    def inizializza_scheda_paziente(self):
        delegate = QStyledItemDelegate()
        self.sesso.setItemDelegate(delegate)  # Inserito per risolvere problemi di visualizzazione del ComboBox con lo stylesheet
        for choice in self.model.paziente.SESSO_CHOICES:  # Costruzione del ComboBox per il sesso sulla base delle alternative descritte nel modello
            self.sesso.addItem(choice.__getitem__(1), QVariant(choice.__getitem__(0)))

    def inizializza_lista_pazienti(self):
        self.lista_pazienti.setGeometry(self.frame_paziente.x(), self.frame_paziente.y(), self.frame_paziente.width(),
                                        self.frame_paziente.height())
        self.lista_pazienti.setColumnCount(5)
        self.lista_pazienti.setHorizontalHeaderLabels(['Codice paziente', 'Cognome', 'Nome', 'Sesso', 'Data nascita'])
        self.lista_pazienti.setColumnWidth(0, 234)
        self.lista_pazienti.setColumnWidth(1, 234)
        self.lista_pazienti.setColumnWidth(2, 234)
        self.lista_pazienti.setColumnWidth(3, 234)
        self.lista_pazienti.setColumnWidth(4, 234)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente gestione paziente')
        self.ambiente.stati[App.GESTIONE_PAZIENTI.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.ambiente.stati[App.GESTIONE_PAZIENTI.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        if self.model.is_modified():  # Ottimizzazione: salvo solo se modificato
            self.model.paziente_corrente.save()  # Salvo nel DataBase
            self.cerca()  # Ripeto la query al DB e aggiorno la lista mostrata

        self.frame_paziente.hide()
        self.lista_pazienti.show()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        # if self.ambiente.stati[App.GESTIONE_PAZIENTI.value] == Stati.MODIFICATO: | ORA QUESTO NON SERVE PIU'
        if self.model.is_modified():  # Se qualcosa nei dati è stato modificato faccio il controllo
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.frame_paziente.hide()
                self.lista_pazienti.show()
        else:
            self.frame_paziente.hide()
            self.lista_pazienti.show()

    def esci(self):
        # esco senza salvare le modifiche fatte
        if self.model.is_modified():  # Se qualcosa nei dati è stato modificato faccio il controllo
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def cerca(self):  # Ricerco i pazienti e costruisco la lista da mostrare
        self.controller.cerca_paziente(self.cerca_codice_paziente.text(), self.cerca_cognome.text(),
                                       self.cerca_nome.text())
        self.lista_pazienti.setRowCount(len(self.model.qs))
        index = 0
        for paziente in self.model.qs:
            self.lista_pazienti.setItem(index, 0, QTableWidgetItem(paziente.codice_paziente))
            self.lista_pazienti.setItem(index, 1, QTableWidgetItem(paziente.cognome))
            self.lista_pazienti.setItem(index, 2, QTableWidgetItem(paziente.nome))
            self.lista_pazienti.setItem(index, 3, QTableWidgetItem(paziente.sesso))
            self.lista_pazienti.setItem(index, 4, QTableWidgetItem(str(paziente.data_nascita)))
            index = index + 1

    def mostra_paziente(self):
        # Seleziono il paziente corrente in base al doppio click fatto sulla lista
        self.model.paziente_corrente = self.model.qs[self.lista_pazienti.currentIndex().row()]
        self.model.setta_originale()  # Copio sotto forma di dizionario il paziente corrente: "mo me lo segno!!"
        self.popola()  # Popolo i campi dell' anagrafica dettagliata come da modello

        self.lista_pazienti.hide()
        self.frame_paziente.show()

    def collega(self):  # Binding degli elementi dell'interfaccia con i relativi campi del modello
        self.codice_paziente.textChanged.connect(self.set_codice_paziente)
        self.nome.textChanged.connect(self.set_nome)
        self.cognome.textChanged.connect(self.set_cognome)
        self.sesso.currentIndexChanged.connect(self.set_sesso)
        self.data_nascita.dateChanged.connect(self.set_data_nascita)

    def set_codice_paziente(self):
        self.model.paziente_corrente.codice_paziente = self.codice_paziente.text()

    def set_nome(self):
        self.model.paziente_corrente.nome = self.nome.text()

    def set_cognome(self):
        self.model.paziente_corrente.cognome = self.cognome.text()

    def set_sesso(self):
        self.model.paziente_corrente.sesso = self.sesso.currentData()

    def set_data_nascita(self):
        self.model.paziente_corrente.data_nascita = self.data_nascita.date().toPyDate()

    def popola(self):  # Popola i campi dell' anagrafica dettagliata come da modello
        self.codice_paziente.setText(self.model.paziente_corrente.codice_paziente)
        self.cognome.setText(self.model.paziente_corrente.cognome)
        self.nome.setText(self.model.paziente_corrente.nome)
        data = QDate()
        data.setDate(self.model.paziente_corrente.data_nascita.year,
                     self.model.paziente_corrente.data_nascita.month,
                     self.model.paziente_corrente.data_nascita.day)
        self.data_nascita.setDate(data)
        self.sesso.setCurrentIndex(self.sesso.findData(QVariant(self.model.paziente_corrente.sesso)))
