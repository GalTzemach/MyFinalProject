from UI import ClientGUILogic, signUpInGUILogic
from ClientServerNetwork import clientNetwork
from math import ceil


class Client():

    ID = None

    def __init__(self):

        clientNetwork.clientNetwork()
        isSignInAndID = signUpInGUILogic.start()
        isSignIn = isSignInAndID[0]
        if isSignIn:
            self.ID = isSignInAndID[1][0]
            ClientGUILogic.start(self.ID[0])
        #ClientGUILogic.start(1)


if __name__ == '__main__':
    Client()

