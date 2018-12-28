import sys
from os import getcwd

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot


class Window(QtWidgets.QMainWindow):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 600)
        self.show()


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    w = Window("Window1")
    w2 = Window("Window 2")
    sys.exit(app.exec())