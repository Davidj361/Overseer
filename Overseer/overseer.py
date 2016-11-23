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

        # OLD - for reference
        # p = subprocess.Popen(["ls", "/proc"], stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        # (output, err) = p.communicate()
        # arr = output.split('\n')
        # outArr = [];
        # for element in arr:
        #     if(element.isdigit()):
        #         cmdString = "/proc/" + element + "/status"
        #         p2 = subprocess.Popen(["cat", cmdString], stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        #         (output2, err) = p2.communicate()
        #         arr2 = output2.split('\n')
        #         for element2 in arr2:
        #             if((element2) and (element2[0] == 'N') and (element2[1] == 'a')):
        #                 element = element.strip(" ")
        #                 element2 = element2.strip("Name:")
        #                 element2 = element2.strip(" ")
        #                 element2 = element2.strip('\t')
        #                 outArr.append([element, element2])

        i = 0
        for element in self.proc.data:
            item = QtGui.QStandardItem(element[0])
            self.model.setItem(i,0, item)
            item = QtGui.QStandardItem(element[1])
            self.model.setItem(i,1, item)
            i += 1
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setVisible(False)

if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
