import socket
from ClientServerNetwork import vocabulary
import Singleton
import pickle
from math import ceil

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