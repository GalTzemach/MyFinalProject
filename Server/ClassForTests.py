import datetime
import copy

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import seaborn

from DB import DBManager

class ClassForTests(object):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.upDownWithPredict()
        #self.myRegression()
        #self.regression()

        id = 4
        #closeAndSentimentList = self.realDataTest(id)
        changeCloseAndSentimentList = self.realDataTestChangeClose(id)
        self.myRegression(changeCloseAndSentimentList, id)

    def realDataTest(self, id):
        # Get close prices
        closePrice = DBManager.DBManager().getClosePricePerDateById(id)
        closePriceKeys = closePrice.keys()

        # Get AVG sentument
        avgSentiment = DBManager.DBManager().getAvgSentimentPerDateById(id)
        avgSentimentKeys = avgSentiment.keys()

        closePriceList = []
        avgSentimentList = []

        for date in avgSentimentKeys:
            if date in closePriceKeys:
                closePriceList.append([closePrice[date]])
                avgSentimentList.append([avgSentiment[date]])

        return [closePriceList, avgSentimentList]


    def realDataTestChangeClose(self, id):
        # Get close prices
        closePrice = DBManager.DBManager().getClosePricePerDateById(id)
        closePriceKeys = closePrice.keys()

        # Changing closePrise dict to closePriceList list
        closePriceList = closePrice.items()
        closePriceList = list(closePriceList)
        closePriceListOld = copy.copy(closePriceList)

        # Turn change close from close on list
        for i in range(len(closePriceListOld)):
            if i == 0:
                pass
            else:
                closePriceList[i] = (closePriceList[i][0], closePriceListOld[i][1] / closePriceListOld[i-1][1])

        # Remove the first element
        del closePriceList[0]

        # Change again closePriceList list to closePrice dict
        closePrice = dict(closePriceList)


        # Get average sentument
        avgSentiment = DBManager.DBManager().getAvgSentimentPerDateById(id)
        avgSentimentKeys = avgSentiment.keys()

        closePriceList = []
        avgSentimentList = []

        for date in avgSentimentKeys:
            if date in closePriceKeys:
                closePriceList.append([closePrice[date]])
                avgSentimentList.append([avgSentiment[date]])

        return [closePriceList, avgSentimentList]


    def myRegression(self, closeSentimentList, id):
        seaborn.set()

        # Get name and symbol
        nameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id)
        name = nameSymbol[0]
        symbol = nameSymbol[1]

        x = sentiment = closeSentimentList[1]
        y = close = closeSentimentList[0]

        #x = [[1],[2],[3]]
        #y = [[2],[4],[6]]

        #x = [[1],[2],[3],[4],[5],[7],[9]]
        #y = [[2],[5],[5],[9],[10],[10],[20]]

        plt.title("%s (%s) \nRegression between close prise and sentiment" % (name, symbol))
        plt.xlabel("Sentiment")
        plt.ylabel("Change-Close")
        plt.scatter(x, y)

        # Regression
        regression = linear_model.LinearRegression()
        regression.fit(x, y)

        # line
        preditionsForLine = regression.predict(x)
        plt.plot(x, preditionsForLine)

        # Prediction
        forPredict = [[0]]
        predicted = regression.predict(forPredict)
        plt.scatter(forPredict, predicted, color="red", linewidths=5)

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