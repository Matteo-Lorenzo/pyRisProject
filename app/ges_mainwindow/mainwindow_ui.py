# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar_pyris = QtWidgets.QMenuBar(MainWindow)
        self.menubar_pyris.setGeometry(QtCore.QRect(0, 0, 1200, 24))
        self.menubar_pyris.setNativeMenuBar(False)
        self.menubar_pyris.setObjectName("menubar_pyris")
        self.menuWorklist = QtWidgets.QMenu(self.menubar_pyris)
        self.menuWorklist.setObjectName("menuWorklist")
        self.menuFile = QtWidgets.QMenu(self.menubar_pyris)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar_pyris)
        self.actionEsecuzione_esame = QtWidgets.QAction(MainWindow)
        self.actionEsecuzione_esame.setObjectName("actionEsecuzione_esame")
        self.actionRefertazione = QtWidgets.QAction(MainWindow)
        self.actionRefertazione.setObjectName("actionRefertazione")
        self.actionFirma = QtWidgets.QAction(MainWindow)
        self.actionFirma.setObjectName("actionFirma")
        self.actionControllo = QtWidgets.QAction(MainWindow)
        self.actionControllo.setObjectName("actionControllo")
        self.actionGestione_pazienti = QtWidgets.QAction(MainWindow)
        self.actionGestione_pazienti.setObjectName("actionGestione_pazienti")
        self.actionPrenotazioni = QtWidgets.QAction(MainWindow)
        self.actionPrenotazioni.setObjectName("actionPrenotazioni")
        self.actionPreferenze = QtWidgets.QAction(MainWindow)
        self.actionPreferenze.setObjectName("actionPreferenze")
        self.actionConsegna = QtWidgets.QAction(MainWindow)
        self.actionConsegna.setObjectName("actionConsegna")
        self.menuWorklist.addAction(self.actionEsecuzione_esame)
        self.menuWorklist.addAction(self.actionRefertazione)
        self.menuWorklist.addAction(self.actionFirma)
        self.menuWorklist.addSeparator()
        self.menuWorklist.addAction(self.actionControllo)
        self.menuFile.addAction(self.actionGestione_pazienti)
        self.menuFile.addAction(self.actionPrenotazioni)
        self.menuFile.addAction(self.actionConsegna)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreferenze)
        self.menubar_pyris.addAction(self.menuFile.menuAction())
        self.menubar_pyris.addAction(self.menuWorklist.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuWorklist.setTitle(_translate("MainWindow", "Worklist"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionEsecuzione_esame.setText(_translate("MainWindow", "Esecuzione esame"))
        self.actionRefertazione.setText(_translate("MainWindow", "Refertazione"))
        self.actionFirma.setText(_translate("MainWindow", "Firma"))
        self.actionControllo.setText(_translate("MainWindow", "Controllo"))
        self.actionGestione_pazienti.setText(_translate("MainWindow", "Gestione pazienti"))
        self.actionPrenotazioni.setText(_translate("MainWindow", "Prenotazioni"))
        self.actionPreferenze.setText(_translate("MainWindow", "Preferenze"))
        self.actionConsegna.setText(_translate("MainWindow", "Consegna"))