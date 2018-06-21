import socket  
import threading
import time
import Singleton
import datetime
from ClientServerNetwork import vocabulary
from DB import DBManager
import pickle



class serverNetwork(metaclass=Singleton.Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create a socket object
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        host = socket.gethostname()                           

        port = 9999                                           

        # bind to the port
        serversocket.bind((host, port))                                  

        # queue up to 5 requests
        serversocket.listen(5) 

        print("The server is running... (%s)" % (datetime.datetime.now()))

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
        print("Got a connection from Thread%d %s" % (self.numThread, str(self.addr)))

        # Receiving requests 
        while True:

            # Receiving the type of request
            recvType = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))
            print("The server received a request of type: %s" % (recvType))

            if recvType == vocabulary.EXIT:
                self.clientsocket.close()
                return

            # Receiving the arg of request
            recvArg = pickle.loads(self.clientsocket.recv(vocabulary.BUFSIZE))

            if recvType == vocabulary.SIGNUP:
                self.signUp(recvArg)
            elif recvType == vocabulary.SIGNIN:
                self.signIn(recvArg)
            elif recvType == vocabulary.SET_IS_CONNECT:
                self.setIsConnect(recvArg)



    def signUp(self, recvArg):
        respons = DBManager.DBManager().addNewUser(recvArg[0], recvArg[1], recvArg[2], recvArg[3], recvArg[4])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.USER_EXIST))


    def signIn(self, recvArg):
        respons = DBManager.DBManager().signIn(recvArg[0], recvArg[1])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.SIGNIN_FAIL))


    def setIsConnect(self, recvArg):
        respons = DBManager.DBManager().setIsConnect(recvArg[0], recvArg[1])
        if respons:
            self.clientsocket.send(pickle.dumps(vocabulary.OK))
        else:
            self.clientsocket.send(pickle.dumps(vocabulary.SET_IS_CONNECT_FAIL))