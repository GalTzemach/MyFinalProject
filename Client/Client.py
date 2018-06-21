from UI import ClientGUILogic, signUpInGUILogic
from ClientServerNetwork import clientNetwork


class Client():

    def __init__(self):
        clientNetwork.clientNetwork()
        isSignIn = signUpInGUILogic.start()
        if isSignIn:
            ClientGUILogic.start()


if __name__ == '__main__':
    Client()

