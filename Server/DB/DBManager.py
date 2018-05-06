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
            
            # Add
            #self.addNewUser("g", "t", "gt@gmail.com", "0000000000", "123")
            ##return boolean

            # signin




            #DBManager.db.close()
            pass
        else:
            print("MY_PRINT: Could not connect to database.")



    def openDatabaseConnection(self, userName, password, DBName):
        try:
            DBManager.db = PyMySQL.connect("localhost", userName, password, DBName, use_unicode=True, charset="utf8")
        except:
            return False

        return True


    def readDataBaseKeysFromFile(self):
        path = "C:\\Users\\Gal Tzemach\\Desktop\\dataBaseKeys.txt"
        # Open a file
        try:
            dataBaseKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("MY-ERROR: In readDataBaseKeysFromFile function, File ", path, " not found.")
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

        # Prepare SQL query to INSERT a record into the database.
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
           print("MY-Error: Insert user failed")
           print("Exception: ", exception)
           return False
        else:
            print("MY-SUCCESS: Insert user successfully.")
            return True


    def stringToMD5(self, str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()


    def getAllStocksID(self):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query to INSERT a record into the database.
        sql = """SELECT id FROM stocks"""
        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch all the rows in a tuple of tuples.
            results = cursor.fetchall()
        except BaseException as exception:
            print("MY-Error: getAllStocksID is failed")
            print("Exception: ", exception)
            return False
        else:
            print("MY-SUCCESS: getAllStocksID is successfully.")
            return results


    def getCountTweetsOfStockInDay(self, id, date):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query to INSERT a record into the database.
        sql = """SELECT COUNT(id) FROM tweets
                 WHERE stock_id = %d AND created_at LIKE \"%s%%\"""" % \
                 (id, date.date())

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch all the rows in a tuple of tuples.
            results = cursor.fetchall()
        except BaseException as exception:
            print("MY-Error: getCountTweetsOfStockInDay is failed")
            print("Exception: ", exception)
            return False
        else:
            print("MY-SUCCESS: getCountTweetsOfStockInDay is successfully.")
            return results[0][0]


    def getNameAndSymbolOfStock(id):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        # Prepare SQL query to INSERT a record into the database.
        sql = """SELECT name, symbol FROM stocks
                 WHERE id = %d""" % \
                 (id)

        try:
            # Execute the SQL command
            cursor.execute(sql)

            # Fetch all the rows in a tuple of tuples.
            results = cursor.fetchone()
        except BaseException as exception:
            print("MY-Error: getNameAndSymbolOfStock is failed")
            print("Exception: ", exception)
            return False
        else:
            print("MY-SUCCESS: getNameAndSymbolOfStock is successfully.")
            return results


    def addTweet(self, id, tweet):
        # prepare a cursor object using cursor() method
        cursor = DBManager.db.cursor()

        tweet_id = tweet._json['id']
        text = tweet._json['text']
        created_at = tweet._json['created_at']
        createdAtDateTime = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        createdAtTimestamp = createdAtDateTime.strftime('%Y-%m-%d %H:%M:%S') # Without +0000

        if 'followers_count' in tweet._json:
            followers_count = tweet._json['followers_count']
        else:
            followers_count = 0

        myFilter = "term=nameLower OR nameCapitalize OR nameUpper AND #$symbol, lang=en, resultType=mixed, count=200" #Gal

        tweetStr = json.dumps(tweet._json)

        # Prepare SQL query to INSERT a record into the database.
        sql = """INSERT INTO tweets
                 (tweet_id, stock_id, the_tweet, text, created_at, followers_count, filter, ibm_analyzed_text, sentiment, emotions)
                 VALUES 
                 ('%d', '%d', '%s', '%s', '%s', '%d', '%s', '%s', '%f', '%s' )""" % \
                 (tweet_id, id, tweetStr,text, createdAtTimestamp, followers_count, myFilter, "{}", 0.0, "{}")
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Commit your changes in the database
           DBManager.db.commit()
        except BaseException as exception:
           # Rollback in case there is any error
           DBManager.db.rollback()
           print("MY-Error: Insert tweet failed")
           print("Exception: ", exception)
           return False
        else:
            print("MY-SUCCESS: Insert tweet successfully.")
            return True