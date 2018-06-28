import datetime
import copy
import threading, _thread
import json
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
import seaborn

from DB import DBManager

class prediction(object):
    shiftDays = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prediction(self.shiftDays)


    def prediction(self, shiftDays):
        today = datetime.datetime.now()
        if self.isBusinessDay(today):
            # Get the previous shiftDays bussines day
            prevShiftBD = self.getPreviousShiftBusinessDay(today, shiftDays)

            # Get all stocks IDs
            allStocksIDs = DBManager.DBManager().getAllStocksIDs()
            for stockID in allStocksIDs:
                stockID = stockID[0]

                # If not exsist
                if not DBManager.DBManager().isExsistPredictionByIDAndDate(stockID, today.date()):

                    ## Get allSentiment by date and id
                    #allSentiment = DBManager.DBManager().getSentimentByDateAndId(prevShiftBD.date(), stockID)
                    ## Do average
                    #TotalSentiment = 0
                    #for sentiment in allSentiment:
                    #    TotalSentiment += sentiment[0]
                    #avgSentiment = TotalSentiment / len(allSentiment)

                    # Get changeClose and avgSentiment lists and x for prediction
                    changeCloseAvgSentimentListAndX = self.getChangeCloseAndAvgSentimentListAndX(stockID, shiftDays)
                    changCloseList = changeCloseAvgSentimentListAndX[0]
                    avgSentimentList = changeCloseAvgSentimentListAndX[1]
                    xForPrediction = changeCloseAvgSentimentListAndX[2]

                    # Do regression
                    if not (len(changCloseList) == 0 or len(avgSentimentList) == 0 or  xForPrediction == None):
                        linearRegressionAndRANSACYsAndR2 = self.linearRegressionAndRANSACYsAndR2(changCloseList, avgSentimentList, xForPrediction, stockID)
                        linearRegressionY = linearRegressionAndRANSACYsAndR2[0]
                        RANSACY = linearRegressionAndRANSACYsAndR2[1]
                        linearR2 =  linearRegressionAndRANSACYsAndR2[2]
                        ransacR2 = linearRegressionAndRANSACYsAndR2[3]

                        # Create prediction
                        # Calculate recommendation
                        recommendation = 'SAME'
                        if linearRegressionY > 1 and RANSACY > 1:
                            recommendation = 'UP'
                        elif linearRegressionY < 1 and RANSACY < 1:
                            recommendation = 'DUWN'
                        # Calculate accuracy
                        accuracy = (linearR2 + ransacR2)/2
                        # Add prediction to DB
                        DBManager.DBManager().addPrediction(stockID, today, linearRegressionY, RANSACY, recommendation, accuracy)


    def getChangeCloseAndAvgSentimentListAndX(self, id, shift):
        # Get close prices dict
        closeDict = DBManager.DBManager().getDateCloseDictById(id)

        # Create changeClose from close
        # Create list from dict & copy
        closeList = list(closeDict.items())

        changeCloseListTemp = []
        for i in range(len(closeList)):
            if i != 0:
                changeCloseListTemp.append((closeList[i][0], closeList[i][1] / closeList[i-1][1])) #(key, value)

        # Convert list to dict again
        changeCloseDict = dict(changeCloseListTemp)

        # Get avg sentiment
        avgSentiment = DBManager.DBManager().getAvgSentimentByStockID(id)

        # Create changeClose & avgSentiment lists with same dates entrys
        closeKeys = changeCloseDict.keys()
        avgSentimentKeys = avgSentiment.keys()

        changeCloseList = []
        avgSentimentList = []

        for date in avgSentimentKeys:
            if date in closeKeys:
                changeCloseList.append([changeCloseDict[date]])
                avgSentimentList.append([avgSentiment[date]])

        # Do shift between changeClose and avgSentiment
        avgSentimentX = None
        if len(changeCloseList) >= shift and len(avgSentimentList) >= shift:
            for i in range(shift):
                if i == shift-1:
                    avgSentimentX = avgSentimentList[len(avgSentimentList) - 1]
                del changeCloseList[0]
                del avgSentimentList[len(avgSentimentList) - 1]

        return [changeCloseList, avgSentimentList, avgSentimentX]


    def linearRegressionAndRANSACYsAndR2(self, y, X, xForPrediction, id):
        # Get name and symbol
        nameSymbol = DBManager.DBManager().getNameAndSymbolByID(id)
        name = nameSymbol[0]
        symbol = nameSymbol[1]
        print(name, symbol, ":")

        X = np.array(X)
        y = np.array(y)
        xForPrediction = np.array(xForPrediction)[:,np.newaxis]

        # Linear Regression with OLS algorithm
        linearReg = linear_model.LinearRegression()
        linearReg.fit(X, y)
        lineYLinearRegression = linearReg.predict(X)
        linearR2 = linearReg.score(X,y)
        print("Linear R^2=", linearR2)
        linearRegressionY = linearReg.predict(xForPrediction)


        # Robust linear regression with RANSAC algorithm
        ransac = linear_model.RANSACRegressor()
        ransac.fit(X, y)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        lineYRansac = ransac.predict(X)
        ransacR2 = ransac.score(X[inlier_mask], y[inlier_mask])
        print("RANSAC R^2=", ransacR2)
        ransacY = ransac.predict(xForPrediction)



        ## Polynomial regression with Ridge algorithm
        #lw = 2
        #for count, degree in enumerate([5,6,7]):
        #    model = make_pipeline(PolynomialFeatures(degree), linear_model.Ridge())
        #    model.fit(X, y)
        #    curveYPolynomial = model.predict(X)
        #    plt.plot(X, curveYPolynomial, label="Polynomial degree %d" % degree)
        #    print("Polynomial R^2= %f (degree:%d)"%(model.score(X, y), degree))

        ## Draw points
        ## Draw inlier points
        #plt.scatter(X[inlier_mask], y[inlier_mask], label='Inliers', color='black',  linewidth=4)
        ## Draw outlier points
        #plt.scatter(X[outlier_mask], y[outlier_mask], label='Outliers', color='black', linewidth=2)

        ## Draw lines
        #plt.plot(X, lineYLinearRegression, label='Linear regressor')
        #plt.plot(X, lineYRansac, label='RANSAC regressor')
        ##plt.plot(X, y, label="Ground truth")

        ## Draw predictions
        #plt.scatter(xForPrediction, linearRegressionY, label='Linear Prediction', color='red', linewidth=5)
        #plt.scatter(xForPrediction, ransacY, label='RANSAC Prediction', color='red', linewidth=5)
        print("Preditcion: \n\tLinear= %f \n\tRANSAC= %f" % (linearRegressionY, ransacY))


        ## Title, Labels and legend
        #plt.title("%s (%s) \nLinear, Robust and Polynomial Regression" % (name, symbol))
        #plt.legend(loc='lower right')
        #plt.xlabel("Sentiment")
        #plt.ylabel("ChangClosePrice")

        #plt.show()

        return (linearRegressionY, ransacY, linearR2, ransacR2)


    def isBusinessDay(self, date):
        return bool(len(pandas.bdate_range(date, date)))


    def getPreviousShiftBusinessDay(self, date, shiftDays):
        if shiftDays >= 1:
            prev = date - datetime.timedelta(days=1)
            while len(pandas.bdate_range(prev, date)) < shiftDays+1:
                prev = prev - datetime.timedelta(days=1)
            return prev
        elif shiftDays == 0:
            return date