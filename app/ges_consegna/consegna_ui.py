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
        Consegna.resize(400, 300)
        self.label = QtWidgets.QLabel(Consegna)
        self.label.setGeometry(QtCore.QRect(50, 10, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Consegna)
        self.pushButton.setGeometry(QtCore.QRect(220, 60, 131, 32))
        self.pushButton.setObjectName("pushButton")
        self.btn_ok = QtWidgets.QPushButton(Consegna)
        self.btn_ok.setGeometry(QtCore.QRect(120, 250, 113, 32))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_cancel = QtWidgets.QPushButton(Consegna)
        self.btn_cancel.setGeometry(QtCore.QRect(250, 250, 113, 32))
        self.btn_cancel.setObjectName("btn_cancel")

        self.retranslateUi(Consegna)
        self.pushButton.clicked.connect(Consegna.modificato)
        self.btn_ok.clicked.connect(Consegna.accetta)
        self.btn_cancel.clicked.connect(Consegna.annulla)
        QtCore.QMetaObject.connectSlotsByName(Consegna)

    def retranslateUi(self, Consegna):
        _translate = QtCore.QCoreApplication.translate
        Consegna.setWindowTitle(_translate("Consegna", "Form"))
        self.label.setText(_translate("Consegna", "Consegna is working"))
        self.pushButton.setText(_translate("Consegna", "Simula Modifica"))
        self.btn_ok.setText(_translate("Consegna", "Accetta"))
        self.btn_cancel.setText(_translate("Consegna", "Annulla"))
