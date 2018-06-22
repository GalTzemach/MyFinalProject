from Twitter import Twitter
from DB import DBManager
from Watson import Watson
from PandasDatareader import PandasDatareader
from Twitter import TestTwitterAPI
import ClassForTests
from ClientServerNetwork import serverNetwork

class Server():

    def __init__(self):
        serverNetwork.serverNetwork()

        #twitter = Twitter.Twitter()
        #managerDB = DBManager.DBManager()
        #watson = Watson.Watson()
        #pandasDatareder = PandasDatareader.PandasDatareder()
        #TestTwitterAPI.TestTwitterAPI()
        #ClassForTests.ClassForTests()


if __name__ == '__main__':
    Server()