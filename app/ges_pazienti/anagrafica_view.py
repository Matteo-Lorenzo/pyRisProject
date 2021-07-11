from PyQt5.QtCore import QDate, QVariant
from PyQt5.QtGui import QCloseEvent
from sequences import get_next_value
from datetime import datetime
from codicefiscale import codicefiscale

from store.models import Radiologia
from .anagrafica_controller import AnagraficaController
from .anagrafica_model import AnagraficaModel
from .anagrafica_ui import Ui_Anagrafica
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QStyledItemDelegate
from django.utils import timezone

from .anamnesi_remota_view import AnamnesiRemotaView
from ..ges_archivio.archivio_controller import ArchivioController
from ..ges_archivio.archivio_model import ArchivioModel
from ..ges_archivio.archivio_view import ArchivioView
from ..ges_referti.referto_controller import RefertoController
from ..ges_referti.referto_model import RefertoModel
from ..ges_referti.referto_view import RefertoView
from ..ges_richieste.richiesta_controller import RichiestaController
from ..ges_richieste.richiesta_model import RichiestaModel
from ..ges_richieste.richiesta_view import RichiestaView
from ..utils import Stati, Ambiente, Applicazioni as App

from ..ges_mainwindow.mainwindow_model import MainWindowModel


class AnagraficaView(Ui_Anagrafica, QWidget):
    def __init__(self, model: AnagraficaModel, controller: AnagraficaController,
                 parent=None):
        super(AnagraficaView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.tab1 = self.ric  # Tengo in memoria i riferimenti alle 3 tab
        self.tab2 = self.ref
        self.tab3 = self.arc
        self.frame_paziente.hide()  # Nascondo l'anagrafica dettagliata
        self.tabWidget.setCurrentIndex(0)
        self.inizializza_lista_pazienti()
        self.inizializza_scheda_paziente()
        self.inizializza_lista_richieste()
        self.inizializza_lista_refertazione()
        self.inizializza_lista_archivio()
        self.user_capabilities()

        self.collega()  # Effettuo il binding degli elementi dell'interfaccia con i relativi campi del modello

    def inizializza_scheda_paziente(self):
        delegate = QStyledItemDelegate()
        self.sesso.setItemDelegate(delegate)  # Inserito per risolvere problemi di visualizzazione del ComboBox con lo stylesheet
        for choice in self.model.paziente.SESSO_CHOICES:  # Costruzione del ComboBox per il sesso sulla base delle alternative descritte nel modello
            self.sesso.addItem(choice.__getitem__(1), QVariant(choice.__getitem__(0)))
        self.tabWidget.removeTab(3)
        self.tabWidget.removeTab(2)
        self.tabWidget.removeTab(1)

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
        self.lista_richieste.setColumnWidth(1, 170)
        self.lista_richieste.setColumnWidth(2, 664)
        self.lista_richieste.setColumnWidth(3, 150)

    def inizializza_lista_refertazione(self):
        self.lista_refertazione.setColumnCount(3)
        self.lista_refertazione.setHorizontalHeaderLabels(['Numero Esame', 'Eseguito il', 'Prestazioni'])
        self.lista_refertazione.setColumnWidth(0, 100)
        self.lista_refertazione.setColumnWidth(1, 170)
        self.lista_refertazione.setColumnWidth(2, 814)

    def inizializza_lista_archivio(self):
        self.lista_archivio.setColumnCount(4)
        self.lista_archivio.setHorizontalHeaderLabels(['Numero Esame', 'Refertato il', 'Prestazioni', 'Refertato da'])
        self.lista_archivio.setColumnWidth(0, 100)
        self.lista_archivio.setColumnWidth(1, 170)
        self.lista_archivio.setColumnWidth(2, 664)
        self.lista_archivio.setColumnWidth(3, 150)

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente gestione paziente')
        Ambiente.stati[App.GESTIONE_PAZIENTI.value] = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        Ambiente.stati[App.GESTIONE_PAZIENTI.value] = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        if self.model.is_modified():  # Ottimizzazione: salvo solo se modificato
            self.model.paziente_corrente.save()  # Salvo nel DataBase
            self.cerca()  # Ripeto la query al DB e aggiorno la lista mostrata

        self.frame_paziente.hide()
        self.lista_pazienti.show()
        self.frame_ricerca.show()

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        # if Ambiente.stati[App.GESTIONE_PAZIENTI.value] == Stati.MODIFICATO: | ORA QUESTO NON SERVE PIU'
        if self.model.is_modified():  # Se qualcosa nei dati è stato modificato faccio il controllo
            risposta = QMessageBox.question(self, 'Attenzione',
                                            'Dati modificati non salvati, sei sicuro di voler uscire?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if risposta == QMessageBox.Yes:
                self.cerca()  # Ripeto la query al DB per aggiornare la lista mostrata ed evitare incongruenze
                self.frame_paziente.hide()
                self.lista_pazienti.show()
                self.frame_ricerca.show()
        else:
            self.frame_paziente.hide()
            self.lista_pazienti.show()
            self.frame_ricerca.show()

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

    def reset(self):
        self.cerca_nome.setText('')
        self.cerca_cognome.setText('')
        self.cerca_codice_paziente.setText('')
        self.lista_pazienti.setRowCount(0)

    def cerca(self):  # Ricerco i pazienti e costruisco la lista da mostrare
        self.controller.cerca_paziente(self.cerca_codice_paziente.text(), self.cerca_cognome.text(),
                                       self.cerca_nome.text())
        self.lista_pazienti.setRowCount(len(self.model.qs_pazienti))
        index = 0
        for paziente in self.model.qs_pazienti:
            self.lista_pazienti.setItem(index, 0, QTableWidgetItem(str(paziente.codice_paziente)))
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
        self.tabWidget.setCurrentIndex(0)  # All'apertura di un nuovo paziente mostro sempre la sua angrafica
        self.frame_ricerca.hide()
        self.lista_pazienti.hide()
        self.frame_paziente.show()

    def collega(self):  # Binding degli elementi dell'interfaccia con i relativi campi del modello
        self.codice_paziente.textChanged.connect(self.set_codice_paziente)
        self.codice_esterno.textChanged.connect(self.set_codice_esterno)
        self.nome.textChanged.connect(self.set_nome)
        self.cognome.textChanged.connect(self.set_cognome)
        self.sesso.currentIndexChanged.connect(self.set_sesso)
        self.data_nascita.dateChanged.connect(self.set_data_nascita)
        self.codice_fiscale.textChanged.connect(self.set_codice_fiscale)
        self.cittadinanza.textChanged.connect(self.set_cittadinanza)
        self.tessera_sanitaria.textChanged.connect(self.set_tessera_sanitaria)
        self.comune_nascita.textChanged.connect(self.set_comune_nascita)
        self.provincia_nascita.textChanged.connect(self.set_provincia_nascita)
        self.indirizzo_residenza.textChanged.connect(self.set_indirizzo_residenza)
        self.comune_residenza.textChanged.connect(self.set_comune_residenza)
        self.provincia_residenza.textChanged.connect(self.set_provincia_residenza)
        self.email.textChanged.connect(self.set_email)
        self.telefono.textChanged.connect(self.set_telefono)
        self.cap_residenza.textChanged.connect(self.set_cap_residenza)
        self.indirizzo_domicilio.textChanged.connect(self.set_indirizzo_domicilio)
        self.comune_domicilio.textChanged.connect(self.set_comune_domicilio)
        self.provincia_domicilio.textChanged.connect(self.set_provincia_domicilio)
        self.cap_domicilio.textChanged.connect(self.set_cap_domicilio)

    def set_codice_paziente(self):
        self.model.paziente_corrente.codice_paziente = int(self.codice_paziente.text())
        # Da controllare l'eccezione generata se si inserisce input non intero

    def set_codice_esterno(self):
        self.model.paziente_corrente.codice_esterno = self.codice_esterno.text()

    def set_nome(self):
        self.model.paziente_corrente.nome = self.nome.text()

    def set_cognome(self):
        self.model.paziente_corrente.cognome = self.cognome.text()

    def set_sesso(self):
        self.model.paziente_corrente.sesso = self.sesso.currentData()

    def set_data_nascita(self):
        self.model.paziente_corrente.data_nascita = self.data_nascita.date().toPyDate()

    def set_codice_fiscale(self):
        self.model.paziente_corrente.codice_fiscale = self.codice_fiscale.text()

    def set_cittadinanza(self):
        self.model.paziente_corrente.cittadinanza = self.cittadinanza.text()

    def set_tessera_sanitaria(self):
        self.model.paziente_corrente.tessera_sanitaria = self.tessera_sanitaria.text()

    def set_comune_nascita(self):
        self.model.paziente_corrente.comune_nascita = self.comune_nascita.text()

    def set_provincia_nascita(self):
        self.model.paziente_corrente.provincia_comune_nascita = self.provincia_nascita.text()

    def set_indirizzo_residenza(self):
        self.model.paziente_corrente.indirizzo_residenza = self.indirizzo_residenza.text()

    def set_comune_residenza(self):
        self.model.paziente_corrente.comune_residenza = self.comune_residenza.text()

    def set_provincia_residenza(self):
        self.model.paziente_corrente.provincia_residenza = self.provincia_residenza.text()

    def set_email(self):
        self.model.paziente_corrente.email = self.email.text()

    def set_telefono(self):
        self.model.paziente_corrente.telefono = self.telefono.text()

    def set_cap_residenza(self):
        self.model.paziente_corrente.cap_residenza = self.cap_residenza.text()

    def set_indirizzo_domicilio(self):
        self.model.paziente_corrente.indirizzo_domicilio = self.indirizzo_domicilio.text()

    def set_comune_domicilio(self):
        self.model.paziente_corrente.comune_domicilio = self.comune_domicilio.text()

    def set_provincia_domicilio(self):
        self.model.paziente_corrente.provincia_domicilio = self.provincia_domicilio.text()

    def set_cap_domicilio(self):
        self.model.paziente_corrente.cap_domicilio = self.cap_domicilio.text()

    def popola(self):  # Popola i campi dell' anagrafica dettagliata come da modello
        self.codice_esterno.setText(self.model.paziente_corrente.codice_esterno)
        self.codice_paziente.setText(str(self.model.paziente_corrente.codice_paziente))
        self.cognome.setText(self.model.paziente_corrente.cognome)
        self.nome.setText(self.model.paziente_corrente.nome)
        if self.model.paziente_corrente.data_nascita is not None:
            data = QDate()
            data.setDate(self.model.paziente_corrente.data_nascita.year,
                         self.model.paziente_corrente.data_nascita.month,
                         self.model.paziente_corrente.data_nascita.day)
            self.data_nascita.setDate(data)
        self.sesso.setCurrentIndex(self.sesso.findData(QVariant(self.model.paziente_corrente.sesso)))
        self.codice_fiscale.setText(self.model.paziente_corrente.codice_fiscale)
        self.cittadinanza.setText(self.model.paziente_corrente.cittadinanza)
        self.tessera_sanitaria.setText(self.model.paziente_corrente.tessera_sanitaria)
        self.comune_nascita.setText(self.model.paziente_corrente.comune_nascita)
        self.provincia_nascita.setText(self.model.paziente_corrente.provincia_comune_nascita)
        self.indirizzo_residenza.setText(self.model.paziente_corrente.indirizzo_residenza)
        self.comune_residenza.setText(self.model.paziente_corrente.comune_residenza)
        self.provincia_residenza.setText(self.model.paziente_corrente.provincia_residenza)
        self.email.setText(self.model.paziente_corrente.email)
        self.telefono.setText(self.model.paziente_corrente.telefono)
        self.cap_residenza.setText(self.model.paziente_corrente.cap_residenza)
        self.indirizzo_domicilio.setText(self.model.paziente_corrente.indirizzo_domicilio)
        self.comune_domicilio.setText(self.model.paziente_corrente.comune_domicilio)
        self.provincia_domicilio.setText(self.model.paziente_corrente.provincia_domicilio)
        self.cap_domicilio.setText(self.model.paziente_corrente.cap_domicilio)

    def mostra_richiesta(self):
        #  Funzione che richiama la dialog di richiesta popolandola con i dati di una già esistente
        self.model.esame_corrente = self.model.qs_richieste[self.lista_richieste.currentIndex().row()]
        richiesta_model = RichiestaModel(self.model.esame_corrente)  # passo l'esame corrente alla richiesta
        richiesta_controller = RichiestaController(richiesta_model)
        richiesta_view = RichiestaView(richiesta_model, richiesta_controller)
        if richiesta_view.exec_():
            self.cerca_richieste()
        #richiesta_view.destroy()

    def nuova_richiesta(self):
        #  Funzione che richiama la dialog di richiesta creando un nuovo esame per cui fare la richiesta al momento attuale
        self.model.esame_corrente = self.model.esame()
        self.model.esame_corrente.codice_esame = get_next_value("esame")
        self.model.esame_corrente.radiologia = self.model.paziente_corrente.radiologia
        self.model.esame_corrente.paziente = self.model.paziente_corrente
        self.model.esame_corrente.data_ora_schedulato = timezone.localtime()  # Schedulo l'esame per adesso
        self.model.esame_corrente.schedulato_da = Ambiente.utente_corrente
        self.model.esame_corrente.stato_avanzamento = 2
        self.model.esame_corrente.save()  # Salvo il nuovo esame nel DataBase e lo passo come esame corrente alla richiesta per editarlo
        print('Esame creato ' + str(self.model.esame_corrente.id))
        richiesta_model = RichiestaModel(self.model.esame_corrente)
        richiesta_controller = RichiestaController(richiesta_model)
        richiesta_view = RichiestaView(richiesta_model, richiesta_controller)
        if richiesta_view.exec_():
            self.cerca_richieste()

    def cerca_richieste(self):  # Ricerco le richieste e costruisco la lista da mostrare
        self.controller.cerca_richieste()
        self.lista_richieste.setRowCount(len(self.model.qs_richieste))
        index = 0
        for esame in self.model.qs_richieste:
            self.lista_richieste.setItem(index, 0, QTableWidgetItem(str(esame.codice_esame)))
            if esame.data_ora_schedulato is not None:
                self.lista_richieste.setItem(index, 1, QTableWidgetItem(esame.data_ora_schedulato.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            self.lista_richieste.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            self.lista_richieste.setItem(index, 3, QTableWidgetItem(esame.get_stato_avanzamento_display()))
            index = index + 1

    def mostra_referto(self):
        #  Funzione che richiama la dialog di refertazione popolandola con i dati
        self.model.esame_corrente = self.model.qs_refertazione[self.lista_refertazione.currentIndex().row()]
        referto_model = RefertoModel(self.model.esame_corrente)  # passo l'esame corrente al referto
        referto_controller = RefertoController(referto_model)
        referto_view = RefertoView(referto_model, referto_controller)
        if referto_view.exec_():
            self.cerca_refertazione()

    def cerca_refertazione(self):  # Ricerco gli studi da refertare e costruisco la lista da mostrare
        self.controller.cerca_refertazione()
        self.lista_refertazione.setRowCount(len(self.model.qs_refertazione))
        index = 0
        for esame in self.model.qs_refertazione:
            self.lista_refertazione.setItem(index, 0, QTableWidgetItem(str(esame.codice_esame)))
            if esame.data_ora_completato is not None:
                self.lista_refertazione.setItem(index, 1, QTableWidgetItem(esame.data_ora_completato.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            self.lista_refertazione.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            index = index + 1

    def mostra_archivio(self):
        #  Funzione che richiama la dialog di archivio popolandola con i dati
        self.model.esame_corrente = self.model.qs_archivio[self.lista_archivio.currentIndex().row()]
        archivio_model = ArchivioModel(self.model.esame_corrente)  # passo l'esame corrente al referto
        archivio_controller = ArchivioController(archivio_model)
        archivio_view = ArchivioView(archivio_model, archivio_controller)
        if archivio_view.exec_():
            self.cerca_archivio()

    def cerca_archivio(self):  # Ricerco gli studi archiviati e costruisco la lista da mostrare
        self.controller.cerca_archivio()
        self.lista_archivio.setRowCount(len(self.model.qs_archivio))
        index = 0
        for esame in self.model.qs_archivio:
            self.lista_archivio.setItem(index, 0, QTableWidgetItem(str(esame.codice_esame)))
            if esame.data_ora_firma is not None:
                self.lista_archivio.setItem(index, 1, QTableWidgetItem(esame.data_ora_firma.astimezone(timezone.get_default_timezone()).strftime("%d-%m-%Y ore %H:%M")))
            self.lista_archivio.setItem(index, 2, QTableWidgetItem(esame.descrizione_esame))
            if esame.firmato_da is not None:
                self.lista_archivio.setItem(index, 3, QTableWidgetItem(esame.firmato_da.last_name))
            index = index + 1

    def gestione(self, x):
        if x == 0:
            self.tabWidget.removeTab(3)
            self.tabWidget.removeTab(2)
            self.tabWidget.removeTab(1)
        elif x == 1:
            self.cerca_richieste()
        elif x == 2:
            self.cerca_refertazione()
        elif x == 3:
            self.cerca_archivio()

    def nuovo(self):
        if self.cerca_nome.text() == '' or self.cerca_cognome.text() == '':
            QMessageBox.information(self, 'Attenzione', 'Per favore inserire nome e cognome', QMessageBox.Ok,
                                    QMessageBox.Ok)
        else:
            self.model.paziente_corrente = self.model.paziente()
            self.model.paziente_corrente.codice_paziente = get_next_value('paziente')
            self.model.paziente_corrente.cognome = self.cerca_cognome.text()
            self.model.paziente_corrente.nome = self.cerca_nome.text()
            self.model.paziente_corrente.radiologia = Ambiente.radiologia_corrente
            self.model.paziente_corrente.save()
            self.model.setta_originale()  # Copio sotto forma di dizionario il paziente corrente: "mo me lo segno!!"
            self.popola()  # Popolo i campi dell' anagrafica dettagliata come da modello
            self.tabWidget.setCurrentIndex(0)  # All'apertura di un nuovo paziente mostro sempre la sua angrafica
            self.frame_ricerca.hide()
            self.lista_pazienti.hide()
            self.frame_paziente.show()

    def calcola_codice_fiscale(self):
        if self.codice_fiscale.text() is None or self.codice_fiscale.text() == '':
            try:
                self.codice_fiscale.setText(codicefiscale.encode(self.cognome.text(), self.nome.text(), self.sesso.currentData(),
                                                             self.data_nascita.date().toPyDate().strftime("%d/%m/%Y"), self.comune_nascita.text()))
            except:
                QMessageBox.information(self, 'Attenzione', 'Errore: riempire tutti i campi necessari', QMessageBox.Ok, QMessageBox.Ok)

    def copia_residenza_domicilio(self):
        self.indirizzo_domicilio.setText(self.indirizzo_residenza.text())
        self.comune_domicilio.setText(self.comune_residenza.text())
        self.provincia_domicilio.setText(self.provincia_residenza.text())
        self.cap_domicilio.setText(self.cap_residenza.text())

    def gestione_anamnesi(self):
        anamnesi_remota_view = AnamnesiRemotaView(self.model.paziente_corrente.anamnesi_remota)
        anamnesi_remota_view.setWindowTitle(f'Anamnesi del paziente: {self.model.paziente_corrente.cognome} {self.model.paziente_corrente.nome}')
        if anamnesi_remota_view.exec_():
            self.model.paziente_corrente.anamnesi_remota = anamnesi_remota_view.anamnesi_remota.toPlainText()
        #gestire la distruzione

    def mostra_cartella_radiologica(self):
        self.tabWidget.insertTab(1, self.tab1, 'Richieste')
        self.tabWidget.insertTab(2, self.tab2, 'Refertazione')
        self.tabWidget.insertTab(3, self.tab3, 'Archivio')

    def user_capabilities(self):
        if Ambiente.utente_corrente.skill_anagrafica_pazienti == 'N':
            self.btn_nuovo.setEnabled(False)
            self.btn_cerca.setEnabled(False)
        elif Ambiente.utente_corrente.skill_anagrafica_pazienti == 'R':
            self.btn_nuovo.setEnabled(False)
            self.btn_cerca.setEnabled(True)
            self.btn_ok.setEnabled(False)
        else:
            self.btn_nuovo.setEnabled(True)
            self.btn_cerca.setEnabled(True)
            self.btn_ok.setEnabled(True)

        self.btn_nuova_richiesta.setEnabled(Ambiente.utente_corrente.flag_accettazione_clinica)
        self.btn_cartella_radiologica.setEnabled(Ambiente.utente_corrente.flag_cartella_radiologica)