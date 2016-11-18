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
        # I have no idea how to get update the model
        # Even if columnview is not the right class, we need to figure this out
        self.tableView.setModel(TableModel(self,["test1","test2"]))
        self.tableView


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__()
        self.datatable = None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.index)
        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.columns.values)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        #some from QtDocumentation, but some from website, to get it working.
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return "{0}".format(self.datatable.iget_value(i,j))
        else:
            return QtCore.QVariant()

    def update(self, inputData):
        self.datatable = inputData

"""
    #from qt docs well behaved models include
    def headerData():
        pass

    #from qt docs, resizable can implement
    def insertRows():
        #from qt docs, will need to call beginInsertRows() and endInsertRows()
        pass

    def insertColumn():
        #from qt docs, will need to call beginInsertColumns() and endInsertColumns()
        pass

    def removeRows():
        #from qt docs, will need to call beginRemoveRows() and endRemoveRows()
        pass

    def removeColumns():
        #from qt docs, will need to call beginRemoveColumns() and endRemoveColums()
        pass
"""
    


if __name__ == "__main__":
    ui = OverseerMainWindow()
    ui.show()
    sys.exit(ui.app.exec_())
