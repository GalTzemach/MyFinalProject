import pymysql as PyMySQL
import hashlib
import Singleton
import datetime
import json


class DBManager(metaclass=Singleton.Singleton):

    db = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.readDataBaseKeysFromFile():
            print("Could not connect to database.")


    def openDatabaseConnection(self, userName, password, DBName):
        try:
            DBManager.db = PyMySQL.connect("localhost", userName, password, DBName, use_unicode=True, charset="utf8mb4")
        except BaseException as e:
            print("Error in openDatabaseConnection: ", e)
            return False
        return True


    def readDataBaseKeysFromFile(self):
        path = "C:\\myFinalProject\\dataBaseKeys.txt"
        try:
            dataBaseKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError as e:
            print("Error In readDataBaseKeysFromFile: ", e)
            return False

        # Read all file
        listOfKeys = dataBaseKeysFile.read().splitlines()
        userName = listOfKeys[0]
        password = listOfKeys[1]
        DBName = listOfKeys[2]

        # Close opened file
        dataBaseKeysFile.close()

        return self.openDatabaseConnection(userName, password, DBName)


    def stringToMD5(self, str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()


    def addNewUser(self, fName, lName, email, phoneNumber, password):
        passwordMD5 = self.stringToMD5(password)

        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """INSERT INTO 
                 users
                 (first_name, last_name, email, phone_number, password)
                 VALUES 
                 ('%s', '%s', '%s', '%s', '%s' )""" % \
                 (fName, lName, email, phoneNumber, passwordMD5)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addNewUser is failed: ", e)
           return False
        else:
            return True


    def getAllStocks(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT name, symbol, country, industry, subsector 
                 FROM stocks"""
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllStocks is failed: ", e)
            return False
        else:
            return results


    def getCountTweetsOfStockInDay(self, id, date):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT COUNT(id) FROM tweets
                 WHERE stock_id = %d AND created_at LIKE \"%s%%\"""" % \
                 (id, date.date())

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getCountTweetsOfStockInDay is failed: ", e)
            return False
        else:
            return results[0][0]


    def getNameAndSymbolByID(self, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT name, symbol FROM stocks
                 WHERE id = %d""" % \
                 (id)

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchone()
        except BaseException as e:
            print("DB getNameAndSymbolByID is failed: ", e)
            return False
        else:
            return results


    def addTweet(self, id, tweet, nextRequest):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        tweetStr = json.dumps(tweet, indent = 4)
        #print(json.dumps(tweet, indent=4))

        tweet_id = tweet['id']
        text = tweet['full_text'].replace("\n", " ")
        created_at = tweet['created_at']
        createdAtDateTime = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        createdAtTimestamp = createdAtDateTime.strftime('%Y-%m-%d %H:%M:%S') # Without +0000

        if 'followers_count' in tweet['user']:
            followers_count = tweet['user']['followers_count']
        else:
            followers_count = 0

        # Prepare SQL query
        sql = """INSERT INTO tweets
                 (tweet_id, stock_id, the_tweet, text, created_at, followers_count, next_request)
                 VALUES 
                 ('%d', '%d', '%s', '%s', '%s', '%d', '%s')""" % \
                 (tweet_id, id, PyMySQL.escape_string(tweetStr),PyMySQL.escape_string(text), createdAtTimestamp, followers_count, PyMySQL.escape_string(nextRequest))
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
			# Rollback in case there is any error
            DBManager.db.rollback()
            print("DB addTweet is failed: ", e)
            return False
        else:
            return True


    def getTextAndIdsOfTweetToAnalyze(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT text, id, stock_id
                 FROM tweets
                 WHERE ibm_analyzed_text IS NULL AND sentiment IS NULL
                 LIMIT 1"""

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchone()
        except BaseException as e:
            print("DB getTextAndIdsOfTweetToAnalyze is failed: ", e)
            return False
        else:
            return results


    def addAnalyzeToTweet(self, textAnalyzed, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        if isinstance(textAnalyzed, str):
            ibm_analyzed_text = textAnalyzed
            sentiment = -3
        else:
            ibm_analyzed_text = json.dumps(textAnalyzed, indent = 4)

            if 'sentiment' in textAnalyzed:
                if 'document' in textAnalyzed['sentiment']:
                    sentiment = textAnalyzed['sentiment']['document']['score']
                else:
                    sentiment = -2
            else:
                sentiment = -2

        # Prepare SQL query
        sql = """UPDATE tweets
                 SET ibm_analyzed_text = '%s', sentiment = '%f'
                 WHERE id = %d""" % \
                 (PyMySQL.escape_string(ibm_analyzed_text), sentiment, id)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addAnalyzeToTweet is failed: ", e)
           return False
        else:
            return True


    def getLastPriceHistoryDateByID(self, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT MAX(date) 
        FROM prices_history 
        WHERE stock_id=%d""" % \
        (id)

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchone()
        except BaseException as e:
            print("DB getLastPriceHistoryDateByID is failed: ", e)
            return False
        else:
            return results


    def getLastTweetsDate(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT MAX(created_at) 
                 FROM tweets"""

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchone()
        except BaseException as e:
            print("DB getLastTweetsDate is failed: ", e)
            return False
        else:
            return results


    def getSymbolByID(self, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT 
        symbol 
        FROM stocks 
        WHERE id=%d""" % \
        (id)

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchone()
        except BaseException as e:
            print("DB getSymbolByID is failed: ", e)
            return False
        else:
            return results


    def addPriceHistoryDataframe(self, id, priceHistory):

        for i in range(len(priceHistory)):
            row = priceHistory.iloc[i]

            date = row.name[1]
            open = row['Open']
            high = row['High']
            low = row['Low']
            close = row['Close']
            volume = row['Volume']

            self.addPricesHistory(id, date, open, high, low, close, volume)


    def addPricesHistory(self, id, date, open, high, low, close, volume):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """INSERT INTO prices_history
                 (stock_id, date, open, high, low, close, volume)
                 VALUES 
                 ('%d', '%s', '%f', '%f', '%f', '%f', '%f' )""" % \
                 (id, date, open, high, low, close, volume)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addPricesHistory is failed: ", e)
           return False
        else:
            return True


    def getAllTweetsCountInDay(self, dateToSearch):
        allId = self.getAllStocksIDs()
        if allId == False:
            print("DB getAllTweetsCountInDay is failed.")
            return False

        idCountDict = {}

        for id in allId:
            countTweets = self.getCountTweetsOfStockInDay(id[0], dateToSearch)
            if countTweets == False and countTweets != 0:
                print("DB getAllTweetsCountInDay is failed.")
                return False
            else:
                idCountDict[id[0]] = countTweets

        return idCountDict


    def getDateCloseDictById(self, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT date, close 
                 FROM prices_history
                 WHERE stock_id = %d""" % (id)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getDateCloseDictById is failed: ", e)
            return False
        else:
            dateClose = {}
            for res in results:
                dateClose[res[0]] = res[1]
            return dateClose


    def getAvgSentimentByStockID(self, id):
        # Create dateSentiment dict
        dateSentimentDict = {}

        # Get all uniqe Dates of tweets by stockID
        allDates = self.getAllDatesOfTweetsById(id)

        for date in allDates:
            # Get all sentiments by date & stockID
            allSentiment = self.getSentimentByDateAndId(date[0], id)

            # Create AVG of sentiment per date
            TotalSentiment = 0
            for sentiment in allSentiment:
                TotalSentiment += sentiment[0]
            avgSentiment = TotalSentiment / len(allSentiment)

            # Add date avgSentiment to dict
            dateSentimentDict[date[0]] = avgSentiment

        return dateSentimentDict
        

    def getAllDatesOfTweetsById(self, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT DISTINCT date(created_at) 
                 FROM tweets
                 WHERE stock_id = %d""" % (id)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllDatesOfTweetsById is failed: ", e)
            return False
        else:
            return results


    def getSentimentByDateAndId(self, date, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT sentiment 
                 FROM tweets
                 WHERE created_at LIKE \"%s%%\" and stock_id = %d and sentiment != -2 and sentiment != -3""" % (date, id) #-2 and -3 is arror analyze
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getSentimentByDateAndId is failed: ", e)
            return False
        else:
            return results


    def signIn(self, email, password):
        password = self.stringToMD5(password)

        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT count(id) 
                 FROM users
                 WHERE email = \"%s\" and password = \"%s\" """ % (email, password)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB signIn is failed: ", e)
            return False
        else:
            if results[0][0] > 0:
                if self.setIsConnect(email, True):
                    return True
            return False


    def setIsConnect(self, email, isConnect):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """UPDATE users
                    SET is_connect = '%d'
                    WHERE email = \"%s\" """ % \
                    (isConnect, email)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            DBManager.db.commit()
        except BaseException as e:
            # Rollback in case there is any error
            DBManager.db.rollback()
            print("DB setIsConnect is failed: ", e)
            return False
        else:
            return True


    def getIDByEmail(self, email):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT id 
                 FROM users
                 WHERE email = \"%s\" """ % (email)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getIDByEmail is failed: ", e)
            return False
        else:
            return results


    def getFullNameByID(self, ID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT first_name, last_name 
                 FROM users
                 WHERE id = %d """ % (ID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getFullNameByID is failed: ", e)
            return False
        else:
            return results


    def getExplanationBySymbol(self, symbol):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT explanation 
                 FROM stocks
                 WHERE symbol = \"%s\" """ % (symbol)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getExplanationBySymbol is failed: ", e)
            return False
        else:
            return results


    def getStockIDBySymbol(self, symbol):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """SELECT id 
                 FROM stocks
                 WHERE symbol = \"%s\" """ % (symbol)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getStockIDBySymbol is failed: ", e)
            return False
        else:
            return results


    def getAllTweetsByStockID(self, stockID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT created_at, followers_count, sentiment, text
                 FROM tweets
                 WHERE stock_id = %d """ % (stockID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllTweetsByStockID is failed: ", e)
            return False
        else:
            return results


    def getMyStocksIDs(self, ID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT stock_id
                 FROM users_stocks
                 WHERE user_id = %d """ % (ID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getMyStocksIDs is failed: ", e)
            return False
        else:
            return results


    def getStockByID(self, stockID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT name, symbol, country, industry, subsector 
                 FROM stocks
                 WHERE id = %d """ % (stockID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getStockByID is failed: ", e)
            return False
        else:
            return results


    def getAllStocksIDs(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT id 
                 FROM stocks"""
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllStocksIDs is failed: ", e)
            return False
        else:
            return results


    def deleteStockByIDs(self, userID, stockID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """DELETE FROM users_stocks
                 WHERE user_id = %d and stock_id = %d """ % \
                    (userID, stockID)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            DBManager.db.commit()
        except BaseException as e:
            # Rollback in case there is any error
            DBManager.db.rollback()
            print("DB deleteStockByIDs is failed: ", e)
            return False
        else:
            return True


    def addStockToUser(self, userID, stockID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """INSERT INTO users_stocks
                 (user_stock_id, user_id, stock_id)
                 VALUES ('%d', '%d', '%d')""" % \
                 (int(str(userID) + str(stockID)), userID, stockID)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addStockToUser is failed: ", e)
           return False
        else:
            return True


    def addPrediction(self, stockID, today, linearRegressionY, RANSACY, recommendation, accuracy):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """INSERT INTO predictions
                 (stock_id, date, linear_regression, ransac, recommendation, accuracy)
                 VALUES ('%d', '%s', '%f', '%f', '%s', '%f')""" % \
                 (stockID, today, linearRegressionY, RANSACY, recommendation, accuracy)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addPrediction is failed: ", e)
           return False
        else:
            return True


    def isExsistPredictionByIDAndDate(self, stockID, date):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT count(id) 
                 FROM predictions
                 WHERE stock_id = %d and date LIKE \"%s%%\" """ % \
                     (stockID, date)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB isExsistPredictionByIDAndDate is failed: ", e)
            return False
        else:
            return results[0][0] > 0


    def getPredictionByIDAndDate(self, stockID, date):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT * 
                 FROM predictions
                 WHERE stock_id = %d and date LIKE \"%s%%\" """ % \
                     (stockID, date)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getPredictionByIDAndDate is failed: ", e)
            return False
        else:
            if results:
                return results
            else:
                return False


    def getAllRegisterToStockByID(self, stockID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT user_id 
                 FROM users_stocks
                 WHERE stock_id = %d """ % \
                     (stockID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllRegisterToStockByID is failed: ", e)
            return False
        else:
            if results:
                return results
            else:
                return False


    def addUserPrediction(self, userID, predictionID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query
        sql = """INSERT INTO users_predictions
                 (user_prediction_id, user_id, prediction_id)
                 VALUES ('%d', '%d', '%d')""" % \
                 (int(str(userID) + str(predictionID)), userID, predictionID)
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as e:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("DB addUserPrediction is failed: ", e)
           return False
        else:
            return True


    def getEmailByID(self, userID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT email 
                 FROM users
                 WHERE id = %d """ % \
                     (userID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getEmailByID is failed: ", e)
            return False
        else:
            return results


    def getAllPredictionsIDByUserID(self, userID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT prediction_id 
                 FROM users_predictions
                 WHERE user_id = %d """ % \
                     (userID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getAllPredictionsIDByUserID is failed: ", e)
            return False
        else:
            return results


    def getPredictionByID(self, predID):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query
        sql = """SELECT stock_id, date(date), recommendation 
                 FROM predictions
                 WHERE id = %d """ % \
                     (predID)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as e:
            print("DB getPredictionByID is failed: ", e)
            return False
        else:
            return results

