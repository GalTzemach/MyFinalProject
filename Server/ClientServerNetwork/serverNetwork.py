import socket  
import threading
import Singleton
import datetime
import pickle
import sys
from ClientServerNetwork import vocabulary
from DB import DBManager, getXYForGraph


class serverNetwork(threading.Thread, metaclass=Singleton.Singleton):


    def __init__(self, **kwargs):
        threading.Thread.__init__(self)


    def run(self):
        # create a socket object
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        host = socket.gethostname()                           

        port = 9999                                           

        # bind to the port
        serversocket.bind((host, port))                                  

        # queue up to 5 requests
        serversocket.listen(5) 

        print("The server was set up in %s." % (datetime.datetime.now()))

        numThread = 1

        while True:
           # establish a connection (blocking)
           clientsocket,addr = serversocket.accept() 
           
           t = handleClient(numThread, clientsocket, addr)
           t.start()

           numThread += 1



class handleClient(threading.Thread):


    def __init__(self, numThread, clientsocket ,addr):
      threading.Thread.__init__(self)

      self.numThread = numThread
      self.clientsocket = clientsocket
      self.addr = addr


    def run(self):
        print("Got a connection from %s, Thread %d." % (str(self.addr), self.numThread))

        # Receiving requests
        while True:
            # Receiving the type of request
            recvType = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
            print("The server received from Thread %d a request of type: %s." % (self.numThread, recvType))

            if recvType == vocabulary.EXIT:
                break
            elif recvType == vocabulary.SIGNUP:
                self.signUp()
            elif recvType == vocabulary.SIGNIN:
                self.signIn()
            elif recvType == vocabulary.SET_IS_CONNECT:
                self.setIsConnect()
            elif recvType == vocabulary.GET_ALL_STOCKS:
                self.getAllStocks()
            elif recvType == vocabulary.GET_ID_BY_EMAIL:
                self.getIDByEmail()
            elif recvType == vocabulary.GET_FULL_NAME_BY_ID:
                self.getFullNameByID()
            elif recvType == vocabulary.GET_EXPLANATION_BY_SYMBOL:
                self.getExplanationBySymbol()
            elif recvType == vocabulary.GET_STOCKID_BY_SYMBOL:
                self.getStockIDBySymbol()
            elif recvType == vocabulary.GET_ALL_TWEETS_BY_STOCKID:
                self.getAllTweetsByStockID()
            elif recvType == vocabulary.GET_MY_STOCKS_IDS:
                self.getMyStocksIDs()
            elif recvType == vocabulary.GET_STOCK_BY_ID:
                self.getStockByID()
            elif recvType == vocabulary.GET_ALL_STOCKS_IDS:
                self.getAllStocksIDs()
            elif recvType == vocabulary.DELETE_STOCK_BY_IDS:
                self.deleteStockByIDs()
            elif recvType == vocabulary.ADD_STOCK_TO_USER:
                self.addStockToUser()
            elif recvType == vocabulary.GET_ALL_MESSAGES_BY_USER_ID:
                self.getAllMessagesByUserID()
            elif recvType == vocabulary.GET_XY_FOR_GRAPH:
                self.getXYForGraphByID()


    def signUp(self):
        # Receiving the arg of request
        recvArg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().addNewUser(recvArg[0], recvArg[1], recvArg[2], recvArg[3], recvArg[4])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.USER_EXIST))


    def signIn(self):
        # Receiving the arg of request
        recvArg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().signIn(recvArg[0], recvArg[1])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.SIGNIN_FAIL))


    def setIsConnect(self):
        # Receiving the arg of request
        recvArg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().setIsConnect(recvArg[0], recvArg[1])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.SET_IS_CONNECT_FAIL))


    def getAllStocks(self):
        respons = DBManager.DBManager().getAllStocks()

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getIDByEmail(self):
        # Receiving the arg of request
        email = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        respons = DBManager.DBManager().getIDByEmail(email)
        if respons:
            self.clientsocket.send(pickle.dumps(respons))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getFullNameByID(self):
        # Receiving the arg of request
        id = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        respons = DBManager.DBManager().getFullNameByID(id)
        if respons:
            self.clientsocket.send(pickle.dumps(respons))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getExplanationBySymbol(self):
        # Receiving the arg of request
        symbol = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        respons = DBManager.DBManager().getExplanationBySymbol(symbol)
        if respons:
            self.clientsocket.send(pickle.dumps(respons))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getStockIDBySymbol(self):
        # Receiving the arg of request
        symbol = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        respons = DBManager.DBManager().getStockIDBySymbol(symbol)
        if respons:
            self.clientsocket.send(pickle.dumps(respons))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getAllTweetsByStockID(self):
        # Receiving the arg of request
        stockID = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().getAllTweetsByStockID(stockID)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getMyStocksIDs(self):
        # Receiving the arg of request
        ID = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().getMyStocksIDs(ID)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getStockByID(self):
        # Receiving the arg of request
        stockID = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

        respons = DBManager.DBManager().getStockByID(stockID)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getAllStocksIDs(self):
        respons = DBManager.DBManager().getAllStocksIDs()

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def deleteStockByIDs(self):
        # Receiving the arg of request
        arg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        userID = arg[0]
        stockID = arg[1]

        respons = DBManager.DBManager().deleteStockByIDs(userID, stockID)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def addStockToUser(self):
        # Receiving the arg of request
        arg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        userID = arg[0]
        stockID = arg[1]

        respons = DBManager.DBManager().addStockToUser(userID, stockID)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))


    def getAllMessagesByUserID(self):
        # Receiving the arg of request
        arg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        userID = arg

        allPredictionIDs = DBManager.DBManager().getAllPredictionsIDByUserID(userID)
        allPredictions = []
        for predID in allPredictionIDs:
            predDateRec = DBManager.DBManager().getPredictionByID(predID[0])[0]
            stockID = predDateRec[0]
            nameSymbol = DBManager.DBManager().getNameAndSymbolByID(stockID)
            allPredictions.append((nameSymbol[0], nameSymbol[1] ,predDateRec[1], predDateRec[2]))

        respons = tuple(allPredictions)

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))    
            

    def getXYForGraphByID(self):
        # Receiving the arg of request
        arg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
        symbol = arg

        respons = getXYForGraph.getXYForGraph(symbol, 3)##

        if respons:
            responsPickled = pickle.dumps(respons)

            size = sys.getsizeof(responsPickled)

            # Sent size and respons
            self.clientsocket.send(pickle.dumps(size))
            self.clientsocket.send(responsPickled)
        else:
            # Sent error
            self.clientsocket.send(pickle.dumps(vocabulary.ERROR))  

