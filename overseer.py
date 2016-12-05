import sys
import subprocess
import signal
import time # Timers
import os
import types # For changing methods of an instance of a class # Needed for right click menu
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UImainwindow import Ui_MainWindow # This is our code that is working off the generated code from pyuic5
from proc import Proc # our proc.py class

# FIXME: Delete below once hooked onto Qt's update/refresh method
# A demonstration that the data isn't linked with Qt properly
proc = Proc()
# time.sleep(1)
# proc.readData()

def test():
    print("works")



# Uneeded, but for reference
# # We need a separate thread for polling, else we need non-blocking IO reads
# class ProcThread(QtCore.QThread):
#     def __init__(self):
#         super(ProcThread, self).__init__()

class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        # super(OverseerMainWindow, self).__init__() # Apparently the arguments are not needed?
        # super().__init__() # 2nd apparently we didn't need to call the base class's __init__ at all

        # VARIABLES

        # Important variables, do not change the order
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow) # This needs to be called before we can reference self.tableView

        # FIXME: make this uncommented when the model is properly linked
        #self.proc = Proc()
        self.proc = proc
        self.processListModel = QtGui.QStandardItemModel(1, 6)
        self.timer = QtCore.QTimer()
        self.setupStartupFile() # See if Overseer starts on startup

        # It was too much of a hassle to create a custom class and working off generated code, so we're using this hackish fix for a small change
        self.tableView.contextMenuEvent = types.MethodType(self._hProcessListContextMenuEvent, self.tableView) # Add a right click menu

        self.configProcessList()
        self.readProcessList()

        # For reference
        # QKeySequence(QKeySequence.Print);
        # QKeySequence(tr("Ctrl+P"));
        # QKeySequence(tr("Ctrl+p"));
        # QKeySequence(Qt.CTRL + Qt.Key_P);
        # QtCore.QObject.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.Dialog), QtCore.SIGNAL('activated()'), self.Dialog.close)
        # QtWidgets.QShortcut(QtGui.QKeySequence("q"), self.MainWindow, test)

        # This timer will act as timer for polling and for updating the GUI
        self.timer.timeout.connect(self.updateView)
        # Every second
        # self.timer.start(1000) # FIXME: Uncomment when done with right click menu

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
        self.tableView.setSortingEnabled(False) # This is a hack fix for getting sorting to stay when deleting all items and re-adding them
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
        self.tableView.setSortingEnabled(True) # This is a hack fix for getting sorting to stay when deleting all items and re-adding them

    # Check if this is our first startup, if so, make the program start on startup
    # This is aimed for only the Ubuntu system
    # FIXME: Add exception handling to this just to be safe
    def setupStartupFile(self):
        directory = "~/.config/autostart"
        directory = os.path.expanduser(directory)
        startupFileString = "~/.config/autostart/overseer.desktop"
        startupFileString = os.path.expanduser(startupFileString)
        startupFile = Path(startupFileString)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not startupFile.is_file():
            fd = open(startupFileString, 'w')
            fd.write('[Desktop Entry]\n')
            fd.write('Type=Application\n')
            fd.write('Name=Overseer\n')
            overseerLocation = os.path.realpath(__file__)
            fd.write('Exec=python3 "' + overseerLocation + '"\n')
            fd.write('Icon=""\n')
            fd.write('Comment=""\n')
            fd.write('X-GNOME-Autostart-enabled=true\n')
            fd.close()

    # This should be a hidden function. Made it a member function so it could access proc
    def _hProcessListContextMenuEvent(self, tableView, event):
        # Define the menu
        tableView.menu = QtWidgets.QMenu(tableView)
        openFileLocationAction = QtWidgets.QAction("Open File Location", tableView)
        # openFileLocationAction.triggered.connect(test) # another way to add functions onto actions
        tableView.menu.addAction(openFileLocationAction)
        tableView.menu.addSeparator()
        endProcessAction = QtWidgets.QAction("End Process", tableView)
        tableView.menu.addAction(endProcessAction)
        endProcessTreeAction = QtWidgets.QAction("End Process Tree", tableView)
        tableView.menu.addAction(endProcessTreeAction)

        # Summon the context menu
        action = tableView.menu.exec_(tableView.mapToGlobal(event.pos()))
        # tableView.menu.popup(QtGui.QCursor.pos()) # Another way of bringing up the menu
        selection = tableView.selectionModel().selection().indexes()[0] # selection() seems to be our best bet on seeing what we right clicked on, could possibly be buggy
        pid = tableView.model().data(tableView.model().index(selection.row(), 1)) # Get our PID
        if action == openFileLocationAction:
            if sys.platform == "linux":
                subprocess.check_call(['xdg-open', self.proc.processList[pid].path])
            else:
                QtWidgets.QMessageBox.about(None, "Warning", "Your system is not running Linux, unable to open a file explorer.")

# def handler(signum, frame):
#     print("got signal")
#     proc.processList[0].utime = 1337

if __name__ == "__main__":
    ui = OverseerMainWindow()
    # signal.signal(signal.SIGALRM, handler)
    # signal.setitimer(signal.ITIMER_REAL, 5)
    ui.show()
    sys.exit(ui.app.exec_())
