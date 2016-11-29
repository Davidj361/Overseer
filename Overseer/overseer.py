import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UImainwindow import Ui_MainWindow
from proc import Proc # our proc.py class

# This is our code that is working off the generated code from pyuic5
class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        super(OverseerMainWindow, self).__init__()

        self.proc = Proc()

        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow)
        self.setupProcessesList()

    def show(self):
        self.MainWindow.show()

    # Add local changes below
    def setupProcessesList(self):
        self.model = QtGui.QStandardItemModel(1, 6)
        # Set the labels for the columns
        self.model.setHeaderData(0, 1, "Image Name")
        self.model.setHeaderData(1, 1, "PID")
        self.model.setHeaderData(2, 1, "User Name")
        self.model.setHeaderData(3, 1, "CPU")
        self.model.setHeaderData(4, 1, "Memory")
        self.model.setHeaderData(5, 1, "Description")
        self.tableView.setModel(self.model)

        for i, process in enumerate(self.proc.processList):
            item = QtGui.QStandardItem(process.name)
            self.model.setItem(i,0, item)
            item = QtGui.QStandardItem(process.pid)
            self.model.setItem(i,1, item)
            item = QtGui.QStandardItem("user")
            self.model.setItem(i,2, item)
            item = QtGui.QStandardItem(process.ramPrecentage)
            self.model.setItem(i,4, item)

            # FIXME: delete below
            item = QtGui.QStandardItem(process.utime)
            self.model.setItem(i,5, item)
            item = QtGui.QStandardItem(process.stime)
            self.model.setItem(i,6, item)

        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)

if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
