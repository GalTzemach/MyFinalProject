import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions
from DB import DBManager


class Watson(object):
    """description of class"""
    
    natural_language_understanding = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readWatsonKeysFromFile():

            #self.whatToAnalyze()
            pass

    def readWatsonKeysFromFile(self):
        print("--- In readWatsonKeysFromFile function ---")
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
        textOfTweet = DBManager.DBManager().getTextOfTweetToAnalyze()
        while textOfTweet:
            text = textOfTweet[0]
            textAnalyzed = self.analyze(text)
            if textAnalyzed:
                DBManager.DBManager().addAnalyzeToTweet(textAnalyzed, textOfTweet[1])

            textOfTweet = DBManager.DBManager().getTextOfTweetToAnalyze()
        else:
            print("--- MyPrint: There is no text to analyze.")



    def analyze(self, text):
        print("--- In analyze function ---")

        if text == None:
            print("The function analyze() received an empty parameter")
        elif text != None:
            response = Watson.natural_language_understanding.analyze(
            text = text,
            features=Features(
            emotion=EmotionOptions(),
            sentiment=SentimentOptions()),
            #language="en",
            return_analyzed_text=True)

            #print(json.dumps(response, indent=4))

            return response





