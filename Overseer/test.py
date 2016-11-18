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

    def show(self):
        self.MainWindow.show()

    # Add local changes below
    def setupProcessesList(self):
        item = QtGui.QStandardItem("test")
        model = QtGui.QStandardItemModel(9, 7)
        model.setItem(2,3, item)
        self.tableView.setModel(model)
        self.tableView.verticalHeader().setVisible(False)

if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
