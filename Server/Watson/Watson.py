import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions
from DB import DBManager


class Watson(object):
    
    natural_language_understanding = None # Creating in readWatsonKeysFromFile


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readWatsonKeysFromFile():
            self.whatToAnalyze()


    def readWatsonKeysFromFile(self):

        path = "C:\\Users\\Gal Tzemach\\Desktop\\watsonKeys.txt"
        # Open a file
        try:
            watsonKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("--- MyError: In readWatsonKeysFromFile function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = watsonKeysFile.read().splitlines()

        username = listOfKeys[0]
        password = listOfKeys[1]
        version = listOfKeys[2]

        # Close opened file
        watsonKeysFile.close()

        #Create natural_language_understanding object with the keys
        Watson.natural_language_understanding = NaturalLanguageUnderstandingV1(username=username, password=password, version=version)       
        return True


    def whatToAnalyze(self):
        # Receives (one) text and id of tweet for analysis,
        # if there is a tweet that has not yet been analyzed.
        textAndIds = DBManager.DBManager().getTextAndIdsOfTweetToAnalyze()

        while textAndIds:
            text = textAndIds[0]
            id = textAndIds[1]
            stockID = textAndIds[2]

            nameSymbol = DBManager.DBManager().getNameAndSymbolByID(stockID)
            name = nameSymbol[0]
            symbol = nameSymbol[1]

            # Send the text for analysis
            textAnalyzed = self.analyze(text, name, symbol)

            if textAnalyzed:
                DBManager.DBManager().addAnalyzeToTweet(textAnalyzed, id)

            # Receives...  again
            textAndIds = DBManager.DBManager().getTextAndIdsOfTweetToAnalyze()
        else:
            print("There is no text to analyze.")


    def analyze(self, text, name, symbol):

        if text == None or text == "":
            raise Exception("The function analyze() received an None or empty text parameter.")

        try:
            response = Watson.natural_language_understanding.analyze(
                            text = text,
                            features = Features(emotion=EmotionOptions(), sentiment=SentimentOptions()),
                            #language="en",
                            return_analyzed_text = False)
        except BaseException as e:
            print(e)
            response = str(e)
        else:
            print(json.dumps(response, indent=4))

        return response


    def analyzeWithTargets(self, text, name, symbol):

        if text == None or text == "":
            raise Exception("The function analyze() received an None or empty text parameter.")

        try: # With name and symbol targets
            response = Watson.natural_language_understanding.analyze(text = text,
                            features = Features(emotion=EmotionOptions(targets=[name, "$" + symbol]), 
                            sentiment=SentimentOptions(targets=[name, "$" + symbol])),
                            #language="en",
                            return_analyzed_text=True)
        except BaseException as e:
            print(e)
            try: # Just with name targets
                response = Watson.natural_language_understanding.analyze(text = text,
                            features = Features(emotion=EmotionOptions(targets=[name]), 
                            sentiment=SentimentOptions(targets=[name])),
                            #language="en",
                            return_analyzed_text=True)
            except BaseException as e:
                print(e)
                try: # Just with symbol targets
                    response = Watson.natural_language_understanding.analyze(text = text,
                            features = Features(emotion=EmotionOptions(targets=[symbol]), 
                            sentiment=SentimentOptions(targets=[symbol])),
                            #language="en",
                            return_analyzed_text=True)
                except BaseException as e:
                    print(e)    
                    try: # Without targets
                        response = Watson.natural_language_understanding.analyze(text = text,
                            features = Features(emotion=EmotionOptions(), 
                            sentiment=SentimentOptions()),
                            #language="en",
                            return_analyzed_text=True)
                    except BaseException as e:
                        print(e)   
                        return False

        print(json.dumps(response, indent=4))

        return response

