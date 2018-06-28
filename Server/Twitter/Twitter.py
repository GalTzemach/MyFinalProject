import twitter
import json
import datetime
from DB import DBManager
from TwitterAPI import TwitterAPI, TwitterPager, TwitterResponse
import pause 

class Twitter:

    apiOfTwitter = None # Initialized in function readTwitterKeysFromFile()
    twitterApi = None # Initialized in function readTwitterKeysFromFile()

    thresholdTweets = 1000 
    maxTweets = 1000 
    daysAgo = 2#11
    waite = 0 #5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readTwitterKeysFromFile():

            ## Verify Credentials
            #user = self.getverifyCredentials()

            # Start to search tweets 
            self.whatToSearch()


    def readTwitterKeysFromFile(self):

        # Path for keys
        # Standard keys
        #path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterKeys.txt"
        # Sandbox key
        path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterSandboxKeys.txt"

        # Open a file
        try:
            twitterKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("MyError: In readTwitterKeysFromFile function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = twitterKeysFile.read().splitlines()

        consumer_key = listOfKeys[0]
        consumer_secret = listOfKeys[1]
        access_token_key = listOfKeys[2]
        access_token_secret = listOfKeys[3]

        # Close opened file
        twitterKeysFile.close()

        #Create apiOfTwitter and twitterApi object with the keys
        Twitter.apiOfTwitter = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret, sleep_on_rate_limit=True)
        Twitter.twitterApi = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        return True


    def whatToSearch(self):
        # Get last date of tweets that has already been filled 
        lastDate = DBManager.DBManager().getLastTweetsDate()[0]

        # Get today and yesterday date
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)

        if lastDate.date() < yesterday.date():
            fromDate = lastDate
        else:
            print("The latest tweets are already in DB.")
            return
        #fromDate = today - datetime.timedelta(days = Twitter.days) 

        while fromDate < today:
            # Set of ID to ignore them in this date
            besidesIDSet = set()

            # Get min tweet (count and id)
            minTuple = self.getMinTweetCountAndIDByDay(fromDate) # [0]= count, [1]=id
            if minTuple == False:
                print("MyError: whatToSearch is faild in getMinTweetsInDay().")
                return False
            minCount = minTuple[0]
            minID = minTuple[1]

            while minCount < self.thresholdTweets:
                # Get name and symbol of tweet by ID
                stockNameSymbol = DBManager.DBManager().getNameAndSymbolByID(minID) # [0]=name, [1]=symbol
                if stockNameSymbol == False:
                    print("MyError: whatToSearch is faild in getNameAndSymbolByID().")
                    return False
                name = stockNameSymbol[0]
                symbol = stockNameSymbol[1]

                # Print search details 
                print("\n Search for Date: %s, for \"%s\" stock (symbol:%s, id:%d):" % (fromDate.date(), name, symbol, minID))

                try:
                    # Get/Search tweets from Twitter by API
                    results = self.getTweetsStandard7Days(minID, fromDate)
                    #results = self.getTweetsSandbox30Days(id, dateToSearch)

                except BaseException as exception:
                    if 'status_code' in exception.__dict__ and exception.status_code == 429: # Is a rate limit exception
                        print("Exception: %s %s" % (exception.__class__, exception))

                        # Get rate limit details
                        rateLimitDict = self.getRateLimit()

                        # Get reset time
                        # Get reset time for /search/tweets endpoint
                        reset = rateLimitDict['resources']['search']['/search/tweets']['reset']
                        ## Get reset time for /tweets/search/:product/:label endpoint
                        #reset = rateLimitDict['resources']['tweets']['/tweets/search/:product/:label']['reset']

                        # Safety coefficient
                        reset += 10 

                        # Create datetime object from reset
                        resetDatetime = datetime.datetime.fromtimestamp(reset)

                        # Sleep until the endpoint is reset
                        print("\n\n Sleep for rate limit until %s (%s)\n\n" % (resetDatetime, reset))
                        pause.until(reset) 
                          
                        # Get/Search tweets again
                        results = self.getTweetsStandard7Days(minID, fromDate)
                        #results = self.getTweetsSandbox30Days(id, dateToSearch)

                    else: # Is no rate limit exception
                        print("Exception: %s %s" % (exception.__class__, exception))
                        return False
                
                if results == False:
                    print("MyError: whatToSearch is faild in getTweets...().")
                    return False

                tweets = results[0]
                nextRequest = results[1]

                countTweets = 0
                notInsertedCount = 0
                setOfText = set()
                setOfID = set()

                for tweet in tweets:
                    countTweets += 1

                    # Add tweet ID/text to sets
                    setOfID.add(tweet['id_str'])
                    setOfText.add(tweet['full_text'])

                    # Add tweet to database
                    if DBManager.DBManager().addTweet(minID, tweet, nextRequest) != True:
                        notInsertedCount += 1


                uniqeIDCount = len(setOfID)
                uniqeTextCount = len(setOfText)
                insertedCount = countTweets - notInsertedCount

                print("In whatToSearch(): \n\t%d tweets received" % (countTweets))
                if countTweets > 0:
                    print("\t%d is uniqe(id), %d is uniqe(text)" % (uniqeIDCount, uniqeTextCount))
                    print("\t%d tweets inserted to DB." % (insertedCount))

                    if insertedCount == 0: 
                        besidesIDSet.add(minID)
                    elif insertedCount < uniqeIDCount: 
                        print("\tNot all unique(id) tweets has been inserted to DB.")
                    elif insertedCount == uniqeIDCount:
                        print("\tAll unique(id) tweets of stock %s (%s) for date %s have been inserted to DB!" % (name, symbol, fromDate.date()))
                        besidesIDSet.add(minID)
                else:
                    besidesIDSet.add(minID)

                minTuple = self.getMinTweetCountAndIDByDay(fromDate, besidesIDSet) # [0]= count, [1]=id
                if minTuple != False:
                    minCount = minTuple[0]
                    minID = minTuple[1]
                else:
                    print("MyError: whatToSearch is faild in getMinTweetsInDay().")
                    return False

            fromDate = fromDate + datetime.timedelta(days=1) # Add days to date


    def getTweetsStandard7Days(self, id, date):

        # Get name & symbol
        nameSymbol = DBManager.DBManager().getNameAndSymbolByID(id) # [0]=name, [1]=symbol
        if nameSymbol == False:
            print("MyError: getTweets is faild in getNameAndSymbolByID().")
            return False
        name = nameSymbol[0]
        symbol = nameSymbol[1]

        # Preparing the parameters for the request
        nameLower = name.lower()
        nameCapitalize = name.capitalize()
        nameUpper = name.upper()

        symbolLower = symbol.lower()
        symbolCapitalize = symbol.capitalize()
        symbolUpper = symbol.upper()

        resultType = 'mixed' # (mixed, recent, popular) is options
        
        count = 100

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date()
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        since = str(since)
        until = str(until)

        lang = "en"

        #notQ = self.getNotQByID(id)
        #q = "%s $%s %s" % (nameLower, symbolLower, notQ)
        q = "%s $%s" % (nameLower, symbolLower)
        query = "lang:%s %s" % (lang, q)


        RESOURCE = 'search/tweets'
        PARAMS = {'q':q, 'count':count, 'lang':lang, 'result_type':resultType, 'since':since, 'until':until,'tweet_mode':'extended'}

        # Get the tweets from twitter
        r = TwitterPager(Twitter.twitterApi, RESOURCE, PARAMS)

        tweetsList = []
        idSet = set()
        countTweets = 0

        for item in r.get_iterator(wait = Twitter.waite): # 5 for 180 call per 15 minutes
            if 'full_text' in item:
                # Get text from tweet without new lines
                text = item['full_text'].replace("\n", " ")

                countTweets += 1

                tweetsList.append(item)

                idSet.add(item['id_str'])

                # Print tweet number, text, id, created_at
                print("%d) %s \n\tid: %s\n\tcreated_at: %s" % (countTweets, text, item['id_str'], item['created_at']))
                if countTweets >= Twitter.maxTweets: 
                    break
            elif 'message' in item :
               print ('ERROR message: %s, code:(%d).' % (item['message'], item['code']))
               return False


        print("In getTweetsStandard7Days(): \n\t%d tweets received" % (countTweets))
        if countTweets > 0:
            print("\t%d uniqe(id)" % (len(idSet)))

        results = [tweetsList, "%s, PARAMS: %s" % (RESOURCE, PARAMS)]
        return results


    def getTweetsPremium30Days(self, id, date):

        # Get name & symbol
        stockNameSymbol = DBManager.DBManager().getNameAndSymbolByID(id) # [0]=name, [1]=symbol
        if stockNameSymbol == False:
            print("MyError: getTweets is faild in getNameAndSymbolByID().")
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
        r = Twitter.twitterApi.request(RESOURCE, PARAMS)

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

        # Get name & symbol
        stockNameSymbol = DBManager.DBManager().getNameAndSymbolByID(id) # [0]=name, [1]=symbol
        if stockNameSymbol == False:
            print("MyError: getTweets is faild in getNameAndSymbolByID().")
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

        maxResultsSandbox = 100

        if date.date() == datetime.datetime.now().date():
            since = (date - datetime.timedelta(days=1)).date
            until = date.date()
        elif date.date() <= datetime.datetime.now().date():
            since = date.date()
            until = (date + datetime.timedelta(days=1)).date()

        since = datetime.datetime.combine(since, datetime.datetime.min.time()).strftime("%Y%m%d%H%M")
        #since = since.strftime("%Y%m%d%H%M")
        until = datetime.datetime.combine(until, datetime.datetime.min.time()).strftime("%Y%m%d%H%M")
        #until = until.strftime("%Y%m%d%H%M")


        PRODUCT = '30day'
        LABEL = 'prob'
        RESOURCE = 'tweets/search/%s/:%s' % (PRODUCT, LABEL)

        notQ = self.getNotQByID(id)
        #q = "%s %s OR %s %s OR %s %s" % (nameLower, symbolUpper, nameCapitalize, symbolUpper, nameUpper, symbolUpper)
        q = "%s %s #%s %s" % (nameLower, symbolLower, symbolLower, notQ)
        lang = "en"
        query = "lang:%s %s" % (lang, q)
        PARAMS = {'query':query, 'maxResults':maxResultsSandbox, 'fromDate':since, 'toDate':until}

        # Get the tweets from twitter
        r = Twitter.twitterApi.request(RESOURCE, PARAMS)

        # Get the response as a JSON object.
        rJson = TwitterResponse(r, False).json()

        next = None
        if 'next' in rJson:
            next = rJson['next']

        tweetsList = []
        idSet = set()
        countTweets = 0

        try:
            for item in r.get_iterator():
                if 'text' in item:
                    if item['truncated'] == True:
                        item['extended_tweet']['full_text'] = item['extended_tweet']['full_text'].replace("\n", " ")
                        text = item['extended_tweet']['full_text']
                    else:
                        # Replace all new line with spaces
                        item['text'] = item['text'].replace("\n", " ")
                        text = item['text']

                    countTweets += 1
                    tweetsList.append(item)
                    idSet.add(item['id_str'])

                    print("%d) %s \n\tid: %s \n\tcreated_at: %s" % (countTweets, text, item['id_str'], item['created_at']))
                elif 'message' in item :
                   print ('ERROR message: %s, code:(%d).' % (item['message'], item['code']))
                   return False
        except BaseException as exception:
            print("Exception: %s" % (exception))
            return False

        print("In getTweetsSandbox30Days() \n\t%d tweets received \n\t%d uniqe(id)" % (countTweets, len(idSet)))

        if next:
            nextRequest = "%s, {'query':%s, 'maxResults':%s, 'fromDate':%s, 'toDate':%s, 'next':%s}" % (RESOURCE, query, maxResultsSandbox, since, until, next)
        else:
            nextRequest = "%s, {'query':%s, 'maxResults':%s, 'fromDate':%s, 'toDate':%s, 'next':%s}" % (RESOURCE, query, maxResultsSandbox, since, until, None)


        results = [tweetsList, nextRequest]
        return results


    def getNotQByID(self, currentId):
        notQ = ""
        allID = DBManager.DBManager().getAllStocksIDs()
        for id in allID:
            if id[0] != currentId:
                stockNameAndSymbol = DBManager.DBManager().getNameAndSymbolByID(id) #[0]=name, [1]=symbol
                name = stockNameAndSymbol[0].replace(" ", "")
                symbol = stockNameAndSymbol[1].replace(" ", "")
                notQ += "-" + name + " -" + symbol + " "
        return notQ


    def getMinTweetCountAndIDByDay(self, date, besidesID=None):
        allStocksID = DBManager.DBManager().getAllStocksIDs()
        if allStocksID:
            min = Twitter.thresholdTweets
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
            
            if min != Twitter.thresholdTweets + 501:
                minTuple = (min, idOfMin)
                return minTuple
            else:
                return False
        else:
            return False


    def getverifyCredentials(self):
        res = Twitter.apiOfTwitter.getverifyCredentials()
        return res


    def getRateLimit(self):
        r = Twitter.twitterApi.request('application/rate_limit_status')

        rateLimitDict = r.json()
        if 'message' in rateLimitDict:
            print ('%s (%d)' % (item['message'], item['code']))
            return False
        else:
            return rateLimitDict


    def writeToFile(self, data):
        desktopPath = "C:\\Users\\Gal Tzemach\\Desktop"

        # Open file with current datetime name
        fileToWrite = open(desktopPath + "\\" + str(datetime.datetime.now()) + ".txt", "a")

        # Write current date & time to file
        fileToWrite.write("\n" + (datetime.datetime.now()).strftime("%d/%m/%Y %H:%M:%S") + "\n")

        if isinstance(data, dict):
            data = json.dumps(data, indent=4)

        # Write data to file
        fileToWrite.write(str(data))

        # Close file
        fileToWrite.close()


    def printDict(self, dict):
        print(json.dumps(dict, indent=4))
        return