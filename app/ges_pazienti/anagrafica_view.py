from PyQt5.QtCore import QDate, QVariant
from PyQt5.QtGui import QCloseEvent

from store.models import Paziente
from .anagrafica_controller import AnagraficaController
from .anagrafica_model import AnagraficaModel
from .anagrafica_ui import Ui_Anagrafica
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate

from ..ges_richieste.richiesta_controller import RichiestaController
from ..ges_richieste.richiesta_model import RichiestaModel
from ..ges_richieste.richiesta_view import RichiestaView
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
        self.inizializza_lista_richieste()
        self.inizializza_lista_refertazione()
        self.inizializza_lista_archivio()
        self.tabWidget.setCurrentIndex(0)

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

    def inizializza_lista_richieste(self):
        self.lista_richieste.setColumnCount(4)
        self.lista_richieste.setHorizontalHeaderLabels(['Numero Esame', 'Schedulato il', 'Prestazioni', 'Stato di Avanzamento'])
        self.lista_richieste.setColumnWidth(0, 100)
        self.lista_richieste.setColumnWidth(1, 120)
        self.lista_richieste.setColumnWidth(2, 714)
        self.lista_richieste.setColumnWidth(3, 150)

    def inizializza_lista_refertazione(self):
        self.lista_refertazione.setColumnCount(3)
        self.lista_refertazione.setHorizontalHeaderLabels(['Numero Esame', 'Eseguito il', 'Prestazioni'])
        self.lista_refertazione.setColumnWidth(0, 100)
        self.lista_refertazione.setColumnWidth(1, 120)
        self.lista_refertazione.setColumnWidth(2, 864)

    def inizializza_lista_archivio(self):
        self.lista_archivio.setColumnCount(4)
        self.lista_archivio.setHorizontalHeaderLabels(['Numero Esame', 'Refertato il', 'Prestazioni', 'Refertato da'])
        self.lista_archivio.setColumnWidth(0, 100)
        self.lista_archivio.setColumnWidth(1, 120)
        self.lista_archivio.setColumnWidth(2, 714)
        self.lista_archivio.setColumnWidth(3, 150)

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
        self.lista_pazienti.setRowCount(len(self.model.qs_pazienti))
        index = 0
        for paziente in self.model.qs_pazienti:
            self.lista_pazienti.setItem(index, 0, QTableWidgetItem(paziente.codice_paziente))
            self.lista_pazienti.setItem(index, 1, QTableWidgetItem(paziente.cognome))
            self.lista_pazienti.setItem(index, 2, QTableWidgetItem(paziente.nome))
            self.lista_pazienti.setItem(index, 3, QTableWidgetItem(paziente.sesso))
            if paziente.data_nascita is not None:
                self.lista_pazienti.setItem(index, 4, QTableWidgetItem(paziente.data_nascita.strftime("%d-%m-%Y")))
            index = index + 1

    def mostra_paziente(self):
        # Seleziono il paziente corrente in base al doppio click fatto sulla lista
        self.model.paziente_corrente = self.model.qs_pazienti[self.lista_pazienti.currentIndex().row()]
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
        self.pk_paziente.setText(str(self.model.paziente_corrente.pk))
        self.codice_paziente.setText(self.model.paziente_corrente.codice_paziente)
        self.cognome.setText(self.model.paziente_corrente.cognome)
        self.nome.setText(self.model.paziente_corrente.nome)
        data = QDate()
        data.setDate(self.model.paziente_corrente.data_nascita.year,
                     self.model.paziente_corrente.data_nascita.month,
                     self.model.paziente_corrente.data_nascita.day)
        self.data_nascita.setDate(data)
        self.sesso.setCurrentIndex(self.sesso.findData(QVariant(self.model.paziente_corrente.sesso)))

    def mostra_richiesta(self):
        # questa è la funzione che richiama la dialog di richiesta, volendo la si può fare parametrica con dei parametri
        # di default, così viene chiamata senza parametri dal bottone Nuova Richiesta e con parametri della richiesta da
        # mostrare e editare facendo doppio click da una richiesta di lista richieste
        self.model.esame_corrente = self.model.qs_richieste[self.lista_richieste.currentIndex().row()]
        richiesta_model = RichiestaModel()
        richiesta_controller = RichiestaController(richiesta_model)
        richiesta_view = RichiestaView(richiesta_model, richiesta_controller)
        richiesta_view.descrizione_esame.setText(self.model.esame_corrente.descrizione_esame)
        richiesta_view.exec_()

    def nuova_richiesta(self):
        richiesta_model = RichiestaModel()
        richiesta_controller = RichiestaController(richiesta_model)
        richiesta_view = RichiestaView(richiesta_model, richiesta_controller)
        richiesta_view.exec_()

    def cerca_richieste(self):  # Ricerco le richieste e costruisco la lista da mostrare
        self.controller.cerca_richieste()
        self.lista_richieste.setRowCount(len(self.model.qs_richieste))
        index = 0
        for esame in self.model.qs_richieste:
            self.lista_richieste.setItem(index, 0, QTableWidgetItem(esame.codice_esame))
            if esame.data_ora_schedulato is not None:
                self.lista_richieste.setItem(index, 1, QTableWidgetItem(esame.data_ora_schedulato.strftime("%d-%m-%Y ore %H:%M")))
            self.lista_richieste.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            self.lista_richieste.setItem(index, 3, QTableWidgetItem(esame.stato_avanzamento))
            index = index + 1

    def cerca_refertazione(self):  # Ricerco gli studi da refertare e costruisco la lista da mostrare
        self.controller.cerca_refertazione()
        self.lista_refertazione.setRowCount(len(self.model.qs_refertazione))
        index = 0
        for esame in self.model.qs_refertazione:
            self.lista_refertazione.setItem(index, 0, QTableWidgetItem(esame.codice_esame))
            if esame.data_ora_completato is not None:
                self.lista_refertazione.setItem(index, 1, QTableWidgetItem(esame.data_ora_completato.strftime("%d-%m-%Y ore %H:%M")))
            self.lista_refertazione.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            index = index + 1

    def cerca_archivio(self):  # Ricerco gli studi archiviati e costruisco la lista da mostrare
        self.controller.cerca_archivio()
        self.lista_archivio.setRowCount(len(self.model.qs_archivio))
        index = 0
        for esame in self.model.qs_archivio:
            self.lista_archivio.setItem(index, 0, QTableWidgetItem(esame.codice_esame))
            if esame.data_ora_refertazione is not None:
                self.lista_archivio.setItem(index, 1, QTableWidgetItem(esame.data_ora_refertazione.strftime("%d-%m-%Y ore %H:%M")))
            self.lista_archivio.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            self.lista_archivio.setItem(index, 3, QTableWidgetItem(esame.refertato_da.last_name))
            index = index + 1

    def gestione(self, x):
        if x == 1:
            self.cerca_richieste()
        elif x == 2:
            self.cerca_refertazione()
        elif x == 3:
            self.cerca_archivio()
