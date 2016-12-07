import sys
import subprocess
import time # Timers
import os
import stat # For making the launch script executable for the shortcut
import types # For changing methods of an instance of a class # Needed for right click menu
import re # regex for setupgsettings
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UImainwindow import Ui_MainWindow # This is our code that is working off the generated code from pyuic5
from proc import Proc # our proc.py class

class OverseerMainWindow(Ui_MainWindow):
    def __init__(self):
        # Important variables, do not change the order
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi(self.MainWindow) # This needs to be called before we can reference self.tableView

        self.proc = Proc()
        self.processListModel = QtGui.QStandardItemModel(1, 6)
        self.timer = QtCore.QTimer()
        # See if this is our first startup. If so, we need to make a bash script to launch this program and add it to unity's shortcuts.
        self.setupShortcuts()

        # It was too much of a hassle to create a custom class and working off generated code, so we're using this hackish fix for a small change
        self.tableView.contextMenuEvent = types.MethodType(self._hProcessListContextMenuEvent, self.tableView) # Add a right click menu

        self.configProcessList()
        self.readProcessList()

        # This timer will act as timer for polling and for updating the GUI
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.updateView)
        # Every second
        self.timer.start(1000)

    def show(self):
        self.MainWindow.show()

    # Update the data and view
    def update(self):
        self.proc.readData()
        self.readProcessList()

    # Update the view depending on what tab we are
    def updateView(self):
        self.readProcessList()

    def configProcessList(self):
        # Set the labels for the columns
        self.processListModel.setHeaderData(0, 1, "Image Name")
        self.processListModel.setHeaderData(1, 1, "PID")
        self.processListModel.setHeaderData(2, 1, "User Name")
        self.processListModel.setHeaderData(3, 1, "CPU (%)")
        self.processListModel.setHeaderData(4, 1, "Memory (%)")
        self.processListModel.setHeaderData(5, 1, "Description")
        self.tableView.setModel(self.processListModel)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setHighlightSections(False)

    def readProcessList(self):
        pid = self.getSelectedProcessPID(self.tableView)
        # Erase all of the items in the model and re-add them
        self.processListModel.removeRows(0, self.processListModel.rowCount())
        self.tableView.setSortingEnabled(False) # This is a hack fix for getting sorting to stay when deleting all items and re-adding them
        for i,(key,value) in enumerate(self.proc.processList.items()):
            item = QtGui.QStandardItem(value.name)
            self.processListModel.setItem(i,0, item)
            item = QtGui.QStandardItem(value.pid)
            self.processListModel.setItem(i,1, item)
            # FIXME: Make this show the proper user name
            item = QtGui.QStandardItem("user")
            self.processListModel.setItem(i,2, item)
            item = QtGui.QStandardItem(str(value.cpuPercentage))
            self.processListModel.setItem(i,3, item)
            item = QtGui.QStandardItem(value.ramPercentage)
            self.processListModel.setItem(i,4, item)
        self.tableView.setSortingEnabled(True) # This is a hack fix for getting sorting to stay when deleting all items and re-adding them
        # Another hack fix for keeping selection
        # It adds more strain to the thread
        if pid != -1:
            for index in range(1, self.tableView.model().rowCount() + 1):
                self.tableView.selectRow(index)
                if self.tableView.selectionModel().selection().indexes()[1].data() == pid:
                    # If the previously selected item is found, leave
                    return
            # If we are still here, the old item wasn't found, so deselect all
            self.tableView.clearSelection()

    # Returns -1 if no selection or PID couldn't be found, or returns PID
    def getSelectedProcessPID(self, tableView):
        pid = -1
        indexes = tableView.selectionModel().selection().indexes()
        if len(indexes) != 0:
            selection = tableView.selectionModel().selection().indexes()[0] # selection() seems to be our best bet on seeing what we right clicked on, could possibly be buggy
            pid = tableView.model().data(tableView.model().index(selection.row(), 1)) # Get our PID
        return pid

    # Check if this is our first startup, if so, make the program start on startup
    # This is aimed for only the Ubuntu system
    def setupShortcuts(self):
        ret = self.setupLaunchScript()
        if ret == False:
            return
        self.setupgsettings(ret)


    # FIXME: Add exception handling to this just to be safe
    def setupLaunchScript(self):
        directory = "~"
        directory = os.path.expanduser(directory)
        launchScriptString = "~/openOverseer.sh"
        launchScriptString = os.path.expanduser(launchScriptString)
        launchScript = Path(launchScriptString)
        if not os.path.exists(directory):
            print("You do not have a home directory")
            return False
            # os.makedirs(directory) # Highly doubt we would need to make the $HOME directory
        if not launchScript.is_file():
            fd = open(launchScriptString, 'w')
            fd.write('#!/bin/bash\n')
            overseerLocation = os.path.realpath(__file__)
            fd.write("python3 '" + overseerLocation + "'\n")
            fd.close()
            st = os.stat(launchScriptString)
            os.chmod(launchScriptString, st.st_mode | stat.S_IEXEC) # Make the bash script executable
        return launchScriptString

    def setupgsettings(self, launchScriptString): # Setup unity's custom shortcut to launch our launch script
        if launchScriptString is None:
            print("launchScriptString is None")
            return
        ret = subprocess.run(['gsettings', 'get', 'org.gnome.settings-daemon.plugins.media-keys', 'custom-keybindings'],stdout=subprocess.PIPE,universal_newlines=True)
        # An example of red.stdout: ['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/']

        # Go through ret and see if any of the custom shortcuts already have an Overseer shortcut
        # Code generated by regex101.com
        regex = r"'([^']+)'"
        matches = re.finditer(regex, ret.stdout)
        found = False
        matchNum = 0
        for match in matches:
            matchNum = matchNum + 1
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                groupMatch = match.group(groupNum)
                # print(groupMatch)
                # Command for asking name of the shortcut:
                # gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name
                ret2 = subprocess.run(['gsettings', 'get', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:' + groupMatch, 'name'],stdout=subprocess.PIPE,universal_newlines=True)
                shortcutName = re.sub("['\n]","",ret2.stdout) # Take out ' and new line characters
                if shortcutName == "Overseer":
                    found = True
        if not found:
            # Make a new list for custom-keybindings
            if not (ret.stdout == "@as []\n"):
                newList = re.sub("]\n$",", '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom" + str(matchNum) + "/']",ret.stdout)
                newList = re.sub("]$",", '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom" + str(matchNum+1) + "/']",newList)
            else:
                newList = "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
                newList = re.sub("]$",", '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/']",newList)
            # How it should look
            # gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "[<altered_list>]"
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys', 'custom-keybindings', newList],stdout=subprocess.PIPE,universal_newlines=True)
            # Remove ctrl+shift+del as a shortcut to log out
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys', 'logout', ''],stdout=subprocess.PIPE,universal_newlines=True)

            # Example for setting
            # gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ name '<newname>'
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum) + '/', 'name', 'Overseer'],stdout=subprocess.PIPE,universal_newlines=True)
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum) + '/', 'command', launchScriptString],stdout=subprocess.PIPE,universal_newlines=True)
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum) + '/', 'binding', '<Primary><Shift>Escape'],stdout=subprocess.PIPE,universal_newlines=True)

            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum+1) + '/', 'name', 'Overseer'],stdout=subprocess.PIPE,universal_newlines=True)
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum+1) + '/', 'command', launchScriptString],stdout=subprocess.PIPE,universal_newlines=True)
            ret2 = subprocess.run(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom' + str(matchNum+1) + '/', 'binding', '<Primary><Alt>Delete'],stdout=subprocess.PIPE,universal_newlines=True)

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
        pid = self.getSelectedProcessPID(tableView)
        if pid == -1:
            return
        if action == openFileLocationAction:
            if sys.platform == "linux":
                # We need to pass in /dev/null to stdout and stderr so we don't get spam in our main program's stdout and stderr
                if self.proc.processList[pid].path == "DENIED":
                    QtWidgets.QMessageBox.about(self.MainWindow, "Warning", "You have no permissions to access this file location.")
                else:
                    subprocess.run(['xdg-open', self.proc.processList[pid].path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                QtWidgets.QMessageBox.about(self.MainWindow, "Warning", "Your system is not running Linux, unable to open a file explorer.")
        elif action == endProcessAction:
            ret = self.proc.processList[pid].endProcess()
            if ret == 1:
                QtWidgets.QMessageBox.about(self.MainWindow, "Warning", "You do not have permission to end this process.")
        elif action == endProcessTreeAction:
            ret = self.proc.processList[pid].endProcessTree()
            if ret == 1:
                QtWidgets.QMessageBox.about(self.MainWindow, "Warning", "You do not have permission to end this process.")

if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
