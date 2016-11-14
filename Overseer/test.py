import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from UImainwindow import Ui_MainWindow

class testGui(Ui_MainWindow):
	def __init__(self, dialog):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
 
        # Reference from tutorial
	# def addInputTextToListbox(self):
	# 	txt = self.myTextInput.text()
	# 	self.listWidget.addItem(txt)
    

if __name__ == "__main__":
    import sys
    import time
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    item = QtWidgets.QListWidgetItem("This is a test.")
    ui.listWidget.addItem(item)
    item = QtWidgets.QListWidgetItem("This is a 2nd test.")
    ui.listWidget.addItem(item)
    item = QtWidgets.QListWidgetItem("This is a 3rd test.")
    ui.listWidget.addItem(item)
    sys.exit(app.exec_())
