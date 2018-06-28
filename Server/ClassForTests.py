import datetime
import copy
import threading, _thread
import json

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
import seaborn

from DB import DBManager


class ClassForTests(object):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        for id in [1,2,3,4,5,6,7,8,9,11,13,14,15]:
            # Get name and symbol
            nameSymbol = DBManager.DBManager().getNameAndSymbolByID(id)
            name = nameSymbol[0]
            symbol = nameSymbol[1]
            print(name, symbol, ":")


        closeSentimentList = self.getCloseAvgSentimentList(id, 3)
        changeCloseSentimentList = self.getChangeCloseAvgSentimentList(id, 3)


    def RRP(self, XYList, id, typeY, name, symbol):
        X = np.array(XYList[0])
        y = np.array(XYList[1])

        # Linear Regression
        linearReg = linear_model.LinearRegression()
        linearReg.fit(X, y)

        # Robustly fit linear model with RANSAC algorithm
        ransac = linear_model.RANSACRegressor()
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)

        # Predict data of estimated models
        line_y = linearReg.predict(X)

        line_y_ransac = ransac.predict(X)

        print(typeY, "=")
        lw = 2
        for count, degree in enumerate([5,10,20]):
            model = make_pipeline(PolynomialFeatures(degree), linear_model.Ridge())
            model.fit(X, y)
            curveY = model.predict(X)
            plt.plot(X, curveY, linewidth=lw, label="degree %d" % degree)
            print("Polynomial R^2= %f (degree:%d)"%(model.score(X, y), degree))


        print("Linear R^2=", linearReg.score(X,y))
        print("RANSAC R^2=", ransac.score(X[inlier_mask], y[inlier_mask]))

        # Inlier points
        plt.scatter(X[inlier_mask], y[inlier_mask], marker='.', label='Inliers', linewidth=5)
        # Outlier points
        plt.scatter(X[outlier_mask], y[outlier_mask], marker='.',label='Outliers', linewidth=5)
        #plt.scatter(X, y, color='navy', s=30, marker='o', label="training points")
        # Line of linear
        plt.plot(X, line_y, linewidth=lw, label='Linear regressor')
        # Line of RANSAC
        plt.plot(X, line_y_ransac, linewidth=lw, label='RANSAC regressor')
        # Curve of Polynomial
        #plt.plot(X, y, color='cornflowerblue', linewidth=lw, label="ground truth")

        plt.title('Linear Robust and Polynomial Regression' + name + symbol)
        plt.legend(loc='lower right')
        plt.xlabel("Sentiment")
        plt.ylabel(typeY)
        plt.show()


    def getCloseAvgSentimentList(self, id, shift):
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


    def getChangeCloseAvgSentimentList(self, id, shift):
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








