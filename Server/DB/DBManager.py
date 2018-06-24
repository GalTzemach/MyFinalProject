import pymysql as PyMySQL
import hashlib
import encodings
import Singleton
import datetime
import json

class DBManager(metaclass=Singleton.Singleton):
    """description of class"""

    db = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readDataBaseKeysFromFile():
            pass
        else:
            print("Could not connect to database.")



    def openDatabaseConnection(self, userName, password, DBName):
        try:
            DBManager.db = PyMySQL.connect("localhost", userName, password, DBName, use_unicode=True, charset="utf8mb4")
        except BaseException as exception:
            print(exception)
            return False

        return True


    def readDataBaseKeysFromFile(self):
        path = "C:\\Users\\Gal Tzemach\\Desktop\\dataBaseKeys.txt"
        # Open a file
        try:
            dataBaseKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("--- MyError: In readDataBaseKeysFromFile function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = dataBaseKeysFile.read().splitlines()
        userName = listOfKeys[0]
        password = listOfKeys[1]
        DBName = listOfKeys[2]

        # Close opened file
        dataBaseKeysFile.close()

        if self.openDatabaseConnection(userName, password, DBName):
            return True
        else:
            return False


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
        except BaseException as exception:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("--- MyError: Insert user failed")
           print("--- Exception: ", exception)
           return False
        else:
            #print("--- MySuccess: Insert user successfully.")
            return True


    def stringToMD5(self, str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()


    def getAllStocksID(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()
        # Prepare SQL query 
        sql = """SELECT id FROM stocks"""
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as exception:
            print("--- MyError: getAllStocksID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getAllStocksID is successfully.")
            return results


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
        except BaseException as exception:
            print("--- MyError: getAllStocks is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getAllStocks is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getCountTweetsOfStockInDay is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getCountTweetsOfStockInDay of id ", id, " is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getNameAndSymbolByID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getNameAndSymbolByID is successfully.")
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
        except BaseException as exception:
			# Rollback in case there is any error
            DBManager.db.rollback()
            print("--- MyError: Insert tweet failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: Insert tweet successfully.")
            return True


   # def addTweet(self, id, tweet):
   #     # prepare a cursor object using cursor() method
   #     cursor = DBManager.db.cursor()

   #     tweetStr = json.dumps(tweet)

   #     tweet_id = tweet._json['id']
   #     text = tweet._json['text']
   #     created_at = tweet._json['created_at']
   #     createdAtDateTime = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
   #     createdAtTimestamp = createdAtDateTime.strftime('%Y-%m-%d %H:%M:%S') # Without +0000

   #     if 'followers_count' in tweet._json['user']:
   #         followers_count = tweet._json['user']['followers_count']
   #     else:
   #         followers_count = 0

   #     myFilter = "term=nameLower OR nameCapitalize OR nameUpper AND #$symbol, lang=en, resultType=mixed, count=200" #Gal



   #     # Prepare SQL query 
   #     sql = """INSERT INTO tweets
   #              (tweet_id, stock_id, the_tweet, text, created_at, followers_count, filter)
   #              VALUES 
   #              ('%d', '%d', '%s', '%s', '%s', '%d', '%s')""" % \
   #              (tweet_id, id, PyMySQL.escape_string(tweetStr),PyMySQL.escape_string(text), createdAtTimestamp, followers_count, myFilter)
   #     try:
   #        # Execute the SQL command
   #        cursor.execute(sql)
   #        # Commit your changes in the database
   #        DBManager.db.commit()
   #     except BaseException as exception:
			## Rollback in case there is any error
   #         DBManager.db.rollback()
   #         print("--- MyError: Insert tweet failed")
   #         print("--- Exception: ", exception)
   #         return False
   #     else:
   #         #print("--- MySuccess: Insert tweet successfully.")
   #         return True


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
        except BaseException as exception:
            print("--- MyError: getTextAndIdsOfTweetToAnalyze is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getTextAndIdsOfTweetToAnalyze is successfully.")
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
        except BaseException as exception:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("--- MyError: Insert analyzed to tweet failed")
           print("--- Exception: ", exception)
           return False
        else:
            #print("--- MySuccess: Insert analyzed to tweet is successfully.")
            return True


    def getLastDateByID(self, id):
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
        except BaseException as exception:
            print("--- MyError: getLastDateByID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getLastDateByID is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getSymbolByID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getSymbolByID is successfully.")
            return results


    def addPriceHistoryDataframe(self, id, priceHistory):

        for i in range(len(priceHistory)):
            row = priceHistory.iloc[i]

            date = row.name[1]
            open = row['Open']
            high = row['High']
            low  = row['Low']
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
        except BaseException as exception:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("--- MyError: Insert PricesHistory failed")
           print("--- Exception: ", exception)
           return False
        else:
            #print("--- MySuccess: Insert PricesHistory successfully.")
            return True


    def getAllTweetsCountInDay(self, dateToSearch):
        allId = self.getAllStocksID()
        if allId == False:
            print("--- MyError: getAllTweetsCountInDay is failed")
            return False

        idCountDict = {}

        for id in allId:
            countTweets = self.getCountTweetsOfStockInDay(id[0], dateToSearch)
            if countTweets == False and countTweets != 0:
                print("--- MyError: getAllTweetsCountInDay is failed")
                return False
            else:
                idCountDict[id[0]] = countTweets

        return idCountDict


    def getClosePricePerDateById(self, id):
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
        except BaseException as exception:
            print("--- MyError: getClosePricePerDateById is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getClosePricePerDateById is successfully.")
            dateClose = {}
            for res in results:
                dateClose[res[0]] = res[1]
            return dateClose


    def getAvgSentimentPerDateById(self, id):
        dateSentiment = {}

        # Get all uniqe Dates of tweets of stock
        allDatesOfTweets = self.getAllDatesOfTweetsById(id)

        for date in allDatesOfTweets:
            # Get all sentiment of stock per date
            allSentimentPerDateAndId = self.getSentimentByDateAndId(date[0], id)

            # Create AVG of sentiment per date
            sumOfSentiment = 0
            for sentiment in allSentimentPerDateAndId:
                sumOfSentiment += sentiment[0]
            avgSentimentPerDate = sumOfSentiment / len(allSentimentPerDateAndId)

            dateSentiment[date[0]] = avgSentimentPerDate

        return dateSentiment
        

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
        except BaseException as exception:
            print("--- MyError: getAllDatesOfTweetsById is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getAllDatesOfTweetsById is successfully.")
            return results


    def getSentimentByDateAndId(self, date, id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query 
        sql = """SELECT sentiment 
                 FROM tweets
                 WHERE created_at LIKE \"%%%s%%\" and stock_id = %d""" % (date, id)
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch
            results = cursor.fetchall()
        except BaseException as exception:
            print("--- MyError: getSentimentByDateAndId is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getSentimentByDateAndId is successfully.")
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
        except BaseException as exception:
            print("--- MyError: signIn is failed")
            print("--- Exception: ", exception)
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
        except BaseException as exception:
            # Rollback in case there is any error
            DBManager.db.rollback()
            print("--- MyError: setIsConnect failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: setIsConnect is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getIDByEmail is failed")
            print("--- Exception: ", exception)
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
        except BaseException as exception:
            print("--- MyError: getFullNameByID is failed")
            print("--- Exception: ", exception)
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
        except BaseException as exception:
            print("--- MyError: getExplanationBySymbol is failed")
            print("--- Exception: ", exception)
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
        except BaseException as exception:
            print("--- MyError: getStockIDBySymbol is failed")
            print("--- Exception: ", exception)
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
        except BaseException as exception:
            print("--- MyError: getAllTweetsByStockID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getAllStocks is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getMyStocks is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getMyStocks is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getStockByID is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getStockByID is successfully.")
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
        except BaseException as exception:
            print("--- MyError: getAllStocksIDs is failed")
            print("--- Exception: ", exception)
            return False
        else:
            #print("--- MySuccess: getAllStocksIDs is successfully.")
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
        except BaseException as exception:
            # Rollback in case there is any error
            DBManager.db.rollback()
            print("deleteStockByIDs is failed")
            print(exception)
            return False
        else:
            #print("deleteStockByIDs is successfully.")
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
        except BaseException as exception:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("addStockToUser is failed")
           print(exception)
           return False
        else:
            #print("addStockToUser is successfully.")
            return True