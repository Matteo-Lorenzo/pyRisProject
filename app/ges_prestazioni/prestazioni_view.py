from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog, QStyledItemDelegate, QTableWidgetItem

from .prestazioni_controller import PrestazioniController
from .prestazioni_model import PrestazioniModel
from .prestazioni_ui import Ui_Prestazioni


class PrestazioniView(Ui_Prestazioni, QDialog):
    def __init__(self, model: PrestazioniModel, controller: PrestazioniController, parent=None):
        super(PrestazioniView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.inizializza_scheda_prestazioni()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura componente aggiunta prestazioni')
        event.accept()

    def accetta(self):
        # procedo a salvare le modifiche fatte
        print("prestazione aggiunta")
        self.model.prestazione_corrente = self.model.qs_prestazioni[self.lista_prestazioni.currentRow()]
        self.accept()  # Se la finestra è stata chiusa con "accetta" devo aggiungere la prestazione selezionata
                        # all'esame corrente nella richiesta (e visualizzarlo)

    def annulla(self):
        # rendo la finestra chiudibile senza salvare le modifiche fatte
        print("nessuna prestazione aggiunta")
        self.close()

    def inizializza_scheda_prestazioni(self):
        # Settaggio dei ComboBox per le selte
        delegate = QStyledItemDelegate()
        self.comboBox_metodica.setItemDelegate(delegate)
        self.comboBox_apparato.setItemDelegate(delegate)
        self.comboBox_organo.setItemDelegate(delegate)

        self.lista_prestazioni.setColumnCount(1)
        self.lista_prestazioni.setHorizontalHeaderLabels(['Prestazione'])
        self.lista_prestazioni.setColumnWidth(0, 420)

        self.carica_metodiche()

    def carica_metodiche(self):
        self.controller.carica_metodiche()
        for metodica in self.model.qs_metodiche:  # Costruzione ComboBox Metotiche sulla base delle alternative presenti nel DataBase
            self.comboBox_metodica.addItem(metodica.descrizione, metodica.codice)
        #self.comboBox_metodica.setCurrentIndex(0)
        self.model.metodica_corrente = self.model.qs_metodiche[0]

    def carica_apparati(self):
        self.controller.carica_apparati()
        self.model.apparato_corrente = self.model.qs_apparati[0]
        self.comboBox_apparato.clear()
        for apparato in self.model.qs_apparati:  # Costruzione ComboBox Apparati sulla base delle alternative presenti nel DataBase
            self.comboBox_apparato.addItem(apparato.descrizione, apparato.codice)
        #self.comboBox_apparato.setCurrentIndex(0)
        self.carica_organi()

    def carica_organi(self):
        self.controller.carica_organi()
        self.model.organo_corrente = self.model.qs_organi[0]
        self.comboBox_organo.clear()
        for organo in self.model.qs_organi:  # Costruzione ComboBox Organi sulla base delle alternative presenti nel DataBase
            self.comboBox_organo.addItem(organo.descrizione, organo.codice)
        #self.comboBox_organo.setCurrentIndex(0)
        self.carica_prestazioni()

    def carica_prestazioni(self):
        self.controller.carica_prestazioni()
        self.lista_prestazioni.setRowCount(len(self.model.qs_prestazioni))
        index = 0
        for nomenclatorePrestazioni in self.model.qs_prestazioni:
            self.lista_prestazioni.setItem(index, 0, QTableWidgetItem(nomenclatorePrestazioni.descrizione))
            index = index + 1

    def metodica_changed(self, index):
        if index >= 0:
            print('metodica ' + str(index))
            self.model.metodica_corrente = self.model.qs_metodiche[index]
            print(f'metodica selezionata {self.model.metodica_corrente.descrizione}')
            self.carica_apparati()

    def apparato_changed(self, index):
        if index >= 0:
            print('apparato ' + str(index))
            self.model.apparato_corrente = self.model.qs_apparati[index]
            print(f'apparato selezionato {self.model.apparato_corrente.descrizione}')
            self.carica_organi()

    def organo_changed(self, index):
        if index >= 0:
            print('organo ' + str(index))
            self.model.organo_corrente = self.model.qs_organi[index]
            print(f'organo selezionato {self.model.organo_corrente.descrizione}')
            self.carica_prestazioni()
