from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox
import sys
from UI import clientGUI 
from ClientServerNetwork import clientNetwork

class ClientGUILogic(QMainWindow, clientGUI.Ui_MainWindow):

    ID = None
    selectedSymbolFromAllStocks = None
    selectedSymbolFromMyStocks = None


    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  

        # All Events

        # Add stocks btn clicked
        self.addStocks_pushButton.clicked.connect(self.addStocks_pushButton_clicked)

        # Item selection changed in all stocks table
        self.allStocks_tableWidget.itemSelectionChanged.connect(self.allStocks_itemSelectionChangedEvent)

        # Item selection changed in my stocks table
        self.myStocks_tableWidget.itemSelectionChanged.connect(self.myStocks_itemSelectionChangedEvent)

        # Delete stock btn
        self.deleteStocks_pushButton.clicked.connect(self.deleteStocks_pushButton_clicked)

        # ComboBox
        self.addStocks_comboBox.currentIndexChanged.connect(self.addStocks_comboBox_changed)

    def addStocks_comboBox_changed(self):
        numItem = self.addStocks_comboBox.count()
        if numItem == 0:
            self.addStocks_pushButton.setEnabled(False)
        else:
            self.addStocks_pushButton.setEnabled(True)



    def getAllStocks(self):
        allStocks = clientNetwork.clientNetwork().getAllStocks()
        if isinstance(allStocks, bool) and allStocks == False:
            print("Could not retrieve all stocks, Try again.")
            return False
        return allStocks


    def addStocks_pushButton_clicked(self):
        self.addStockToUser()

    def addStockToUser(self):
        comboText = self.addStocks_comboBox.currentText()
        symbol = comboText.split(",")[1].lstrip()

        stockID = clientNetwork.clientNetwork().getStockIDBySymbol(symbol)
        if stockID:
            if clientNetwork.clientNetwork().addStockToUser(self.ID, stockID[0][0]):
                self.fillMyStocks()
                self.fillAddStocksComboBox()
            else:
                pass
        else:
            pass
        



    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        clientNetwork.clientNetwork().exit()


    def allStocks_itemSelectionChangedEvent(self):
        # Get symbol that selected
        self.selectedSymbolFromAllStocks = self.allStocks_tableWidget.selectedItems()[1].text()
        print(self.selectedSymbolFromAllStocks)

        # Set visible true
        self.stockInfo_tabWidget.setVisible(True)

        # Fill tabWidgets
        self.fillStockInfo(self.selectedSymbolFromAllStocks)


    def fillStockInfo(self, symbol):
        # Fill info tab
        explanation = clientNetwork.clientNetwork().getExplanationBysymbol(symbol)
        if explanation:
            self.textBrowser.setText(explanation[0][0])
        else:
            self.textBrowser.setText("")


        # Fill tweets tab
        stockID = clientNetwork.clientNetwork().getStockIDBySymbol(symbol)
        if stockID:
            allTweets = clientNetwork.clientNetwork().getAllTweetsByStockID(stockID[0][0])
            if allTweets:
                self.fillTable(self.tweets_tableWidget, allTweets)
            else:
                self.tweets_tableWidget.setRowCount(0)
        else:
            self.tweets_tableWidget.setRowCount(0)


        # Fill regression tab


    def focusInEvent(self, QFocusEvent):
        super().focusInEvent(QFocusEvent)

        print ("in")




    def showEvent(self, QShowEvent):
        super().showEvent(QShowEvent)

        # Until stocks select
        self.stockInfo_tabWidget.setVisible(False)

        self.prepareGUI()

        self.addStocks_comboBox_changed()


    def prepareGUI(self):
        # Full name
        fullName = clientNetwork.clientNetwork().getFullNameByID(self.ID)
        if fullName:
            firstName = fullName[0][0]
            lastName = fullName[0][1]
            self.helloUser_label.setText("Hello %s %s" % (firstName, lastName))

        # All Stocks
        allStocks = self.getAllStocks()
        if allStocks:
            self.fillTable(self.allStocks_tableWidget, allStocks)

        # My stocks table
        self.fillMyStocks()

        # Add stocks ComboBox
        self.fillAddStocksComboBox()


    def fillAddStocksComboBox(self):
        allStocksIDs = clientNetwork.clientNetwork().getAllStocksIDs()
        if allStocksIDs:
            allStocksIDs = list(allStocksIDs)
            myStocksIDs = clientNetwork.clientNetwork().getMyStocksIDs(self.ID)
            StocksList = []

            if myStocksIDs or isinstance(myStocksIDs, tuple):
                # Remove exists
                for myStockID in myStocksIDs:
                    for i, stockID in enumerate(allStocksIDs):
                        if myStockID[0] == stockID[0]:
                            del allStocksIDs[i]
                            break

            stocksListForComboBox = []
            for stockID in allStocksIDs:
                stock = clientNetwork.clientNetwork().getStockByID(stockID[0])[0]
                stocksListForComboBox.append(str(stock[0]) + ", \t" + str(stock[1]))
            # Fill combo
            self.addStocks_comboBox.clear()
            self.addStocks_comboBox.addItems(stocksListForComboBox)

        else:
            pass


    def fillMyStocks(self):
        myStocks = self.getMyStocks(self.ID)
        if myStocks:
            self.fillTable(self.myStocks_tableWidget, myStocks)
        else:
            self.myStocks_tableWidget.setRowCount(0)


    def getMyStocks(self, ID):
        myStocksIDs = clientNetwork.clientNetwork().getMyStocksIDs(ID)
        if myStocksIDs:
            myStocksList = []
            for stockID in myStocksIDs:
                stockID = stockID[0]
                myStocksList.append(clientNetwork.clientNetwork().getStockByID(stockID)[0])
            return tuple(myStocksList)
        else:
            print("Could not retrieve myStocksIDs, or is empty.")
        

    def myStocks_itemSelectionChangedEvent(self):
        self.deleteStocks_pushButton.setEnabled(True)
        if self.myStocks_tableWidget.selectedItems():
            self.selectedSymbolFromMyStocks = self.myStocks_tableWidget.selectedItems()[1].text()
        else:
            self.deleteStocks_pushButton.setEnabled(False)
       

    def deleteStocks_pushButton_clicked(self):
        self.deleteStockBySymbol()

    def deleteStockBySymbol(self):
        ID = clientNetwork.clientNetwork().getStockIDBySymbol(self.selectedSymbolFromMyStocks)
        if ID:
            isDelete = clientNetwork.clientNetwork().deleteStockByIDs(self.ID, ID[0][0])
            if isDelete:
                self.fillMyStocks()
                self.fillAddStocksComboBox()
            else:
                print("Can not delete stock.")
        else:
            print("Can not delete stock.")



    def fillTable(self, table, data):
        table.setRowCount(0)
        for rowNumber, rowData in enumerate(data):
            table.insertRow(rowNumber)
            for colNumber, colData in enumerate(rowData):
                table.setItem(rowNumber, colNumber, QTableWidgetItem(str(colData)))





def start(ID):
    app = QApplication(sys.argv) # A new instance of QApplication
    form = ClientGUILogic()   
    form.ID = ID
    form.show()   
    app.exec_()                    





