import sys
import subprocess
import signal
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UImainwindow import Ui_MainWindow
from proc import Proc # our proc.py class

# This is our code that is working off the generated code from pyuic5

# FIXME: Delete below once hooked onto Qt's update/refresh method
# A demonstration that the data isn't linked with Qt properly
proc = Proc()
time.sleep(1)
proc.readData()

class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        super(OverseerMainWindow, self).__init__()

        # FIXME: make this uncommented when the model is properly linked
        #self.proc = Proc()
        self.proc = proc

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

        # for i, process in enumerate(proc.processList): # OLD
        for i,(key,value) in enumerate(self.proc.processList.items()):
            item = QtGui.QStandardItem(value.name)
            self.model.setItem(i,0, item)
            item = QtGui.QStandardItem(value.pid)
            self.model.setItem(i,1, item)
            # FIXME: Make this show the proper user name
            item = QtGui.QStandardItem("user")
            self.model.setItem(i,2, item)
            item = QtGui.QStandardItem(value.ramPercentage)
            self.model.setItem(i,4, item)

            # FIXME: delete below
            item = QtGui.QStandardItem(str(value.cpuPercentage))
            self.model.setItem(i,3, item)

        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)

# def handler(signum, frame):
#     print("got signal")
#     proc.processList[0].utime = 1337

if __name__ == "__main__":
    ui = OverseerMainWindow()
    # signal.signal(signal.SIGALRM, handler)
    # signal.setitimer(signal.ITIMER_REAL, 5)
    ui.show()
    sys.exit(ui.app.exec_())
