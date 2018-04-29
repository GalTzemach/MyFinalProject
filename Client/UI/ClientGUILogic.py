from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from UI import clientGUI 

class ClientGUILogic(QMainWindow, clientGUI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  

        #event clicked
        self.addStocks_pushButton.clicked.connect(self.addStocks_pushButton_clicked)

    def addStocks_pushButton_clicked(self):
        print("addStocks_pushButton id clicked")


def start():
    app = QApplication(sys.argv) # A new instance of QApplication
    form = ClientGUILogic()                 
    form.show()                         
    app.exec_()                         





