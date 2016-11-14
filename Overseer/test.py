import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UImainwindow import Ui_MainWindow

# This is our code that is working off the generated code from pyuic5
class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        super(OverseerMainWindow, self).__init__()
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow)
        self.setupProcessesList()

    def show():
        self.MainWindow.show()

    # Add local changes below
    def setupProcessesList(self):
        # I have no idea how to get update the model
        # Even if columnview is not the right class, we need to figure this out
        self.columnView.setModel(self, QtCore.QAbstractItemModel(["test1","test2"]))




if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(app.exec_())
