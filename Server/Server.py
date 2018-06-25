from Twitter import Twitter
from DB import DBManager
from Watson import Watson
from PandasDatareader import PandasDatareader
from Twitter import TestTwitterAPI
import ClassForTests
from ClientServerNetwork import serverNetwork
import sys

class Server():

    def __init__(self):

        #serverNetwork.serverNetwork()
        #twitter = Twitter.Twitter()
        #watson = Watson.Watson()
        #pandasDatareder = PandasDatareader.PandasDatareder()

        #TestTwitterAPI.TestTwitterAPI()
        ClassForTests.ClassForTests()

        DBManager.DBManager().db.close()


if __name__ == '__main__':
    Server()