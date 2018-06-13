import twitter
import json
import datetime
from DB import DBManager
from TwitterAPI import TwitterAPI, TwitterPager, TwitterResponse
import pause 

class Twitter:

    apiOfTwitter = None # Initialized in function readTwitterKeysFromFile()
    api = None # Initialized in function readTwitterKeysFromFile()

    threshold = 10000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readTwitterKeysFromFile():

            ## Check rate limit
            #self.checkRateLimitOld()

            ## Verify Credentials
            #user = self.verifyCredentials()

            ## search()
            #self.search("q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL%20since%3A2018-05-28%20until%3A2018-05-29&result_type=mixed&lang=en&count=600")

            self.whatToSearch()


    def readTwitterKeysFromFile(self):
        #print("--- In readTwitterKeysFromFile function ---")
        #path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterKeys.txt"
        path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterSandboxKeys.txt"

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
        Twitter.apiOfTwitter = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret, sleep_on_rate_limit=True)
        Twitter.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        return True


    def whatToSearchOld(self):
        #print("--- In whatToSearch function ---")

        now = datetime.datetime.now()
        dateToSearch = now - datetime.timedelta(days=7) # Sub days from date

        while dateToSearch < now:
            besidesIDSet = set()

            minTuple = self.getMinTweetsInDay(dateToSearch) # [0]= count, [1]=id
            if minTuple == False:
                print("--- MyError: whatToSearch is faild in getMinTweetsInDay().")
                return False
            minTweets = minTuple[0]
            id = minTuple[1]

            while minTweets < Twitter.threshold:
                stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
                if stockNameSymbol == False:
                    print("--- MyError: whatToSearch is faild in getNameAndSymbolOfStock().")
                    return False

                print("--- dateToSearch is: %s, for %s stock (%s, %d)." % (dateToSearch.date(), stockNameSymbol[0], stockNameSymbol[1], id))

                # Get tweets
                listOfTweets = self.searchTweets(id, dateToSearch)

                if listOfTweets == False:
                    print("--- MyError: whatToSearch is faild in ().")
                    return False

                numberOfTweetsNotInserted = 0
                countTweets = 0
                textSet = set()
                idSet = set()

                for tweet in listOfTweets:
                    tweetJson = tweet._json

                    countTweets += 1

                    # Add tweet to sets
                    idSet.add(tweetJson['id_str'])
                    textSet.add(tweetJson['text'])

                    # Add tweet to database
                    if DBManager.DBManager().addTweet(id, tweet) != True:
                        numberOfTweetsNotInserted += 1


                uniqeTweetsId = len(idSet)
                uniqeTweetsText = len(textSet)

                print("--- %d from %d tweets are uniqe (id)" % (len(idSet), countTweets))
                print("--- %d from %d tweets are uniqe (text)" % (len(textSet), countTweets))

                print("--- %d tweets inserted to DB." % (countTweets - numberOfTweetsNotInserted))

                if countTweets == 0 or numberOfTweetsNotInserted >= uniqeTweetsId:
                    besidesIDSet.add(id)

                minTuple = self.getMinTweetsInDay(dateToSearch, besidesIDSet) # [0]= count, [1]=id

                if minTuple != False:
                    minTweets = minTuple[0]
                    id = minTuple[1]
                else:
                    print("--- MyError: whatToSearch is faild in getMinTweetsInDay().")
                    return False

            dateToSearch = dateToSearch + datetime.timedelta(days=1) # Add days to date


    def whatToSearch(self):
        #print("--- In whatToSearch function ---")

        # Get current time and prepare the time for initial search
        now = datetime.datetime.now()
        dateToSearch = now - datetime.timedelta(days=10) # Sub days from date

        while dateToSearch < now:

            # A set of ID numbers ignore them
            besidesIDSet = set()

            # Get min tweet (count and id)
            minTuple = self.getMinTweetsInDay(dateToSearch) # [0]= count, [1]=id
            if minTuple == False:
                print("--- MyError: whatToSearch is faild in getMinTweetsInDay().")
                return False
            minTweets = minTuple[0]
            id = minTuple[1]

            while minTweets == 0: #< Twitter.threshold:

                # Get name & symbol of tweet
                stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
                if stockNameSymbol == False:
                    print("--- MyError: whatToSearch is faild in getNameAndSymbolOfStock().")
                    return False
                name = stockNameSymbol[0]
                symbol = stockNameSymbol[1]

                # Print search details 
                print("\n--- Search for Date: %s, for \"%s\" stock (symbol:%s, id:%d):" % (dateToSearch.date(), name, symbol, id))

                try:
                    # Get/Search tweets
                    results = self.getTweetsStandard7Days(id, dateToSearch)

                except BaseException as exception:
                    if 'status_code' in exception.__dict__:
                        if exception.status_code == 429: # rate limit
                            print("--- Exception: %s" % (exception))

                            # Get rate limit details
                            rateLimitDict = self.checkRateLimit()
                            reset = rateLimitDict['resources']['search']['/search/tweets']['reset']
                            reset += 10

                            d = datetime.datetime.fromtimestamp(reset)
                            print("\n\n--- Sleep for rate limit until %s (%s)\n\n" % (d, reset))
                            
                            pause.until(reset) #Stops the thread until the service restarts
                          
                          # Get/Search tweets again
                            results = self.getTweetsStandard7Days(id, dateToSearch)



                if results == False:
                    print("--- MyError: whatToSearch is faild in getTweets...().")
                    return False

                tweets = results[0]
                nextRequest = results[1]

                numberOfTweetsNotInserted = 0
                countTweets = 0
                textSet = set()
                idSet = set()

                for tweet in tweets:
                    countTweets += 1

                    # Add tweet to sets
                    idSet.add(tweet['id_str'])
                    textSet.add(tweet['text'])

                    # Add tweet to database
                    if DBManager.DBManager().addTweet(id, tweet, nextRequest) != True:
                        numberOfTweetsNotInserted += 1


                uniqeTweetsId = len(idSet)
                uniqeTweetsText = len(textSet)

                print("--- In whatToSearch() \n\t%d tweets received \n\t%d uniqe(id) \n\t%d uniqe(text)" % (countTweets, len(idSet), len(textSet)))

                numberOfInsertedTweets = countTweets - numberOfTweetsNotInserted
                if countTweets > 0:
                    print("%d tweets inserted to DB." % (numberOfInsertedTweets))

                if countTweets == 0: 
                    besidesIDSet.add(id)
                    print("0 Tweets received, Check the reason.")
                elif countTweets > 0 and numberOfInsertedTweets == 0: 
                    print("0 Tweets inseted to DB, Check the reason.")
                elif countTweets > 0 and numberOfInsertedTweets < uniqeTweetsId: 
                    print("Not all unique(id) tweets have been inserted to DB, Check the reason.")
                elif countTweets > 0 and numberOfInsertedTweets == uniqeTweetsId:
                    print("All unique(id) tweets of stock %s (%s) for date %s have been inserted to DB!" % (name, symbol, dateToSearch.date()))
                    besidesIDSet.add(id)

                minTuple = self.getMinTweetsInDay(dateToSearch, besidesIDSet) # [0]= count, [1]=id

                if minTuple != False:
                    minTweets = minTuple[0]
                    id = minTuple[1]
                else:
                    print("--- MyError: whatToSearch is faild in getMinTweetsInDay().")
                    return False

            dateToSearch = dateToSearch + datetime.timedelta(days=1) # Add days to date


    def getTweetsPremium30Days(self, id, date):
        #print("--- In getTweetsPremium30Days function ---")

        # Get name & symbol
        stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
        if stockNameSymbol == False:
            print("--- MyError: getTweets is faild in getNameAndSymbolOfStock().")
            return False
        name = stockNameSymbol[0]
        symbol = stockNameSymbol[1]

        # Preparing the parameters for the request
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        symbolLower = symbol.lower()
        symbolCapitalize = symbol.capitalize()
        symbolUpper = symbol.upper()

        resultType = 'mixed' # mixed recent popular is options
        
        count = 100
        maxResultsSandbox = 100
        maxResults = 500

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        PRODUCT = '30day'
        LABEL = 'prob'
        RESOURCE = 'tweets/search/%s/:%s' % (PRODUCT, LABEL)

        q = "%s %s OR %s %s OR %s %s" % (nameLower, symbolUpper, nameCapitalize, symbolUpper, nameUpper, symbolUpper)
        lang = "en"
        query = "lang:%s %s" % (lang, q)
        PARAMS = {'query':query, 'maxResults':maxResults, 'fromDate':since, 'toDate':until}

        # Get the tweets from twitter
        r = Twitter.api.request(RESOURCE, PARAMS)

        # Get the response as a JSON object.
        rJson = TwitterResponse(r, False).json()
        #self.printDict(rJson)

        next = None
        next = rJson['next']

        tweetsList = []
        idSet = set()
        countTweets = 0

        for item in r.get_iterator():
            if 'text' in item:
                item['text'] = item['text'].replace("\n", " ")
                countTweets += 1
                tweetsList.append(item)
                idSet.add(item['id_str'])
                #print("%d) %s \nid: %s \ncreated_at: %s" % (countTweets, item['text'], item['id_str'], item['created_at']))
            elif 'message' in item :
               print ('ERROR message: %s, code:(%d).' % (item['message'], item['code']))
               return False

        print("%d tweets received." % (countTweets))
        print("%d tweets is uniqe." % (len(idSet)))

        if next:
            nextRequest = "%s, {'query':%s, 'maxResults':%s, 'fromDate':%s, 'toDate':%s, 'next':%s}" % (RESOURCE, query, maxResults, since, until, next)

        results = [tweetsList, nextRequest]
        return results
           

    def getTweetsSandbox30Days(self, id, date):
        #print("--- In getTweetsSandbox30Days function ---")

        # Get name & symbol
        stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
        if stockNameSymbol == False:
            print("--- MyError: getTweets is faild in getNameAndSymbolOfStock().")
            return False
        name = stockNameSymbol[0]
        symbol = stockNameSymbol[1]

        # Preparing the parameters for the request
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        symbolLower = symbol.lower()
        symbolCapitalize = symbol.capitalize()
        symbolUpper = symbol.upper()

        resultType = 'mixed' # mixed recent popular is options
        
        count = 100
        maxResultsSandbox = 100
        maxResults = 500

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        PRODUCT = '30day'
        LABEL = 'prob'
        RESOURCE = 'tweets/search/%s/:%s' % (PRODUCT, LABEL)

        q = "%s %s OR %s %s OR %s %s" % (nameLower, symbolUpper, nameCapitalize, symbolUpper, nameUpper, symbolUpper)
        lang = "en"
        query = "lang:%s %s" % (lang, q)
        PARAMS = {'query':query, 'maxResults':maxResultsSandbox, 'fromDate':since, 'toDate':until}

        # Get the tweets from twitter
        r = Twitter.api.request(RESOURCE, PARAMS)

        # Get the response as a JSON object.
        rJson = TwitterResponse(r, False).json()
        #self.printDict(rJson)

        next = None
        next = rJson['next']

        tweetsList = []
        idSet = set()
        countTweets = 0

        for item in r.get_iterator():
            if 'text' in item:
                item['text'] = item['text'].replace("\n", " ")
                countTweets += 1
                tweetsList.append(item)
                idSet.add(item['id_str'])
                #print("%d) %s \nid: %s \ncreated_at: %s" % (countTweets, item['text'], item['id_str'], item['created_at']))
            elif 'message' in item :
               print ('ERROR message: %s, code:(%d).' % (item['message'], item['code']))
               return False

        print("%d tweets received." % (countTweets))
        print("%d tweets is uniqe." % (len(idSet)))

        if next:
            nextRequest = "%s, {'query':%s, 'maxResults':%s, 'fromDate':%s, 'toDate':%s, 'next':%s}" % (RESOURCE, query, maxResults, since, until, next)

        results = [tweetsList, nextRequest]
        return results


    def getTweetsStandard7Days(self, id, date):
        #print("--- In getTweetsStandard7Days function ---")

        # Get name & symbol
        stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol
        if stockNameSymbol == False:
            print("--- MyError: getTweets is faild in getNameAndSymbolOfStock().")
            return False
        name = stockNameSymbol[0]
        symbol = stockNameSymbol[1]

        # Preparing the parameters for the request
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        symbolLower = symbol.lower()
        symbolCapitalize = symbol.capitalize()
        symbolUpper = symbol.upper()

        resultType = 'mixed' # (mixed, recent, popular) is options
        
        count = 100
        maxResultsSandbox = 100
        maxResults = 500

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        since = str(since)
        until = str(until)

        RESOURCE = 'search/tweets'

        notQ = self.getNotQForId(id)
        #q = "%s %s OR %s %s OR %s %s" % (nameLower, symbolUpper, nameCapitalize, symbolUpper, nameUpper, symbolUpper)
        #q = "%s $%s OR %s $%s OR %s $%s" % (nameLower, symbolLower, nameCapitalize, symbolUpper, nameUpper, symbolUpper)
        q = "%s $%s %s" % (nameLower, symbolLower, notQ)
        lang = "en"
        query = "lang:%s %s" % (lang, q)
        PARAMS = {'q':q, 'count':count, 'lang':lang, 'result_type':resultType, 'since':since, 'until':until}

        # Get the tweets from twitter
        r = TwitterPager(Twitter.api, RESOURCE, PARAMS)

        tweetsList = []
        idSet = set()
        countTweets = 0

        for item in r.get_iterator(wait=0): #wait=5 for 180 call per 15 minutes
            if 'text' in item:
                # Replace all new line with spaces
                item['text'] = item['text'].replace("\n", " ")

                countTweets += 1
                tweetsList.append(item)
                idSet.add(item['id_str'])

                #print("%d) %s \n\tid: %s \n\tcreated_at: %s" % (countTweets, item['text'], item['id_str'], item['created_at']))
                if countTweets >= 1000: 
                    break
            elif 'message' in item :
               print ('ERROR message: %s, code:(%d).' % (item['message'], item['code']))
               return False


        print("--- In getTweetsStandard7Days() \n\t%d tweets received \n\t%d uniqe(id)" % (countTweets, len(idSet)))

        results = [tweetsList, "%s, PARAMS: %s" % (RESOURCE, PARAMS)]
        return results


    def GetTweets2(self, id, date):
        #print("--- In searchTweets function ---")

        stockNameSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) # [0]=name, [1]=symbol

        name = stockNameSymbol[0]
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        symbol = stockNameSymbol[1]
        symbolLower = symbol.lower()
        symbolCapitalize = symbol.capitalize()
        symbolUpper = symbol.upper()

        term = "%s %s OR %s %s OR %s %s" % (nameLower, symbolUpper, nameCapitalize, symbolUpper, nameUpper, symbolUpper)

        lang = "en"
        resultType = "mixed" # mixed / recent / popular
        count = 600

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        # Get tweets from Twitter
        try:
            # Get statuses
            statuses = Twitter.apiOfTwitter.GetSearch(term=term, until=until, since=since, count=count, lang=lang, result_type=resultType)

            idSet = set()
            for tweet in statuses:
                idSet.add(tweet['id_str'])

            print("%d Tweets returned!" % (countTweets))
            print("%d Tweets is uniqe!" % (len(idSet)))
            return statuses
        except BaseException as exception:
            print("--- Exception: ", exception)
            return False


    def GetTweets1(self, query):
        #print("--- In search function ---")
        if query == None:
            print("The function Search() received an empty parameter")
        elif query != None:
            # Get statuses
            statuses = Twitter.apiOfTwitter.GetSearch(raw_query= query)

            print(len(statuses), " Statuses returned!")
            print(type(statuses))
            print(statuses)

            print(type(statuses[0]))
            print(statuses[0])

            return statuses


    def getNotQForId(self, currentId):
        notQ = ""
        allID = DBManager.DBManager().getAllStocksID()
        for id in allID:
            if id[0] != currentId:
                stockNameAndSymbol = DBManager.DBManager().getNameAndSymbolOfStock(id) #[0]=name, [1]=symbol
                name = stockNameAndSymbol[0].replace(" ", "")
                symbol = stockNameAndSymbol[1].replace(" ", "")
                notQ += "-" + name + " -" + symbol + " "
        return notQ


    def getMinTweetsInDay(self, date, besidesID=None):
        allStocksID = DBManager.DBManager().getAllStocksID()
        if allStocksID:
            min = Twitter.threshold
            idOfMin = None

            for stockID in allStocksID:
                id = stockID[0]

                if besidesID != None and id in besidesID:
                    continue

                currentCount = DBManager.DBManager().getCountTweetsOfStockInDay(id, date)
                if currentCount == False & currentCount != 0:
                    return False

                if currentCount <= min:
                    min = currentCount
                    idOfMin = id
            
            if min != Twitter.threshold + 501:
                minTuple = (min, idOfMin)
                return minTuple
            else:
                return False
        else:
            return False


    def verifyCredentials(self):
        #print("--- In verifyCredentials function ---")
        res = Twitter.apiOfTwitter.VerifyCredentials()
        return res


    def checkRateLimit(self):
        r = Twitter.api.request('application/rate_limit_status')

        rateLimitDict = r.json()
        x = 4
        if 'message' in rateLimitDict:
            print ('%s (%d)' % (item['message'], item['code']))
            return False
        else:
            return rateLimitDict


                      
    def checkRateLimitOld(self):
        #print("--- In checkRateLimitOld function ---")

        Twitter.apiOfTwitter.InitializeRateLimit()
        rate_limit = Twitter.apiOfTwitter.rate_limit
        rateLimitDict = (rate_limit).__dict__

        try:
            resources_dict = rateLimitDict['resources']
            search_dict = resources_dict['search']
            application_dict = resources_dict['application']
            print(json.dumps(search_dict, indent=4))
            print(json.dumps(application_dict, indent=4))
        except KeyError:
            print("--- MyError: In checkRateLimitOld function, The key is not found in the dictionary.")


    def writeToFile(self, data):
        desktopPath = "C:\\Users\\Gal Tzemach\\Desktop"

        # Open file
        fileToWrite = open(desktopPath + "\\" + str(datetime.datetime.now()) + ".txt", "a")

        # Write current date & time to file
        fileToWrite.write("\n" + (datetime.datetime.now()).strftime("%d/%m/%Y %H:%M:%S") + "\n")

        if data is dict:
            data = json.dumps(data, indent=4)

        # Write data to file
        fileToWrite.write(str(data))

        # Close file
        fileToWrite.close()


    def printDict(self, dict):
        print(json.dumps(dict, indent=4))
        return