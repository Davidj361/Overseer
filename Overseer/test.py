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
        self.model = QtGui.QStandardItemModel(1, 6)
        # Set the labels for the columns
        self.model.setHeaderData(0, 1, "Image Name")
        self.model.setHeaderData(1, 1, "PID")
        self.model.setHeaderData(2, 1, "User Name")
        self.model.setHeaderData(3, 1, "CPU")
        self.model.setHeaderData(4, 1, "Memory")
        self.model.setHeaderData(5, 1, "Description")
        self.model.setItem(2, 3, item)
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)

if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
