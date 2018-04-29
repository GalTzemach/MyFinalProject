import twitter
import json

class Twitter:

    api = None # Initialized in function readTwitterKeysFromFile()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readTwitterKeysFromFile():

            # Check rate limit
            self.checkRateLimit()

            ## Verify Credentials
            #user = self.verifyCredentials()
            #self.printTwitterClass(user)

            ## Search tweets
            #statuses = self.search("q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL&result_type=mixed&count=100&lang=en")
            #self.printTwitterClass(statuses)

            for i in range(362):
                statuses = self.search("q=apple%20OR%20Apple%20OR%20APPLE%20%23%24AAPL&result_type=mixed&count=1")
                if i % 10 == 0:
                    self.checkRateLimit()


    def readTwitterKeysFromFile(self):
        print("--- In readTwitterKeysFromFile function ---")
        path = "C:\\Users\\Gal Tzemach\\Desktop\\twitterKeys.txt"
        # Open a file
        try:
            twitterKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("MY-ERROR: In readTwitterKeysFromFile function, File ", path, " not found.")
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
            statuses = Twitter.api.GetSearch(raw_query = query)
            print(len(statuses), " Statuses returned!")
            return statuses


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

            # Print text of tweet only
            text = (twitterClass)._json['text']
            print("text: ", text)

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
            print("MY-ERROR: In checkRateLimit function, The key is not found in the dictionary.")





                       


