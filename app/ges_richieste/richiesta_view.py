from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog, QStyledItemDelegate, QTableWidgetItem
from datetime import datetime
from django.utils import timezone

from .richiesta_controller import RichiestaController
from .richiesta_model import RichiestaModel
from .richiesta_ui import Ui_Dialog_Richiesta
from ..ges_informazioni.informazioni_view import InformazioniView
from ..utils import Stati, Ambiente
from ..ges_prestazioni.prestazioni_controller import PrestazioniController
from ..ges_prestazioni.prestazioni_model import PrestazioniModel
from ..ges_prestazioni.prestazioni_view import PrestazioniView


class RichiestaView(Ui_Dialog_Richiesta, QDialog):
    def __init__(self, model: RichiestaModel, controller: RichiestaController, parent=None):
        super(RichiestaView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)  # All'apertura di una richiesta mostro i dati relativi all'esame
        self.stato = Stati.CHIUSO
        self.btn_remove_prestazione.setEnabled(False)
        # blocco gli automatismi durante la costruzione della finestra
        self.sala_diagnostica.blockSignals(True)
        self.attrezzatura.blockSignals(True)
        self.medico_esecutore.blockSignals(True)
        self.tecnico_esecutore.blockSignals(True)
        self.inizializza_schede_richiesta()
        self.popola()
        # riattivo gli automatismi
        self.sala_diagnostica.blockSignals(False)
        self.attrezzatura.blockSignals(False)
        self.medico_esecutore.blockSignals(False)
        self.tecnico_esecutore.blockSignals(False)
        self.collega()
        self.set_bottoni_esecuzione()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura dialog richiesta')
        self.stato = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def modificato(self):
        self.stato = Stati.MODIFICATO

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        if self.model.esame_corrente.sala_diagnostica is not None and self.model.esame_corrente.attrezzatura is not None:
            self.model.esame_corrente.save()
            self.accept()  # Chiusa la Dialog di richiesta con "accetta" devo riaggiornare la lista_richieste dell'anagrafica paziente
        else:
            QMessageBox.information(self, 'Attenzione', 'Per favore inserire sala diagnostica e modalità', QMessageBox.Ok,
                                   QMessageBox.Ok)
            # Volendo lanciare eccezione da controllare

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

    def set_bottoni_esecuzione(self):
        if self.model.esame_corrente.stato_avanzamento < 3:
            self.btn_inizia_esame.show()
            self.btn_completa_esame.hide()
        elif self.model.esame_corrente.stato_avanzamento == 3:
            self.btn_inizia_esame.hide()
            self.btn_completa_esame.show()
        elif self.model.esame_corrente.stato_avanzamento >= 4:
            self.btn_inizia_esame.hide()
            self.btn_completa_esame.hide()

    def add_prestazione(self):
        print("aggiungo una prestazione")
        prestazioni_model = PrestazioniModel()
        prestazioni_controller = PrestazioniController(prestazioni_model)
        prestazioni_view = PrestazioniView(prestazioni_model, prestazioni_controller)
        if prestazioni_view.exec_():
            print(prestazioni_view.model.prestazione_corrente)
            la_prestazione = self.model.prestazione()
            la_prestazione.procedura = prestazioni_view.model.prestazione_corrente
            la_prestazione.modificatore = prestazioni_view.modificatore.text()
            la_prestazione.commento = prestazioni_view.commento.text()
            la_prestazione.esame = self.model.esame_corrente
            la_prestazione.save()
            self.carica_prestazioni()

    def abilita_bottone_rimuovi(self):
        self.btn_remove_prestazione.setEnabled(True)

    def remove_prestazione(self):
        if self.lista_prestazioni.currentRow() >= 0:
            self.model.qs_prestazioni[self.lista_prestazioni.currentRow()].delete()
            self.carica_prestazioni()
            self.lista_prestazioni.clearSelection()
            self.btn_remove_prestazione.setEnabled(False)

    def inizializza_schede_richiesta(self):
        self.lista_prestazioni.setColumnCount(2)
        self.lista_prestazioni.setHorizontalHeaderLabels(['Prestazione', 'Modificatore'])
        self.lista_prestazioni.setColumnWidth(0, 328)
        self.lista_prestazioni.setColumnWidth(1, 327)
        # Settaggio dei ComboBox per le selte
        delegate = QStyledItemDelegate()
        self.sala_diagnostica.setItemDelegate(delegate)
        self.attrezzatura.setItemDelegate(delegate)
        self.medico_esecutore.setItemDelegate(delegate)
        self.tecnico_esecutore.setItemDelegate(delegate)
        self.classe_dose_cumulativa.setItemDelegate(delegate)
        for sala_diagnostica in Ambiente.sale_diagnostiche_correnti:  # Costruzione ComboBox sale diagnostiche sulla base delle alternative presenti nel DataBase
            self.sala_diagnostica.addItem(sala_diagnostica.nome, sala_diagnostica.id)
        if self.model.esame_corrente.sala_diagnostica is not None:
            for attrezzatura in self.model.esame_corrente.sala_diagnostica.attrezzature.all():  # Costruzione ComboBox attrezzature sulla base delle alternative presenti nel DataBase
                self.attrezzatura.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)
            for utente in self.model.esame_corrente.sala_diagnostica.utente_set.filter(tipo='MED'):  # Costruzione ComboBox medico esecutore sulla base delle alternative presenti nel DataBase
                nome_completo = f'{utente.titolo} {utente.last_name} {utente.first_name}'
                self.medico_esecutore.addItem(nome_completo, utente.id)
            for utente in self.model.esame_corrente.sala_diagnostica.utente_set.filter(tipo='TEC'):  # Costruzione ComboBox tecnico esecutore sulla base delle alternative presenti nel DataBase
                nome_completo = f'{utente.titolo} {utente.last_name} {utente.first_name}'
                self.tecnico_esecutore.addItem(nome_completo, utente.id)

        index = 0
        for dose in ['', 'I Classe', 'II Classe', 'III Classe', 'IV Classe']:  # Costruzione ComboBox dose cumulativa
            self.classe_dose_cumulativa.addItem(dose, index)
            index = index+1

    def sala_diagnostica_changed(self, index):
        if index >= 0:
            self.attrezzatura.clear()
            self.medico_esecutore.clear()
            self.tecnico_esecutore.clear()
            print('sala diagnostica ' + str(index))
            self.model.esame_corrente.sala_diagnostica = Ambiente.sale_diagnostiche_correnti.get(id=self.sala_diagnostica.currentData())
            # per modificare i comboBox di attrezzature, medico esecutore e tecnico esecutore blocco gli automatismi dell'interfaccia
            self.attrezzatura.blockSignals(True)
            self.medico_esecutore.blockSignals(True)
            self.tecnico_esecutore.blockSignals(True)
            for attrezzatura in self.model.esame_corrente.sala_diagnostica.attrezzature.all():  # Costruzione ComboBox attrezzature sulla base delle alternative presenti nel DataBase
                self.attrezzatura.addItem(attrezzatura.dicom_ae_title, attrezzatura.id)
            for utente in self.model.esame_corrente.sala_diagnostica.utente_set.filter(tipo='MED'):  # Costruzione ComboBox medico esecutore sulla base delle alternative presenti nel DataBase
                nome_completo = f'{utente.titolo} {utente.last_name} {utente.first_name}'
                self.medico_esecutore.addItem(nome_completo, utente.id)
            for utente in self.model.esame_corrente.sala_diagnostica.utente_set.filter(tipo='TEC'):  # Costruzione ComboBox tecnico esecutore sulla base delle alternative presenti nel DataBase
                nome_completo = f'{utente.titolo} {utente.last_name} {utente.first_name}'
                self.tecnico_esecutore.addItem(nome_completo, utente.id)
            # Avendo cambiato la sala diagnostica, resetto l'interfaccia pulendo tutti i comboBox creati e setto a null le Foreign Keys
            # così da annullare le eventuali relazioni esistenti tra esame corrente e attrezzatura, medico esecutore e tecnico esecutore
            self.attrezzatura.setCurrentIndex(-1)
            self.medico_esecutore.setCurrentIndex(-1)
            self.tecnico_esecutore.setCurrentIndex(-1)
            self.model.esame_corrente.attrezzatura_id = None
            self.model.esame_corrente.medico_esecutore_id = None
            self.model.esame_corrente.tecnico_esecutore_id = None
            # tutto fatto, riattivo gli automatismi
            self.attrezzatura.blockSignals(False)
            self.medico_esecutore.blockSignals(False)
            self.tecnico_esecutore.blockSignals(False)

    def attrezzatura_changed(self, index):
        if index >= 0:
            print('attrezzatura ' + str(index))
            self.model.esame_corrente.attrezzatura = self.model.esame_corrente.sala_diagnostica.attrezzature.get(id=self.attrezzatura.currentData())
            print(self.model.esame_corrente.attrezzatura)

    def medico_esecutore_changed(self, index):
        if index >= 0:
            print('medico esecutore ' + str(index))
            self.model.esame_corrente.medico_esecutore = self.model.esame_corrente.sala_diagnostica.utente_set.get(
                id=self.medico_esecutore.currentData())
            print(self.model.esame_corrente.medico_esecutore)

    def tecnico_esecutore_changed(self, index):
        if index >= 0:
            print('tecnico esecutore ' + str(index))
            self.model.esame_corrente.tecnico_esecutore = self.model.esame_corrente.sala_diagnostica.utente_set.get(
                id=self.tecnico_esecutore.currentData())
            print(self.model.esame_corrente.tecnico_esecutore)

    def popola(self):
        self.codice_paziente.setText(str(self.model.esame_corrente.paziente.codice_paziente))
        self.nome_paziente.setText(self.model.esame_corrente.paziente.cognome + ' ' + self.model.esame_corrente.paziente.nome)
        self.codice_esame.setText(str(self.model.esame_corrente.codice_esame))
        # tab Esame
        self.carica_prestazioni()
        self.data_ora_schedulato.setDateTime(self.model.esame_corrente.data_ora_schedulato.astimezone(timezone.get_default_timezone()))
        self.flag_urgente.setChecked(self.model.esame_corrente.flag_urgente)
        if self.model.esame_corrente.sala_diagnostica is not None:
            self.sala_diagnostica.setCurrentIndex(self.sala_diagnostica.findData(QVariant(self.model.esame_corrente.sala_diagnostica.id)))
        else:
            self.sala_diagnostica.setCurrentIndex(-1)
            self.attrezzatura.clear()
            self.medico_esecutore.clear()
            self.tecnico_esecutore.clear()
        if self.model.esame_corrente.attrezzatura is not None:
            self.attrezzatura.setCurrentIndex(self.attrezzatura.findData(QVariant(self.model.esame_corrente.attrezzatura.id)))
        else:
            self.attrezzatura.setCurrentIndex(-1)
        # tab Dati Generici
        self.codice_esterno.setText(self.model.esame_corrente.id_cup)
        if self.model.esame_corrente.data_richiesta is not None:
            self.data_richiesta.setDate(self.model.esame_corrente.data_richiesta)
        self.impegnativa.setText(self.model.esame_corrente.numero_impegnativa)
        self.medico_richiedente.setText(self.model.esame_corrente.medico_richiedente)
        # tab Anamnesi
        self.text_anamnesi.setPlainText(self.model.esame_corrente.anamnesi)
        self.text_contenuto_richiesta.setPlainText(self.model.esame_corrente.contenuto_richiesta)
        self.text_motivo_esame.setPlainText(self.model.esame_corrente.motivo_esame)
        # tab Completamento
        if self.model.esame_corrente.data_ora_inizio is not None:
            self.data_ora_iniziato.setDateTime(self.model.esame_corrente.data_ora_inizio.astimezone(timezone.get_default_timezone()))
        if self.model.esame_corrente.data_ora_completato is not None:
            self.data_ora_completato.setDateTime(self.model.esame_corrente.data_ora_completato.astimezone(timezone.get_default_timezone()))
        if self.model.esame_corrente.medico_esecutore is not None:
            self.medico_esecutore.setCurrentIndex(self.medico_esecutore.findData(QVariant(self.model.esame_corrente.medico_esecutore.id)))
        else:
            self.medico_esecutore.setCurrentIndex(-1)
        if self.model.esame_corrente.tecnico_esecutore is not None:
            self.tecnico_esecutore.setCurrentIndex(self.tecnico_esecutore.findData(QVariant(self.model.esame_corrente.tecnico_esecutore.id)))
        else:
            self.tecnico_esecutore.setCurrentIndex(-1)
        if self.model.esame_corrente.classe_dose_cumulativa is not None:
            self.classe_dose_cumulativa.setCurrentIndex(self.classe_dose_cumulativa.findData(QVariant(self.model.esame_corrente.classe_dose_cumulativa)))
        else:
            self.classe_dose_cumulativa.setCurrentIndex(-1)
        self.flag_produzione_cd.setChecked(self.model.esame_corrente.flag_produzione_CD)

    def carica_prestazioni(self):  # Ricerco le prestazioni e costruisco la lista da mostrare
        self.controller.cerca_prestazioni()
        self.lista_prestazioni.setRowCount(len(self.model.qs_prestazioni))
        index = 0
        for prestazione in self.model.qs_prestazioni:
            self.lista_prestazioni.setItem(index, 0, QTableWidgetItem(prestazione.procedura.descrizione))
            self.lista_prestazioni.setItem(index, 1, QTableWidgetItem(prestazione.modificatore))
            index = index + 1
        self.riassunto()

    def riassunto(self):
        rias = ''
        for prestazione in self.model.qs_prestazioni:
            rias = rias + prestazione.procedura.descrizione + ' - '
        if rias != '':
            rias = rias[0:len(rias)-3]
        self.model.esame_corrente.descrizione_esame = rias

    def collega(self):
        self.data_ora_schedulato.dateTimeChanged.connect(self.set_data_ora_schedulato)
        self.flag_urgente.stateChanged.connect(self.set_flag_urgente)
        self.codice_esterno.textChanged.connect(self.set_codice_esterno)
        self.data_richiesta.dateChanged.connect(self.set_data_richiesta)
        self.impegnativa.textChanged.connect(self.set_impegnativa)
        self.medico_richiedente.textChanged.connect(self.set_medico_richiedente)
        self.text_anamnesi.textChanged.connect(self.set_text_anamnesi)
        self.text_contenuto_richiesta.textChanged.connect(self.set_text_contenuto_richiesta)
        self.text_motivo_esame.textChanged.connect(self.set_text_motivo_esame)
        self.data_ora_iniziato.dateTimeChanged.connect(self.set_data_ora_iniziato)
        self.data_ora_completato.dateTimeChanged.connect(self.set_data_ora_completato)
        self.classe_dose_cumulativa.currentIndexChanged.connect(self.set_classe_dose_cumulativa)
        self.flag_produzione_cd.stateChanged.connect(self.set_flag_produzione_cd)

    def set_data_ora_schedulato(self):
        self.model.esame_corrente.data_ora_schedulato = self.data_ora_schedulato.dateTime().toPyDateTime()

    def set_flag_urgente(self):
        self.model.esame_corrente.flag_urgente = self.flag_urgente.isChecked()

    def set_codice_esterno(self):
        self.model.esame_corrente.id_cup = self.codice_esterno.text()

    def set_data_richiesta(self):
        self.model.esame_corrente.data_richiesta = self.data_richiesta.date().toPyDate()

    def set_impegnativa(self):
        self.model.esame_corrente.numero_impegnativa = self.impegnativa.text()

    def set_medico_richiedente(self):
        self.model.esame_corrente.medico_richiedente = self.medico_richiedente.text()

    def set_text_anamnesi(self):
        self.model.esame_corrente.anamnesi = self.text_anamnesi.toPlainText()

    def set_text_contenuto_richiesta(self):
        self.model.esame_corrente.contenuto_richiesta = self.text_contenuto_richiesta.toPlainText()

    def set_text_motivo_esame(self):
        self.model.esame_corrente.motivo_esame = self.text_motivo_esame.toPlainText()

    def set_data_ora_iniziato(self):
        self.model.esame_corrente.data_ora_inizio = self.data_ora_iniziato.dateTime().toPyDateTime()

    def set_data_ora_completato(self):
        self.model.esame_corrente.data_ora_completato = self.data_ora_completato.dateTime().toPyDateTime()

    def set_classe_dose_cumulativa(self):
        self.model.esame_corrente.classe_dose_cumulativa = self.classe_dose_cumulativa.currentData()

    def set_flag_produzione_cd(self):
        self.model.esame_corrente.flag_produzione_CD = self.flag_produzione_cd.isChecked()

    def completa_esame(self):
        # per adesso fa solo questo
        self.model.esame_corrente.stato_avanzamento = 4  # setto lo stato dell'esame a completato
        self.data_ora_completato.setDateTime(timezone.localtime())
        self.model.esame_corrente.completato_da = Ambiente.utente_corrente
        self.model.esame_corrente.save()
        self.set_bottoni_esecuzione()

    def inizia_esame(self):
        self.model.esame_corrente.stato_avanzamento = 3  # setto lo stato dell'esame a iniziato
        self.data_ora_iniziato.setDateTime(timezone.localtime())
        self.model.esame_corrente.iniziato_da = Ambiente.utente_corrente
        self.model.esame_corrente.save()
        self.set_bottoni_esecuzione()

    def mostra_informazioni(self):
        informazioni_view = InformazioniView(self.model.esame_corrente)
        informazioni_view.exec_()
