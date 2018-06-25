import datetime
import copy
import threading, _thread

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import seaborn

from DB import DBManager


class ClassForTests(object):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        for id in [1,2,3,4,5,6,7,8,9,11,13,14,15]:
            closeSentimentList = self.getCloseAvgSentimentList(id)
            self.linearRegression(closeSentimentList, id)

            changeCloseSentimentList = self.getChangeCloseAvgSentimentList(id)
            self.linearRegression(changeCloseSentimentList, id)
        

        #id = 2
        #closeSentimentList = self.getCloseAvgSentimentList(id)
        #self.linearRegression(closeSentimentList, id)

        #changeCloseSentimentList = self.getChangeCloseAvgSentimentList(id)
        #self.linearRegression(changeCloseSentimentList, id)

        #_thread.start_new_thread(self.myRegression, (closeSentimentList, id))
        #_thread.start_new_thread(self.myRegression, (changeCloseSentimentList, id))

        #self.regression()
        #self.upDownWithPredict()



    def getCloseAvgSentimentList(self, id):
        # Get close prices
        closeDict = DBManager.DBManager().getDateCloseDictById(id)

        # Get avg sentiment
        avgSentiment = DBManager.DBManager().getAvgSentimentByStockID(id)

        # Create close & avg lists with same dates
        closeList = []
        avgSentimentList = []

        # Create keys
        closeKeys = closeDict.keys()
        avgSentimentKeys = avgSentiment.keys()    
        
        for date in avgSentimentKeys:
            if date in closeKeys:
                closeList.append([closeDict[date]])
                avgSentimentList.append([avgSentiment[date]])


        return [avgSentimentList, closeList]


    def getChangeCloseAvgSentimentList(self, id):
        # Get close prices dict
        closeDict = DBManager.DBManager().getDateCloseDictById(id)

        # Create changeClose from close
        # Create list from dict & copy
        closeList = list(closeDict.items())
        #closeListTemp = copy.copy(closeList)

        changeCloseListTemp = []

        for i in range(len(closeList)):
            if i != 0:
                #closeList[i] = (closeList[i][0], closeList[i][1] / closeList[i-1][1]) #(key, value)
                changeCloseListTemp.append((closeList[i][0], closeList[i][1] / closeList[i-1][1])) #(key, value)

        #for i in range(len(closeListTemp)):
        #    if i != 0:
        #        closeList[i] = (closeList[i][0], closeListTemp[i][1] / closeListTemp[i-1][1]) #(key, value)

        # Remove the first element
        #del closeList[0]

        # Convert list to dict again
        changeCloseListTemp = dict(changeCloseListTemp)

        # Get avg sentiment
        avgSentiment = DBManager.DBManager().getAvgSentimentByStockID(id)

        # Create changeClose & avg lists with same dates
        # Create keys
        closeKeys = changeCloseListTemp.keys()
        avgSentimentKeys = avgSentiment.keys()

        changeCloseList = []
        avgSentimentList = []

        for date in avgSentimentKeys:
            if date in closeKeys:
                changeCloseList.append([changeCloseListTemp[date]])
                avgSentimentList.append([avgSentiment[date]])

        return [avgSentimentList, changeCloseList]


    def linearRegression(self, XYList, id):
        seaborn.set()

        # Get name and symbol
        nameSymbol = DBManager.DBManager().getNameAndSymbolByID(id)
        name = nameSymbol[0]
        symbol = nameSymbol[1]

        # Get x & y lists
        x = sentiment = XYList[0]
        y = close = XYList[1]

        ## Test x & y
        #x = [[1],[2],[3]]
        #y = [[2],[4],[6]]
        #x = [[1],[2],[3],[4],[5],[7],[9]]
        #y = [[2],[5],[5],[9],[10],[10],[20]]

        # Name for Title and axises 
        plt.title("%s (%s) Regression" % (name, symbol))
        plt.xlabel("Sentiment")
        plt.ylabel("Change/Close")

        # Add the points to the graph
        plt.scatter(x, y)

        # Regression
        regression = linear_model.LinearRegression()
        regression.fit(x, y)
        yPreditionsForLine = regression.predict(x)

        # Add the regression line to the graph
        plt.plot(x, yPreditionsForLine)

        # Prediction
        xForPredict = [[0]]
        yPredicted = regression.predict(xForPredict)

        # Add the prediction point to the graph
        plt.scatter(xForPredict, yPredicted, color="red", linewidths=5)

        plt.show()


    def regression(self):
        # Load the diabetes dataset
        diabetes = datasets.load_diabetes()
        print(type(diabetes))
        print(diabetes)


        # Use only one feature
        diabetes_X = diabetes.data[:, np.newaxis, 2]
        print(type(diabetes_X))
        print(diabetes_X)

        # Split the data into training/testing sets
        diabetes_X_train = diabetes_X[:-20]
        print(type(diabetes_X_train))
        print(diabetes_X_train)

        diabetes_X_test = diabetes_X[-20:]
        print(type(diabetes_X_test))
        print(diabetes_X_test)

        # Split the targets into training/testing sets
        diabetes_y_train = diabetes.target[:-20]
        diabetes_y_test = diabetes.target[-20:]

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(diabetes_X_train, diabetes_y_train)

        # Make predictions using the testing set
        diabetes_y_pred = regr.predict(diabetes_X_test)

        # The coefficients
        print('Coefficients: \n', regr.coef_)
        # The mean squared error
        print("Mean squared error: %.2f"
              % mean_squared_error(diabetes_y_test, diabetes_y_pred))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

        # Plot outputs
        plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
        plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

        plt.show()


    def upDownWithPredict(self):
        x = [[1],[-1],[0],[1],[-1],[0],[0],[1],[-1]]   
        xy = [[0],[1],[2],[3],[4],[5],[6],[7],[8]]

        y = [[1],[-1],[0],[0],[0],[-1],[1],[-1],[1]]
        yy = [[0],[1],[2],[3],[4],[5],[6],[7],[8]]

        plt.scatter(xy, x, linewidth=10)
        plt.scatter(yy, y, linewidth=7)

        plt.plot(x, linewidth=4)
        plt.plot(y,linewidth=2)



        plt.show()