import quandl

class Quandl(object):
    """description of class"""

    quandl.ApiConfig.api_key = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.readQuandlKeysFromFile():
    
            pass


    def readQuandlKeysFromFile():
        path = "C:\\Users\\Gal Tzemach\\Desktop\\quandlKeys.txt"
        # Open a file
        try:
            quandlKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("--- MyError: In readQuandlKeysFromFile function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = quandlKeysFile.read().splitlines()

        api_key = listOfKeys[0]

        # Close opened file
        quandlKeysFile.close()

        #Create quandl.ApiConfig.api_key object with the keys
        Quandl.quandl.ApiConfig.api_key = api_key        
        return True