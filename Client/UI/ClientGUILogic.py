from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys
from UI import clientGUI 
from ClientServerNetwork import clientNetwork

class ClientGUILogic(QMainWindow, clientGUI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  

        # Event btn clicked
        self.addStocks_pushButton.clicked.connect(self.addStocks_pushButton_clicked)


    def keyPressEvent(self, QKeyEvent):
        super().keyPressEvent(QKeyEvent)
        print("keyPressEvent")

        results = self.getAllStocks()
        if results:
            self.allStocks_tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.allStocks_tableWidget.insertRow(row_number)
                for col_number, data in enumerate(row_data):
                    self.allStocks_tableWidget.setItem(row_number, col_number, QTableWidgetItem(str(data)))



    def getAllStocks(self):
        allStocks = clientNetwork.clientNetwork().getAllStocks()
        if isinstance(allStocks, bool) and allStocks == False:
            print("Could not retrieve all stocks, Try again.")
            return False
        return allStocks

    def addStocks_pushButton_clicked(self):
        print("addStocks_pushButton id clicked")


    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        clientNetwork.clientNetwork().exit()

def start():
    app = QApplication(sys.argv) # A new instance of QApplication
    form = ClientGUILogic()                 
    form.show()   
    app.exec_()                    





