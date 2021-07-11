from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QMessageBox, QDialog, QStyledItemDelegate, QTableWidgetItem
from datetime import datetime
from django.utils import timezone

from .referto_controller import RefertoController
from .referto_model import RefertoModel
from .referto_ui import Ui_Dialog_Referto
from ..ges_informazioni.informazioni_view import InformazioniView
from ..utils import Stati, Ambiente


class RefertoView(Ui_Dialog_Referto, QDialog):
    def __init__(self, model: RefertoModel, controller: RefertoController, parent=None):
        super(RefertoView, self).__init__(parent)
        self.model = model
        self.controller = controller
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)  # All'apertura di un referto mostro i dati relativi all'esame
        self.stato = Stati.CHIUSO
        self.inizializza_schede_referto()
        self.user_capabilities()
        self.popola()
        self.collega()

    def closeEvent(self, event: QCloseEvent):
        print('Chiusura dialog referto')
        self.stato = Stati.CHIUSO
        event.accept()
        # prevedere la non accettazione della chiusura per modifiche non salvate

    def accetta(self):
        # chiamo django per salvare le modifiche fatte
        if self.model.esame_corrente.stato_avanzamento == 5 and (self.testo_referto.toPlainText() is None or self.testo_referto.toPlainText() == ''):
            self.model.esame_corrente.stato_avanzamento = 4
            self.model.esame_corrente.data_ora_trascrizione = None
            self.model.esame_corrente.trascritto_da = None
        self.model.esame_corrente.save()
        self.accept()  # Chiusa la Dialog di richiesta con "accetta" devo riaggiornare la lista_richieste dell'anagrafica paziente

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

    def inizializza_schede_referto(self):
        # Settaggio dei ComboBox per le selte
        self.label_info.hide()
        delegate = QStyledItemDelegate()
        self.classe_dose_cumulativa.setItemDelegate(delegate)
        self.medico_refertatore.setItemDelegate(delegate)
        # Costruzione ComboBox medico refertatore sulla base delle alternative presenti nel DataBase
        if self.model.esame_corrente.sala_diagnostica is not None:
            for utente in self.model.esame_corrente.sala_diagnostica.utente_set.filter(tipo='MED'):
                nome_completo = f'{utente.titolo} {utente.last_name} {utente.first_name}'
                self.medico_refertatore.addItem(nome_completo, utente.id)
        index = 0
        for dose in ['', 'I Classe', 'II Classe', 'III Classe', 'IV Classe']:  # Costruzione ComboBox dose cumulativa
            self.classe_dose_cumulativa.addItem(dose, index)
            index = index+1
        # Popolare i comboBox tramite Query al DB

    def popola(self):
        self.codice_paziente.setText(str(self.model.esame_corrente.paziente.codice_paziente))
        self.nome_paziente.setText(self.model.esame_corrente.paziente.cognome + ' ' + self.model.esame_corrente.paziente.nome)
        self.codice_esame.setText(str(self.model.esame_corrente.codice_esame))
        self.data_completato.setDate(self.model.esame_corrente.data_ora_completato.date())
        # tab referto
        self.descrizione_esame.setText(self.model.esame_corrente.descrizione_esame)
        self.testo_referto.setPlainText(self.model.esame_corrente.testo_referto)

        if Ambiente.utente_corrente.tipo == 'MED':
            if self.model.esame_corrente.medico_esecutore is None:  # L'ho preso dal mucchio, il caso diventa mio
                self.medico_refertatore.setCurrentIndex(self.medico_refertatore.findData(QVariant(Ambiente.utente_corrente.id)))
                self.model.esame_corrente.medico_esecutore = Ambiente.utente_corrente
                self.model.esame_corrente.firmato_da = Ambiente.utente_corrente
            elif self.model.esame_corrente.medico_esecutore.id == Ambiente.utente_corrente.id:  # Il caso è già mio
                self.medico_refertatore.setCurrentIndex(self.medico_refertatore.findData(QVariant(Ambiente.utente_corrente.id)))
                self.model.esame_corrente.firmato_da = Ambiente.utente_corrente
            else:  # Il caso è già assegnato a un altro medico, comunico la cosa
                QMessageBox.information(self, 'Attenzione',
                                                f"L'esame è già assegnato a {self.model.esame_corrente.medico_esecutore.first_name} {self.model.esame_corrente.medico_esecutore.last_name}. \n Verrà assegnato a te.",
                                                QMessageBox.Ok, QMessageBox.Ok)
                self.medico_refertatore.setCurrentIndex(self.medico_refertatore.findData(QVariant(Ambiente.utente_corrente.id)))
                self.model.esame_corrente.medico_esecutore = Ambiente.utente_corrente
                self.model.esame_corrente.firmato_da = Ambiente.utente_corrente
        else:
            if self.model.esame_corrente.medico_esecutore is not None:  # Se c'è già il medico esecutore e non è un medico ad esseresi collegato, va già in automatico
                self.medico_refertatore.setCurrentIndex(self.medico_refertatore.findData(QVariant(self.model.esame_corrente.medico_esecutore.id)))
                self.model.esame_corrente.firmato_da = self.model.esame_corrente.medico_esecutore
            else:
                self.medico_refertatore.setCurrentIndex(-1)

        if self.model.esame_corrente.tecnico_esecutore is not None:
            nome_completo = f'{self.model.esame_corrente.tecnico_esecutore.titolo} {self.model.esame_corrente.tecnico_esecutore.last_name} {self.model.esame_corrente.tecnico_esecutore.first_name}'
            self.tecnico_esecutore.setText(nome_completo)
        # tab Dati Generici
        self.codice_esterno.setText(self.model.esame_corrente.id_cup)
        if self.model.esame_corrente.data_richiesta is not None:
            self.data_richiesta.setDate(self.model.esame_corrente.data_richiesta)
        self.impegnativa.setText(self.model.esame_corrente.numero_impegnativa)
        self.medico_richiedente.setText(self.model.esame_corrente.medico_richiedente)
        # tab anamnesi
        self.text_anamnesi.setPlainText(self.model.esame_corrente.anamnesi)
        self.text_contenuto_richiesta.setPlainText(self.model.esame_corrente.contenuto_richiesta)
        self.text_motivo_esame.setPlainText(self.model.esame_corrente.motivo_esame)
        # tab valutazioni
        if self.model.esame_corrente.classe_dose_cumulativa is not None:
            self.classe_dose_cumulativa.setCurrentIndex(self.classe_dose_cumulativa.findData(QVariant(self.model.esame_corrente.classe_dose_cumulativa)))
        else:
            self.classe_dose_cumulativa.setCurrentIndex(-1)
        self.impressioni.setPlainText(self.model.esame_corrente.impressioni)
        self.set_giudizio_qualita()

    def collega(self):
        self.testo_referto.textChanged.connect(self.set_testo_referto)
        self.medico_refertatore.currentIndexChanged.connect(self.set_medico_refertatore)
        self.text_anamnesi.textChanged.connect(self.set_text_anamnesi)
        self.text_contenuto_richiesta.textChanged.connect(self.set_text_contenuto_richiesta)
        self.text_motivo_esame.textChanged.connect(self.set_text_motivo_esame)
        self.impressioni.textChanged.connect(self.set_impressioni)
        self.rb_non_valutata.clicked.connect(self.ges_qualita)
        self.rb_bassa.clicked.connect(self.ges_qualita)
        self.rb_buona.clicked.connect(self.ges_qualita)
        self.rb_ottima.clicked.connect(self.ges_qualita)
        self.rb_non_valutato.clicked.connect(self.ges_giudizio)
        self.rb_negativo.clicked.connect(self.ges_giudizio)
        self.rb_positivo.clicked.connect(self.ges_giudizio)
        self.classe_dose_cumulativa.currentIndexChanged.connect(self.set_classe_dose_cumulativa)

    def set_testo_referto(self):
        self.model.esame_corrente.testo_referto = self.testo_referto.toPlainText()

    def set_medico_refertatore(self):
        if self.medico_refertatore.currentIndex() >= 0:
            print(Ambiente.radiologia_corrente.utenti_interni.get(id=self.medico_refertatore.currentData()))
            self.model.esame_corrente.medico_esecutore = Ambiente.radiologia_corrente.utenti_interni.get(id=self.medico_refertatore.currentData())
            self.model.esame_corrente.firmato_da = Ambiente.radiologia_corrente.utenti_interni.get(id=self.medico_refertatore.currentData())

    def set_text_anamnesi(self):
        self.model.esame_corrente.anamnesi = self.text_anamnesi.toPlainText()

    def set_text_contenuto_richiesta(self):
        self.model.esame_corrente.contenuto_richiesta = self.text_contenuto_richiesta.toPlainText()

    def set_text_motivo_esame(self):
        self.model.esame_corrente.motivo_esame = self.text_motivo_esame.toPlainText()

    def set_impressioni(self):
        self.model.esame_corrente.impressioni = self.impressioni.toPlainText()

    def set_classe_dose_cumulativa(self):
        self.model.esame_corrente.classe_dose_cumulativa = self.classe_dose_cumulativa.currentData()

    def firma_referto(self):
        if self.medico_refertatore.currentData() != Ambiente.utente_corrente.id:  # Non si può firmare a nome di un altro!
            QMessageBox.warning(self, 'Attenzione', "Attenzione: il medico refertatore non coincide con l'utente corrente", QMessageBox.Ok, QMessageBox.Ok)
            return False
        if self.testo_referto.toPlainText() is not None and self.testo_referto.toPlainText() != '':  # Si può firmare solo se è stato scritto effettivamente qualcosa nel referto
            self.model.esame_corrente.stato_avanzamento = 6  # setto lo stato dell'esame a firmato
            self.model.esame_corrente.data_ora_firma = timezone.localtime()
            self.model.esame_corrente.firmato_da = Ambiente.utente_corrente
            return True
        return False

    def firma(self):
        if self.firma_referto():
            self.accetta()

    def stampa(self):
        print('Sto stampando il referto')

    def firma_stampa(self):
        if self.firma_referto():
            self.stampa()
            self.accetta()

    def referto_modificato(self):
        if Ambiente.utente_corrente.flag_firma_referto:
            if self.testo_referto.toPlainText() == '':
                self.label_info.show()
                self.btn_firma.setEnabled(False)
                self.btn_firma_stampa.setEnabled(False)
            else:
                self.label_info.hide()
                self.btn_firma.setEnabled(True)
                self.btn_firma_stampa.setEnabled(True)
        else:
            self.label_info.hide()
            self.btn_firma.setEnabled(False)
            self.btn_firma_stampa.setEnabled(False)
        self.btn_trascritto.setEnabled(self.testo_referto.toPlainText() != '' and self.model.esame_corrente.stato_avanzamento < 5)

    def mostra_informazioni(self):
        informazioni_view = InformazioniView(self.model.esame_corrente)
        informazioni_view.exec_()

    def trascritto(self):
        if self.medico_refertatore.currentIndex() >= 0:  # C'è qualcuno selezionato
            self.model.esame_corrente.stato_avanzamento = 5
            self.model.esame_corrente.data_ora_trascrizione = timezone.localtime()
            self.model.esame_corrente.trascritto_da = Ambiente.utente_corrente
            self.model.esame_corrente.save()
            self.accept()
        else:
            QMessageBox.warning(self, 'Attenzione', "Attenzione: il medico refertatore non è stato selezionato", QMessageBox.Ok, QMessageBox.Ok)

    def user_capabilities(self):
        if Ambiente.utente_corrente.tipo == 'MED':
            self.btn_trascritto.hide()
            self.btn_firma.show()
            self.btn_firma_stampa.show()
        else:
            self.btn_trascritto.show()
            self.btn_firma.hide()
            self.btn_firma_stampa.hide()

    def set_giudizio_qualita(self):
        self.rb_non_valutato.setChecked(self.model.esame_corrente.giudizio == 'NV')
        self.rb_negativo.setChecked(self.model.esame_corrente.giudizio == 'NEG')
        self.rb_positivo.setChecked(self.model.esame_corrente.giudizio == 'POS')
        self.rb_non_valutata.setChecked(self.model.esame_corrente.qualita_esame == 'NV')
        self.rb_bassa.setChecked(self.model.esame_corrente.qualita_esame == 'BAS')
        self.rb_buona.setChecked(self.model.esame_corrente.qualita_esame == 'BUO')
        self.rb_ottima.setChecked(self.model.esame_corrente.qualita_esame == 'OTT')

    def ges_qualita(self):
        if self.rb_non_valutata.isChecked():
            self.model.esame_corrente.qualita_esame = 'NV'
        elif self.rb_bassa.isChecked():
            self.model.esame_corrente.qualita_esame = 'BAS'
        elif self.rb_buona.isChecked():
            self.model.esame_corrente.qualita_esame = 'BUO'
        else:
            self.model.esame_corrente.qualita_esame = 'OTT'

    def ges_giudizio(self):
        if self.rb_non_valutato.isChecked():
            self.model.esame_corrente.giudizio = 'NV'
        elif self.rb_negativo.isChecked():
            self.model.esame_corrente.giudizio = 'NEG'
        else:
            self.model.esame_corrente.giudizio = 'POS'
