import time
import datetime
from Twitter import Twitter
from DB import DBManager
from Watson import Watson
from PandasDatareader import PandasDatareader
from ClientServerNetwork import serverNetwork
from datetime import timedelta
from Prediction import prediction
from SendMessages import sendMessages


class Server():


    def __init__(self):
        # Runing Server for clients requests on new thread
        s = serverNetwork.serverNetwork()
        s.start()

        while True:
            ## Fill DB
            #self.fillDB()

            ## Do prediction
            #prediction.prediction()

            ## Send messages to client
            #sendMessages.sendMessages()

            # Sleep one day
            print("Server (of prediction) sleep until %s"%str(datetime.datetime.now() + timedelta(days=1)))
            time.sleep(86400) #86400 sec is a day

        # Close resources
        DBManager.DBManager().db.close()


    def fillDB(self):
        print("Start fill DB...")

        # Fill price history of stocks
        pandasDatareder = PandasDatareader.PandasDatareder()
        print("Price history was filled Successfully.")

        # Fill Tweets from Twitter
        twitter = Twitter.Twitter()
        print("Tweets was filled Successfully.")

        # Analyze Tweets and fill
        watson = Watson.Watson()
        print("Analyzed tweets was filled Successfully.")

        print("Adding new data to DB is finished and will resume tomorrow")


if __name__ == '__main__':
    Server()