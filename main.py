import pickle
import sys
from PyQt5.QtWidgets import QApplication
import platform
import orm_setup
import qdarkstyle

from app.ges_mainwindow.mainwindow_model import MainWindowModel
from app.ges_mainwindow.mainwindow_controller import MainWindowController
from app.ges_mainwindow.mainwindow_view import MainWindowView
from app.utils import Ambiente

from qt_material import apply_stylesheet

class App(QApplication):

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.mainwindow_model = MainWindowModel()
        self.mainwindow_controller = MainWindowController(self.mainwindow_model)
        self.mainwindow_view = MainWindowView(self.mainwindow_model, self.mainwindow_controller)
        self.mainwindow_view.show()


if __name__ == '__main__':
    Ambiente.app = App(sys.argv)
    Ambiente.piattaforma = platform.system()
    print(Ambiente.piattaforma)
    try:
        with open('..config.pickle', 'rb') as f:
            Ambiente.visualizzazione = pickle.load(f)
        Ambiente.app.setStyle(Ambiente.visualizzazione['stile'])
        if Ambiente.visualizzazione['tema'] == 'scuro':
            Ambiente.app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            Ambiente.app.setStyleSheet('')
    except:
        print('File di configurazioni non trovato, uso la configurazione di default')
        Ambiente.app.setStyle(Ambiente.visualizzazione['stile'])
        if Ambiente.visualizzazione['tema'] == 'scuro':
            Ambiente.app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            Ambiente.app.setStyleSheet('')

    # apply_stylesheet(Ambiente.app, theme='light_blue.xml', invert_secondary=True)
    sys.exit(Ambiente.app.exec_())
