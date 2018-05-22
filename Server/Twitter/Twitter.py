import twitter
import json
import datetime
from DB import DBManager

class Twitter:

    api = None # Initialized in function readTwitterKeysFromFile()
    threshold = 20 # The number of tweets to be searched for each stock per day

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readTwitterKeysFromFile():

            ## Check rate limit
            #self.checkRateLimit()

            ## Verify Credentials
            #user = self.verifyCredentials()
            #self.printTwitterClass(user)

            ## Search tweets
            #query = ""
            #q = "q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL"
            #resultType = "result_type=mixed"
            #lagudge = "lang=en"
            #count = "count=10"
            #statuses =
            #self.search("q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL&result_type=mixed&lang=en")
            ## "q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL&result_type=mixed&lang=en&count=10"
            #self.printTwitterClass(statuses)

            self.whatToSearch()

            #for i in range(362):
            #    statuses =
            #    self.search("q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL&result_type=mixed&count=1")
            #    if i % 10 == 0:
            #        self.checkRateLimit()


    def readTwitterKeysFromFile(self):
        print("--- In readTwitterKeysFromFile function ---")
        path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterKeys.txt"
        # Open a file
        try:
            twitterKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("--- MyError: In readTwitterKeysFromFile function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = twitterKeysFile.read().splitlines()
        consumer_key = listOfKeys[0]
        consumer_secret = listOfKeys[1]
        access_token_key = listOfKeys[2]
        access_token_secret = listOfKeys[3]
        # Close opened file
        twitterKeysFile.close()

        #Create api object with the keys
        Twitter.api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret, sleep_on_rate_limit=True)
        return True


    def verifyCredentials(self):
        print("--- In verifyCredentials function ---")
        res = Twitter.api.VerifyCredentials()
        return res


    def search(self, query):
        print("--- In search function ---")
        if query == None:
            print("The function Search() received an empty parameter")
        elif query != None:
            statuses = Twitter.api.GetSearch(term = "Gal", count=11)
            print(len(statuses), " Statuses returned!")
            return statuses

    def whatToSearch(self):
        now = datetime.datetime.now()
        dateToSearch = now - datetime.timedelta(days=7) # Sub days from date
        #dayToSearch = now.day - 7

        while dateToSearch < now:
            minTuple = self.getMinTweetsOfStockInDay(dateToSearch) # [0]= count, [1]=id
            if minTuple == False:
                print("--- MyError: whatToSearch is faild.")
                return False
            min = minTuple[0]
            id = minTuple[1]
            while min < Twitter.threshold:
                #search tweets for id
                print("--- In whatToSearch function ---")
                print("--- dateToSearch is: ", dateToSearch, ", for id :", id, ".")
                listOfTweets = self.searchTweets(id, dateToSearch)
                for tweet in listOfTweets:
                    DBManager.DBManager().addTweet(id, tweet)
                minTuple = self.getMinTweetsOfStockInDay(dateToSearch) # [0]= count, [1]=id
                min = minTuple[0]
                id = minTuple[1]

            dateToSearch = dateToSearch + datetime.timedelta(days=1) # Add days to date


    def getMinTweetsOfStockInDay(self, date):
        allStocksID = DBManager.DBManager().getAllStocksID()
        if allStocksID:
            min = Twitter.threshold + 201 # 200(or 100) This is the maximum number of tweets you can search per call
            idOfMin = None

            for stockID in allStocksID:
                id = stockID[0]
                currentCount = DBManager.DBManager().getCountTweetsOfStockInDay(id, date)
                if currentCount == False & currentCount != 0:
                    return False
                if currentCount <= min:
                    min = currentCount
                    idOfMin = id

            minTuple = (min, idOfMin)
            return minTuple
        else:
            return False


    def searchTweets(self, id, date):
        print("--- In searchTweets function ---")
        stockNameSymbol = DBManager.DBManager.getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
        name = stockNameSymbol[0]
        symbol = stockNameSymbol[1]
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        term = nameLower + " OR " + nameCapitalize + " OR " + nameUpper + " AND #$" + symbol

        lang = "en"

        resultType = "mixed" # mixed / recent / popular

        count = 100 # 100 is a max of twitter API

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()
        try:
            statuses = Twitter.api.GetSearch(term=term, until=until, since=since, count=count, lang=lang, result_type=resultType)
            print("---", len(statuses), " Statuses returned!")
            return statuses
        except BaseException as exception:
            print("--- Exception: ", exception)


    def printTwitterClass(self, twitterClass):
        indexInList = 0

        if type(twitterClass) == list:
            for item in twitterClass:
                print("indexInList[", indexInList, "]")
                indexInList = indexInList + 1
                self.printTwitterClass(item)
        else: # Not a list
            print("--- In printTwitterClass function ---")
            print("The type of class is:", type(twitterClass))

            ## Print text of tweet only
            #text = (twitterClass)._json['text']
            #print("text: ", text)

            # Print all class
            #print(json.dumps((twitterClass)._json, indent=4))
            


    def checkRateLimit(self):
        print("--- In checkRateLimit function ---")
        Twitter.api.InitializeRateLimit()
        rate_limit = Twitter.api.rate_limit
        rate_limit_dict = (rate_limit).__dict__

        try:
            resources_dict = rate_limit_dict['resources']
            search_dict = resources_dict['search']
            application_dict = resources_dict['application']
            print(json.dumps(search_dict, indent=4))
            print(json.dumps(application_dict, indent=4))
        except KeyError:
            print("--- MyError: In checkRateLimit function, The key is not found in the dictionary.")





                       


