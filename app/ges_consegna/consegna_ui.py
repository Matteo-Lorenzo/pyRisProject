# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'consegna.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Consegna(object):
    def setupUi(self, Consegna):
        Consegna.setObjectName("Consegna")
        Consegna.resize(1200, 800)
        self.label = QtWidgets.QLabel(Consegna)
        self.label.setGeometry(QtCore.QRect(10, -10, 211, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btn_ok = QtWidgets.QPushButton(Consegna)
        self.btn_ok.setGeometry(QtCore.QRect(920, 720, 113, 32))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_cancel = QtWidgets.QPushButton(Consegna)
        self.btn_cancel.setGeometry(QtCore.QRect(1050, 720, 113, 32))
        self.btn_cancel.setObjectName("btn_cancel")
        self.label_7 = QtWidgets.QLabel(Consegna)
        self.label_7.setGeometry(QtCore.QRect(51, 54, 81, 20))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.cerca_codice_esame = QtWidgets.QLineEdit(Consegna)
        self.cerca_codice_esame.setGeometry(QtCore.QRect(270, 54, 131, 21))
        self.cerca_codice_esame.setText("")
        self.cerca_codice_esame.setMaxLength(40)
        self.cerca_codice_esame.setObjectName("cerca_codice_esame")
        self.label_9 = QtWidgets.QLabel(Consegna)
        self.label_9.setGeometry(QtCore.QRect(420, 54, 111, 20))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.cerca_nome_paziente = QtWidgets.QLineEdit(Consegna)
        self.cerca_nome_paziente.setGeometry(QtCore.QRect(780, 54, 131, 21))
        self.cerca_nome_paziente.setText("")
        self.cerca_nome_paziente.setMaxLength(80)
        self.cerca_nome_paziente.setObjectName("cerca_nome_paziente")
        self.btn_reset = QtWidgets.QPushButton(Consegna)
        self.btn_reset.setGeometry(QtCore.QRect(1060, 50, 81, 32))
        self.btn_reset.setObjectName("btn_reset")
        self.cerca_codice_paziente = QtWidgets.QLineEdit(Consegna)
        self.cerca_codice_paziente.setGeometry(QtCore.QRect(540, 54, 113, 21))
        self.cerca_codice_paziente.setObjectName("cerca_codice_paziente")
        self.label_10 = QtWidgets.QLabel(Consegna)
        self.label_10.setGeometry(QtCore.QRect(160, 54, 101, 20))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.btn_cerca = QtWidgets.QPushButton(Consegna)
        self.btn_cerca.setGeometry(QtCore.QRect(940, 50, 81, 32))
        self.btn_cerca.setObjectName("btn_cerca")
        self.label_8 = QtWidgets.QLabel(Consegna)
        self.label_8.setGeometry(QtCore.QRect(660, 54, 111, 20))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.lista_esami = QtWidgets.QTableWidget(Consegna)
        self.lista_esami.setGeometry(QtCore.QRect(10, 100, 1180, 301))
        self.lista_esami.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lista_esami.setAlternatingRowColors(True)
        self.lista_esami.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lista_esami.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lista_esami.setObjectName("lista_esami")
        self.lista_esami.setColumnCount(6)
        self.lista_esami.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.lista_esami.setHorizontalHeaderItem(5, item)
        self.lista_esami.horizontalHeader().setDefaultSectionSize(196)
        self.lista_esami.verticalHeader().setVisible(False)
        self.frame = QtWidgets.QFrame(Consegna)
        self.frame.setGeometry(QtCore.QRect(10, 420, 1181, 281))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.schedulato_da = QtWidgets.QLineEdit(self.frame)
        self.schedulato_da.setGeometry(QtCore.QRect(270, 80, 91, 23))
        self.schedulato_da.setReadOnly(True)
        self.schedulato_da.setObjectName("schedulato_da")
        self.data_ora_accettato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_accettato.setEnabled(False)
        self.data_ora_accettato.setGeometry(QtCore.QRect(140, 50, 131, 24))
        self.data_ora_accettato.setReadOnly(True)
        self.data_ora_accettato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_accettato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_accettato.setObjectName("data_ora_accettato")
        self.data_ora_completato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_completato.setEnabled(False)
        self.data_ora_completato.setGeometry(QtCore.QRect(530, 50, 131, 24))
        self.data_ora_completato.setReadOnly(True)
        self.data_ora_completato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_completato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_completato.setObjectName("data_ora_completato")
        self.data_ora_firmato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_firmato.setEnabled(False)
        self.data_ora_firmato.setGeometry(QtCore.QRect(900, 20, 131, 24))
        self.data_ora_firmato.setReadOnly(True)
        self.data_ora_firmato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_firmato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_firmato.setObjectName("data_ora_firmato")
        self.data_ora_consegnato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_consegnato.setEnabled(False)
        self.data_ora_consegnato.setGeometry(QtCore.QRect(900, 50, 131, 24))
        self.data_ora_consegnato.setReadOnly(True)
        self.data_ora_consegnato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_consegnato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_consegnato.setObjectName("data_ora_consegnato")
        self.consegnato_da = QtWidgets.QLineEdit(self.frame)
        self.consegnato_da.setGeometry(QtCore.QRect(1030, 50, 91, 23))
        self.consegnato_da.setReadOnly(True)
        self.consegnato_da.setObjectName("consegnato_da")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(60, 80, 81, 22))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(450, 80, 81, 22))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(450, 20, 81, 22))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(810, 50, 91, 22))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 20, 81, 22))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(820, 80, 81, 22))
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(450, 50, 81, 22))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.data_ora_schedulato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_schedulato.setEnabled(False)
        self.data_ora_schedulato.setGeometry(QtCore.QRect(140, 80, 131, 24))
        self.data_ora_schedulato.setReadOnly(True)
        self.data_ora_schedulato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_schedulato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_schedulato.setObjectName("data_ora_schedulato")
        self.data_ora_iniziato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_iniziato.setEnabled(False)
        self.data_ora_iniziato.setGeometry(QtCore.QRect(530, 20, 131, 24))
        self.data_ora_iniziato.setReadOnly(True)
        self.data_ora_iniziato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_iniziato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_iniziato.setObjectName("data_ora_iniziato")
        self.prenotato_da = QtWidgets.QLineEdit(self.frame)
        self.prenotato_da.setGeometry(QtCore.QRect(270, 20, 91, 23))
        self.prenotato_da.setReadOnly(True)
        self.prenotato_da.setObjectName("prenotato_da")
        self.trascritto_da = QtWidgets.QLineEdit(self.frame)
        self.trascritto_da.setGeometry(QtCore.QRect(660, 80, 91, 23))
        self.trascritto_da.setReadOnly(True)
        self.trascritto_da.setObjectName("trascritto_da")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(820, 20, 81, 22))
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.data_ora_consegna = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_consegna.setEnabled(True)
        self.data_ora_consegna.setGeometry(QtCore.QRect(990, 190, 131, 24))
        self.data_ora_consegna.setReadOnly(False)
        self.data_ora_consegna.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_consegna.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_consegna.setObjectName("data_ora_consegna")
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(830, 190, 151, 22))
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.data_ora_prenotato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_prenotato.setEnabled(False)
        self.data_ora_prenotato.setGeometry(QtCore.QRect(140, 20, 131, 24))
        self.data_ora_prenotato.setReadOnly(True)
        self.data_ora_prenotato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_prenotato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_prenotato.setObjectName("data_ora_prenotato")
        self.data_ora_annullato = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_annullato.setEnabled(False)
        self.data_ora_annullato.setGeometry(QtCore.QRect(900, 80, 131, 24))
        self.data_ora_annullato.setReadOnly(True)
        self.data_ora_annullato.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_annullato.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_annullato.setObjectName("data_ora_annullato")
        self.data_ora_trascritto = QtWidgets.QDateTimeEdit(self.frame)
        self.data_ora_trascritto.setEnabled(False)
        self.data_ora_trascritto.setGeometry(QtCore.QRect(530, 80, 131, 24))
        self.data_ora_trascritto.setReadOnly(True)
        self.data_ora_trascritto.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.data_ora_trascritto.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.data_ora_trascritto.setObjectName("data_ora_trascritto")
        self.firmato_da = QtWidgets.QLineEdit(self.frame)
        self.firmato_da.setGeometry(QtCore.QRect(1030, 20, 91, 23))
        self.firmato_da.setReadOnly(True)
        self.firmato_da.setObjectName("firmato_da")
        self.iniziato_da = QtWidgets.QLineEdit(self.frame)
        self.iniziato_da.setGeometry(QtCore.QRect(660, 20, 91, 23))
        self.iniziato_da.setReadOnly(True)
        self.iniziato_da.setObjectName("iniziato_da")
        self.accettato_da = QtWidgets.QLineEdit(self.frame)
        self.accettato_da.setGeometry(QtCore.QRect(270, 50, 91, 23))
        self.accettato_da.setReadOnly(True)
        self.accettato_da.setObjectName("accettato_da")
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(60, 50, 81, 22))
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.annullato_da = QtWidgets.QLineEdit(self.frame)
        self.annullato_da.setGeometry(QtCore.QRect(1030, 80, 91, 23))
        self.annullato_da.setReadOnly(True)
        self.annullato_da.setObjectName("annullato_da")
        self.completato_da = QtWidgets.QLineEdit(self.frame)
        self.completato_da.setGeometry(QtCore.QRect(660, 50, 91, 23))
        self.completato_da.setReadOnly(True)
        self.completato_da.setObjectName("completato_da")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(70, 190, 181, 22))
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(70, 120, 291, 51))
        self.groupBox.setObjectName("groupBox")
        self.rb_paziente = QtWidgets.QRadioButton(self.groupBox)
        self.rb_paziente.setGeometry(QtCore.QRect(10, 25, 100, 20))
        self.rb_paziente.setObjectName("rb_paziente")
        self.rb_altri = QtWidgets.QRadioButton(self.groupBox)
        self.rb_altri.setGeometry(QtCore.QRect(140, 25, 81, 20))
        self.rb_altri.setObjectName("rb_altri")
        self.consegnato_a = QtWidgets.QPlainTextEdit(self.frame)
        self.consegnato_a.setGeometry(QtCore.QRect(270, 190, 481, 79))
        self.consegnato_a.setObjectName("consegnato_a")

        self.retranslateUi(Consegna)
        self.btn_ok.clicked.connect(Consegna.accetta)
        self.btn_cancel.clicked.connect(Consegna.annulla)
        QtCore.QMetaObject.connectSlotsByName(Consegna)

    def retranslateUi(self, Consegna):
        _translate = QtCore.QCoreApplication.translate
        Consegna.setWindowTitle(_translate("Consegna", "Form"))
        self.label.setText(_translate("Consegna", "Procedura di Consegna"))
        self.btn_ok.setText(_translate("Consegna", "Salva"))
        self.btn_cancel.setText(_translate("Consegna", "Annulla"))
        self.label_7.setText(_translate("Consegna", "Ricerca per:"))
        self.label_9.setText(_translate("Consegna", "Codice Paziente:"))
        self.btn_reset.setText(_translate("Consegna", "Reset"))
        self.label_10.setText(_translate("Consegna", "Codice Esame:"))
        self.btn_cerca.setText(_translate("Consegna", "Cerca"))
        self.btn_cerca.setShortcut(_translate("Consegna", "Return"))
        self.label_8.setText(_translate("Consegna", "Nome Paziente:"))
        item = self.lista_esami.horizontalHeaderItem(0)
        item.setText(_translate("Consegna", "Codice Paziente"))
        item = self.lista_esami.horizontalHeaderItem(1)
        item.setText(_translate("Consegna", "Nome Paziente"))
        item = self.lista_esami.horizontalHeaderItem(2)
        item.setText(_translate("Consegna", "Codice Esame"))
        item = self.lista_esami.horizontalHeaderItem(3)
        item.setText(_translate("Consegna", "Descrizione"))
        item = self.lista_esami.horizontalHeaderItem(4)
        item.setText(_translate("Consegna", "Data Esame"))
        item = self.lista_esami.horizontalHeaderItem(5)
        item.setText(_translate("Consegna", "Data Firma"))
        self.data_ora_accettato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_completato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_firmato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_consegnato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.label_3.setText(_translate("Consegna", "Schedulato:"))
        self.label_6.setText(_translate("Consegna", "Trascritto:"))
        self.label_4.setText(_translate("Consegna", "Iniziato:"))
        self.label_11.setText(_translate("Consegna", "Consegnato:"))
        self.label_2.setText(_translate("Consegna", "Prenotato:"))
        self.label_12.setText(_translate("Consegna", "Annullato:"))
        self.label_5.setText(_translate("Consegna", "Completato:"))
        self.data_ora_schedulato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_iniziato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.label_13.setText(_translate("Consegna", "Firmato:"))
        self.data_ora_consegna.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.label_14.setText(_translate("Consegna", "Data e ora consegna:"))
        self.data_ora_prenotato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_annullato.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.data_ora_trascritto.setDisplayFormat(_translate("Consegna", "dd/MM/yyyy HH:mm"))
        self.label_15.setText(_translate("Consegna", "Accettato:"))
        self.label_16.setText(_translate("Consegna", "Dati anagrafici del ritirante:"))
        self.groupBox.setTitle(_translate("Consegna", "Consegna:"))
        self.rb_paziente.setText(_translate("Consegna", "Al Paziente"))
        self.rb_altri.setText(_translate("Consegna", "Ad Altri"))
