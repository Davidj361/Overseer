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
# time.sleep(1)
# proc.readData()


# We need a separate thread for polling, else we need non-blocking IO reads
class ProcThread(QtCore.QThread):
    def __init__(self):
        super(ProcThread, self).__init__()

class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        super(OverseerMainWindow, self).__init__()

        # VARIABLES
        # FIXME: make this uncommented when the model is properly linked
        #self.proc = Proc()
        self.proc = proc
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.processListModel = QtGui.QStandardItemModel(1, 6)
        self.timer = QtCore.QTimer()

        self.setupUi(self.MainWindow)
        self.configProcessList()

        # This timer will act as timer for polling and for updating the GUI
        self.timer.timeout.connect(self.updateView)
        # Every second
        self.timer.start(1000)

    def show(self):
        self.MainWindow.show()

    def updateView(self):
        self.readProcessList()

    def configProcessList(self):
        # Set the labels for the columns
        self.processListModel.setHeaderData(0, 1, "Image Name")
        self.processListModel.setHeaderData(1, 1, "PID")
        self.processListModel.setHeaderData(2, 1, "User Name")
        self.processListModel.setHeaderData(3, 1, "CPU")
        self.processListModel.setHeaderData(4, 1, "Memory")
        self.processListModel.setHeaderData(5, 1, "Description")
        self.tableView.setModel(self.processListModel)
        self.tableView.verticalHeader().setVisible(False)

    def readProcessList(self):
        # Erase all of the items in the model and re-add them
        self.processListModel.removeRows(0, self.processListModel.rowCount())
        # for i, process in enumerate(proc.processList): # OLD
        for i,(key,value) in enumerate(self.proc.processList.items()):
            item = QtGui.QStandardItem(value.name)
            self.processListModel.setItem(i,0, item)
            item = QtGui.QStandardItem(value.pid)
            self.processListModel.setItem(i,1, item)
            # FIXME: Make this show the proper user name
            item = QtGui.QStandardItem("user")
            self.processListModel.setItem(i,2, item)
            item = QtGui.QStandardItem(value.ramPercentage)
            self.processListModel.setItem(i,4, item)

            # FIXME: delete below
            item = QtGui.QStandardItem(str(value.cpuPercentage))
            self.processListModel.setItem(i,3, item)

# def handler(signum, frame):
#     print("got signal")
#     proc.processList[0].utime = 1337

if __name__ == "__main__":
    ui = OverseerMainWindow()
    # signal.signal(signal.SIGALRM, handler)
    # signal.setitimer(signal.ITIMER_REAL, 5)
    ui.show()
    sys.exit(ui.app.exec_())
