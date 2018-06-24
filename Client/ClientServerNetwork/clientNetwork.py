import socket
from ClientServerNetwork import vocabulary
import Singleton
import pickle
from math import ceil
import sys

class clientNetwork(metaclass=Singleton.Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # create a socket object
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        host = socket.gethostname()                           

        port = 9999

        # connection to hostname on the port.
        self.s.connect((host, port))                               


    def signUp(self, arg):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.SIGNUP))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(arg))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.OK:
            print("User successfully signup.")
            return True
        elif response == vocabulary.USER_EXIST:
            print("Email already exists, try with another email address.")
            return "Email already exists, try with another email address."


        
    def getAllStocks(self):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_ALL_STOCKS))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("getAllStocks is failed.")
            return False

        packets = []
        for i in range(ceil(sizeOrError / vocabulary.BUFSIZE)):
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   

        data =  pickle.loads(b"".join(packets))

        return data



    def signIn(self, arg):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.SIGNIN))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(arg))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.OK:
            print("User successfully signin.")
            return True
        elif response == vocabulary.SIGNIN_FAIL:
            print("Signin failed, Try again.")
            return "Signin failed, Try again."


    def exit(self):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.EXIT))
    
        self.s.close()

    def setIsConnect(self, arg):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.SET_IS_CONNECT))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(arg))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.OK:
            print("Set is connect to false is successfully.")
            return True
        elif response == vocabulary.SET_IS_CONNECT_FAIL:
            print("Set is connect to false is failed.")
            return "Set is connect to false is failed."


    def getIDByEmail(self, email):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_ID_BY_EMAIL))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(email))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.ERROR:
            print("Get ID by email is faild")
            return False
        else: 
            print("Get ID by email is successfully")
            return response


    def getFullNameByID(self, ID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_FULL_NAME_BY_ID))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(ID))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.ERROR:
            print("Get full name by ID is faild")
            return False
        else: 
            print("Get full name by ID is successfully")
            return response


    def getExplanationBysymbol(self, symbol):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_EXPLANATION_BY_SYMBOL))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(symbol))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.ERROR:
            print("Get explanation by symbol is faild")
            return False
        else: 
            print("Get explanation by symbol is successfully")
            return response


    def getStockIDBySymbol(self, symbol):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_STOCKID_BY_SYMBOL))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(symbol))

        # Get response
        response = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if response == vocabulary.ERROR:
            print("Get stockID by symbol is faild")
            return False
        else: 
            print("Get stockID by symbol is successfully")
            return response


    #def getAllTweetsByStockID(self, stockID):
    #    # Sending the type of requst
    #    self.s.send(pickle.dumps(vocabulary.GET_ALL_TWEETS_BY_STOCKID))

    #    # Sending the relevant arguments of request
    #    self.s.send(pickle.dumps(stockID))

    #    # Get response
    #    sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

    #    if sizeOrError == vocabulary.ERROR:
    #        print("getAllTweetsByStockID is failed.")
    #        return False

    #    print(sizeOrError, sizeOrError / vocabulary.BUFSIZE, ceil(sizeOrError / vocabulary.BUFSIZE))

    #    packets = []
    #    for i in range(ceil(sizeOrError / vocabulary.BUFSIZE)):
    #        packet = self.s.recv(vocabulary.BUFSIZE)
    #        packets.append(packet)   

    #        print("%d) \n %d"%(i, sys.getsizeof(packet)))

    #    print(sys.getsizeof(b"".join(packets)))
    #    data =  pickle.loads(b"".join(packets))
    #    print(sys.getsizeof(data))

    #    return data



    def getAllTweetsByStockID(self, stockID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_ALL_TWEETS_BY_STOCKID))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(stockID))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("getAllTweetsByStockID is failed or empty.")
            return False

        print(sizeOrError)

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass


    def getMyStocksIDs(self, ID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_MY_STOCKS_IDS))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(ID))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("getMyStocks is failed or empty.")
            return False

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass


    def getStockByID(self, stockID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_STOCK_BY_ID))

        # Sending the relevant arguments of request
        self.s.send(pickle.dumps(stockID))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("getStockByID is failed or empty.")
            return False

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass


    def getAllStocksIDs(self):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.GET_ALL_STOCKS_IDS))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("getAllStocksIDs is failed or empty.")
            return False

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass


    def deleteStockByIDs(self, userID, stockID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.DELETE_STOCK_BY_IDS))

        # Sending the relevant arguments of request
        arg = (userID, stockID)
        self.s.send(pickle.dumps(arg))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("deleteStockByIDs is failed.")
            return False

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass

    def addStockToUser(self, userID, stockID):
        # Sending the type of requst
        self.s.send(pickle.dumps(vocabulary.ADD_STOCK_TO_USER))

        # Sending the relevant arguments of request
        arg = (userID, stockID)
        self.s.send(pickle.dumps(arg))

        # Get response
        sizeOrError = pickle.loads(self.s.recv(vocabulary.BUFSIZE))

        if sizeOrError == vocabulary.ERROR:
            print("addStockToUser is failed.")
            return False

        packets = []
        while True:
            packet = self.s.recv(vocabulary.BUFSIZE)
            packets.append(packet)   
            try:
                data =  pickle.loads(b"".join(packets))
                return data
            except:
                pass