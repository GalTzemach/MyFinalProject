import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn ##
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from UI import clientGUI 
from ClientServerNetwork import clientNetwork


class ClientGUILogic(QMainWindow, clientGUI.Ui_MainWindow):

    userID = None
    selectedSymbolFromAllStocks = None
    selectedSymbolFromMyStocks = None


    def __init__(self):
        super(self.__class__, self).__init__()

        # Setup UI of pyqt
        self.setupUi(self)  

        #Events
        self.addStocks_pushButton.clicked.connect(self.addStocks_pushButton_clicked)
        self.deleteStocks_pushButton.clicked.connect(self.deleteStocks_pushButton_clicked)
        self.allStocks_tableWidget.itemSelectionChanged.connect(self.allStocks_itemSelectionChangedEvent)
        self.myStocks_tableWidget.itemSelectionChanged.connect(self.myStocks_itemSelectionChangedEvent)
        self.addStocks_comboBox.currentIndexChanged.connect(self.addStocks_comboBox_changed)
        self.showGraph_pushButton.clicked.connect(self.openGraphWindow)


    def addStocks_comboBox_changed(self):
        # Get number item
        numItem = self.addStocks_comboBox.count()

        if numItem == 0:
            self.addStocks_pushButton.setEnabled(False)
        else:
            self.addStocks_pushButton.setEnabled(True)


    def getAllStocks(self):
        allStocks = clientNetwork.clientNetwork().getAllStocks()

        if isinstance(allStocks, bool) and allStocks == False:
            print("Could not retrieve all stocks.")
            return False

        return allStocks


    def addStocks_pushButton_clicked(self):
        self.addStockToUser()


    def addStockToUser(self):
        # Get symbol from combobox
        comboText = self.addStocks_comboBox.currentText()
        symbol = comboText.split(",")[1].lstrip()

        stockID = clientNetwork.clientNetwork().getStockIDBySymbol(symbol)

        if stockID:
            if clientNetwork.clientNetwork().addStockToUser(self.userID, stockID[0][0]):
                # Update GUI
                self.fillMyStocks()
                self.fillAddStocksComboBox()


    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        clientNetwork.clientNetwork().exit()


    def allStocks_itemSelectionChangedEvent(self):
        # Get symbol
        symbol = self.allStocks_tableWidget.selectedItems()[1].text()
        self.selectedSymbolFromAllStocks = symbol

        # Set stockInfo_tabWidget visible
        self.stockInfo_tabWidget.setVisible(True)

        # Fill stock info
        self.fillStockInfo()


    def fillStockInfo(self):
        # Fill info tab
        explanation = clientNetwork.clientNetwork().getExplanationBysymbol(self.selectedSymbolFromAllStocks)
        if explanation:
            self.explanation_textBrowser.setText(explanation[0][0])
        else:
            self.explanation_textBrowser.setText("")

        # Fill tweets tab
        stockID = clientNetwork.clientNetwork().getStockIDBySymbol(self.selectedSymbolFromAllStocks)
        if stockID:
            allTweets = clientNetwork.clientNetwork().getAllTweetsByStockID(stockID[0][0])
            if allTweets:
                self.fillTable(self.tweets_tableWidget, allTweets)
            else:
                self.tweets_tableWidget.setRowCount(0)
        else:
            self.tweets_tableWidget.setRowCount(0)

        # Fill regression tab
        # The btn is open new window


    def openGraphWindow(self):
        # Close if open
        plt.close()

        # Get x and y (The samples)
        xy = clientNetwork.clientNetwork().getXYForGraphByID(self.selectedSymbolFromAllStocks)
        X = np.array(xy[1])
        y = np.array(xy[0])

        if len(X) == 0 or len(y) == 0:
            return

        # Linear Regression with OLS algorithm
        linearReg = linear_model.LinearRegression()
        linearReg.fit(X, y)
        lineYLinearRegression = linearReg.predict(X)
        linearR2 = linearReg.score(X,y)
        print("Linear R^2=", linearR2)

        # Robust linear regression with RANSAC algorithm
        ransac = linear_model.RANSACRegressor()
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        lineYRansac = ransac.predict(X)
        ransacR2 = ransac.score(X[inlier_mask], y[inlier_mask])
        print("RANSAC R^2=", ransacR2)

        # Polynomial regression with Ridge algorithm
        lw = 2
        for count, degree in enumerate([5,6]):
            model = make_pipeline(PolynomialFeatures(degree), linear_model.Ridge())
            model.fit(X, y)
            curveYPolynomial = model.predict(X)
            plt.plot(X, curveYPolynomial, label="Polynomial degree %d" % degree)
            print("Polynomial R^2= %f (degree:%d)" % (model.score(X, y), degree))

        # Draw plot
        # Inlier points
        plt.scatter(X[inlier_mask], y[inlier_mask], label='Inliers', color='black',  linewidth=4)
        # Outlier points
        plt.scatter(X[outlier_mask], y[outlier_mask], label='Outliers', color='black', linewidth=2)
        # Lines
        plt.plot(X, lineYLinearRegression, label='Linear regressor')
        plt.plot(X, lineYRansac, label='RANSAC regressor')
        # Title, Labels and legend
        plt.title("Linear, Robust and Polynomial Regression \nFor %s" % (self.selectedSymbolFromAllStocks))
        plt.xlabel("Sentiment")
        plt.ylabel("ChangClosePrice")
        plt.legend()##loc='lower right')

        plt.show()


    def showEvent(self, QShowEvent):
        super().showEvent(QShowEvent)

        # Stick info is unvisible until some stock is selected
        self.stockInfo_tabWidget.setVisible(False)

        # prepare GUI
        self.prepareGUI()

        # Call to addStocks_comboBox_changed event
        self.addStocks_comboBox_changed()


    def prepareGUI(self):
        # Full name
        fullName = clientNetwork.clientNetwork().getFullNameByID(self.userID)
        if fullName:
            firstName = fullName[0][0]
            lastName = fullName[0][1]
            self.helloUser_label.setText("Hello %s %s" % (firstName, lastName))

        # All stocks
        allStocks = self.getAllStocks()
        if allStocks:
            self.fillTable(self.allStocks_tableWidget, allStocks)

        # My stocks
        self.fillMyStocks()

        # Add stocks ComboBox
        self.fillAddStocksComboBox()

        # My messages
        self.fillMyMessages()


    def fillMyMessages(self):
        allMessages = clientNetwork.clientNetwork().getAllMessagesByUserID(self.userID)
        if allMessages:
            self.fillTable(self.myMessages_tableWidget, allMessages)
        else:
            self.myMessages_tableWidget.setRowCount(0)


    def fillAddStocksComboBox(self):
        allStocksIDs = clientNetwork.clientNetwork().getAllStocksIDs()
        if allStocksIDs:
            allStocksIDs = list(allStocksIDs)

            myStocksIDs = clientNetwork.clientNetwork().getMyStocksIDs(self.userID)

            StocksList = []
            if myStocksIDs or isinstance(myStocksIDs, tuple):##
                # Remove myStocks from allStocks
                for myStockID in myStocksIDs:
                    for i, allStockID in enumerate(allStocksIDs):
                        if myStockID[0] == allStockID[0]:
                            del allStocksIDs[i]
                            break

            stocksListForComboBox = []
            for allStockID in allStocksIDs:
                stock = clientNetwork.clientNetwork().getStockByID(allStockID[0])[0]
                stocksListForComboBox.append(str(stock[0]) + ", \t" + str(stock[1]))

            self.addStocks_comboBox.clear()
            self.addStocks_comboBox.addItems(stocksListForComboBox)
        else:
            self.addStocks_comboBox.clear()


    def fillMyStocks(self):
        myStocks = self.getMyStocks(self.userID)
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
        # Enable deleteStocks_pushButton
        self.deleteStocks_pushButton.setEnabled(True)

        if self.myStocks_tableWidget.selectedItems():
            # Save selectedSymbolFromMyStocks
            self.selectedSymbolFromMyStocks = self.myStocks_tableWidget.selectedItems()[1].text()
        else:
            # Disable deleteStocks_pushButton
            self.deleteStocks_pushButton.setEnabled(False)
       

    def deleteStocks_pushButton_clicked(self):
        stockID = clientNetwork.clientNetwork().getStockIDBySymbol(self.selectedSymbolFromMyStocks)
        if stockID:
            isDelete = clientNetwork.clientNetwork().deleteStockByIDs(self.userID, stockID[0][0])
            if isDelete:
                # Update GUI
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
    form.userID = ID
    form.show()   
    app.exec_()                    





