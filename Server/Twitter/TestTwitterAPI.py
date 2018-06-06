import json
from TwitterAPI import TwitterAPI, TwitterPager, TwitterResponse


class TwitterAPIII:

    api = None # Initialized in function readTwitterKeysFromFile()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readTwitterKeysFromFile:
            self.startSearch()


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
        Twitter.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        return True


    def startSearch(self):
        PRODUCT = '30day'
        LABEL = 'prob'


        ##1 Standard search/tweets request
        #r = api.request('search/tweets',   {'q':'apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                                    'count':10, 
        #                                    'lang':'en', 
        #                                    'result_type':'mixed',
        #                                    'since':'2018-06-02',
        #                                    'until':'2018-06-03'})

        ### Quota information in the REST-only response header.
        ##q = TwitterResponse(r, False).get_quota()
        ##print("Quota:\n", json.dumps(q, indent=4))

        ### Dictionary of API response header contents.
        ##h = TwitterResponse(r, False).headers
        ##print("header:\n", json.dumps(dict(h), indent=4))

        ## Get the response as a JSON object.
        #j = TwitterResponse(r, False).json()
        ##print("json:\n", json.dumps(j, indent=4))
        #searchMetaData = j['search_metadata']
        #print("searchMetaData:\n", json.dumps(searchMetaData, indent=4))

        ### HTTP response status code.
        ##s = TwitterResponse(r, False).status_code
        ##print("status code:\n", json.dumps(s, indent=4))

        ### Raw API response text.
        ##t = TwitterResponse(r, False).text
        ##print("text:\n", json.dumps(json.loads(t), indent=4))

        #countTweets = 0
        #for item in r.get_iterator():
        #    if 'text' in item:
        #        countTweets += 1
        #        text = item['text']
        #        cleanText = (item['text']).replace("\n", " ")
        #        print(str(countTweets) + ")" , cleanText + "\t(" + item['user']['screen_name'] + ")\t" + item['id_str'])
        #    elif 'message' in item:
        #        print('%s (%d)' % (item['message'], item['code']))

        #if True:
        #    pass


        ##1.1 Standard search/tweets request with max_id for pageing
        #r = api.request('search/tweets',   {'q':'apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                                    'count':10, 
        #                                    'lang':'en', 
        #                                    'result_type':'mixed',
        #                                    'since':'2018-06-02',
        #                                    'until':'2018-06-03'})

        ### Quota information in the REST-only response header.
        ##q = TwitterResponse(r, False).get_quota()
        ##print("Quota:\n", json.dumps(q, indent=4))

        ### Dictionary of API response header contents.
        ##h = TwitterResponse(r, False).headers
        ##print("header:\n", json.dumps(dict(h), indent=4))

        ## Get the response as a JSON object.
        #j = TwitterResponse(r, False).json()
        #print("json:\n", json.dumps(j, indent=4))
        #searchMetaData = j['search_metadata']
        #print("searchMetaData:\n", json.dumps(searchMetaData, indent=4))
        #maxID = searchMetaData['max_id_str']

        ### HTTP response status code.
        ##s = TwitterResponse(r, False).status_code
        ##print("status code:\n", json.dumps(s, indent=4))

        ### Raw API response text.
        ##t = TwitterResponse(r, False).text
        ##print("text:\n", json.dumps(json.loads(t), indent=4))

        #countTweets = 0
        #for item in r.get_iterator():
        #    if 'text' in item:
        #        countTweets += 1
        #        text = item['text']
        #        cleanText = (item['text']).replace("\n", " ")
        #        print(str(countTweets) + ")" , cleanText + "\t(" + item['user']['screen_name'] + ")\t" + item['id_str'])
        #    elif 'message' in item:
        #        print('%s (%d)' % (item['message'], item['code']))


        #l = len(j['statuses'])
        #while l > 0:
        #    r = api.request('search/tweets',   {'q':'apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                                        'count':10, 
        #                                        'lang':'en', 
        #                                        'result_type':'mixed',
        #                                        'since':'2018-06-02',
        #                                        'until':'2018-06-03',
        #                                        'max_id':maxID})

        #    # Get the response as a JSON object.
        #    j = TwitterResponse(r, False).json()
        #    print("json:\n", json.dumps(j, indent=4))
        #    searchMetaData = j['search_metadata']
        #    print("searchMetaData:\n", json.dumps(searchMetaData, indent=4))
        #    maxID = searchMetaData['max_id_str']

        #    l = len(j['statuses'])

        #    for item in r.get_iterator():
        #        if 'text' in item:
        #            countTweets += 1
        #            text = item['text']
        #            cleanText = (item['text']).replace("\n", " ")
        #            print(str(countTweets) + ")" , cleanText + "\t(" + item['user']['screen_name'] + ")\t" + item['id_str'])
        #        elif 'message' in item:
        #            print('%s (%d)' % (item['message'], item['code']))


        #if True:
        #    pass


        ##2 Standard search/tweets pager
        #r = TwitterPager(api, 'search/tweets', {'q':'apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                                        'count':100, 
        #                                        'lang':'en', 
        #                                        'result_type':'mixed',
        #                                        'since':'2018-06-02',
        #                                        'until':'2018-06-03'})

        #countTweets = 0
        #tweetsIDSet = set()
        #for item in r.get_iterator(wait=5):
        #    if 'text' in item:
        #        countTweets += 1
        #        tweetsIDSet.add(item['id_str'])
        #        print (str(countTweets) + ")" , item['text'], item['id_str'], item['created_at'])
        #        print(len(tweetsIDSet), "tweets are uniqe.")
        #    elif 'message' in item and item['code'] == 88:
        #        print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        #        break
        #    elif 'message' in item :
        #       print ('%s (%d)' % (item['message'], item['code']))
        #       break



        ##3 Sandbob request
        #r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        #                 {'query':'lang:en apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                    'maxResults':100, 
        #                    'fromDate':'201806020000',
        #                    'toDate':'201806030000'})

        ### Quota information in the REST-only response header.
        ##q = TwitterResponse(r, False).get_quota()
        ##print("Quota:\n", json.dumps(q, indent=4))

        ### Dictionary of API response header contents.
        ##h = TwitterResponse(r, False).headers
        ##print("header:\n", json.dumps(dict(h), indent=4))

        ## Get the response as a JSON object.
        #j = TwitterResponse(r, False).json()
        ##print("json:\n", json.dumps(j, indent=4))

        #next = None
        #next = j['next']
        #print("next: \n", next)

        ### HTTP response status code.
        ##s = TwitterResponse(r, False).status_code
        ##print("status code:\n", json.dumps(s, indent=4))

        ### Raw API response text.
        ##t = TwitterResponse(r, False).text
        ##print("text:\n", json.dumps(json.loads(t), indent=4))

        #listOfTweets = []
        #tweetsIDSet = set()
        #countTweets = 0
        #for item in r.get_iterator():
        #    if 'text' in item:
        #        countTweets += 1
        #        listOfTweets.append(item)
        #        tweetsIDSet.add(item['id_str'])
        #        print (str(countTweets) + ")" , item['text'], item['id_str'], item['created_at'])
        #        print(len(tweetsIDSet), "tweets are uniqe.")
        #        print(len(listOfTweets), "tweets in listOfTweets.")
        #    elif 'message' in item and item['code'] == 88:
        #        print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        #        break
        #    elif 'message' in item :
        #       print ('%s (%d)' % (item['message'], item['code']))
        #       break

        #if next:
        #    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        #                     {'query':'lang:en apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                        'maxResults':100, 
        #                        'fromDate':'201806020000',
        #                        'toDate':'201806030000',
        #                        'next':next})

        #    # Get the response as a JSON object.
        #    j = TwitterResponse(r, False).json()
        #    #print("json:\n", json.dumps(j, indent=4))

        #    next = None
        #    next = j['next']
        #    print("next: \n", next)

        #    listOfTweets.append("Gal")

        #    for item in r.get_iterator():
        #        if 'text' in item:
        #            countTweets += 1
        #            listOfTweets.append(item)
        #            tweetsIDSet.add(item['id_str'])
        #            print (str(countTweets) + ")" , item['text'], item['id_str'], item['created_at'])
        #            print(len(tweetsIDSet), "tweets are uniqe.")
        #            print(len(listOfTweets), "tweets in listOfTweets.")
        #        elif 'message' in item and item['code'] == 88:
        #            print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        #            break
        #        elif 'message' in item :
        #           print ('%s (%d)' % (item['message'], item['code']))
        #           break


        #    if next:
        #        r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        #                         {'query':'lang:en apple AAPL OR Apple AAPL OR APPLE AAPL', 
        #                            'maxResults':100, 
        #                            'fromDate':'201806020000',
        #                            'toDate':'201806030000',
        #                            'next':next})

        #        # Get the response as a JSON object.
        #        j = TwitterResponse(r, False).json()
        #        #print("json:\n", json.dumps(j, indent=4))

        #        next = None
        #        next = j['next']
        #        print("next: \n", next)

        #        listOfTweets.append("Gal")

        #        for item in r.get_iterator():
        #            if 'text' in item:
        #                countTweets += 1
        #                listOfTweets.append(item)
        #                tweetsIDSet.add(item['id_str'])
        #                print (str(countTweets) + ")" , item['text'], item['id_str'], item['created_at'])
        #                print(len(tweetsIDSet), "tweets are uniqe.")
        #                print(len(listOfTweets), "tweets in listOfTweets.")
        #            elif 'message' in item and item['code'] == 88:
        #                print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        #                break
        #            elif 'message' in item :
        #               print ('%s (%d)' % (item['message'], item['code']))
        #               break

        ##4 Sandbob pager
        #r = TwitterPager(api, 'tweets/search/%s/:%s' % (PRODUCT, LABEL), 
        #                 {'query':'lang:en apple AAPL OR lang:en Apple AAPL OR lang:en APPLE AAPL', 
        #                    'maxResults':100, 
        #                    'fromDate':'201806020000',
        #                    'toDate':'201806030000'})

        #countTweets = 0
        #tweetsIDSet = set()
        #for item in r.get_iterator(wait=5):
        #    if 'text' in item:
        #        countTweets += 1
        #        tweetsIDSet.add(item['id_str'])
        #        print (str(countTweets) + ")" , item['text'], item['id_str'], item['created_at'])
        #        print(len(tweetsIDSet), "tweets are uniqe.")
        #    elif 'message' in item and item['code'] == 88:
        #        print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        #        break
        #    elif 'message' in item :
        #       print ('%s (%d)' % (item['message'], item['code']))
        #       break