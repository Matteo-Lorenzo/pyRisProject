import sys
from PyQt5.QtWidgets import QApplication
import orm_setup
import qdarkstyle

from app.ges_mainwindow.mainwindow_model import MainWindowModel
from app.ges_mainwindow.mainwindow_controller import MainWindowController
from app.ges_mainwindow.mainwindow_view import MainWindowView

from qt_material import apply_stylesheet

class App(QApplication):

    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.mainwindow_model = MainWindowModel()
        self.mainwindow_controller = MainWindowController(self.mainwindow_model)
        self.mainwindow_view = MainWindowView(self.mainwindow_model, self.mainwindow_controller)
        self.mainwindow_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec_())
