import pandas_datareader.data as web
#from datetime 
import datetime
from DB import DBManager

class PandasDatareder(object):
    """description of class"""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.whatToretrieve()
        #retrieveStockPriceHistory


    def whatToretrieve(self):
        start = datetime.datetime(2018, 1, 1)
        start = start.date()
        end = datetime.datetime.now()
        end = end.date()
        
        allStockID = DBManager.DBManager().getAllStocksID()
        if allStockID:
            for stockID in allStockID:
                id = stockID[0]

                lastDate = DBManager.DBManager().getLastDateOfStockPricesHistory(id)[0]
                if type(lastDate) == 'datetime':
                    lastDate = lastDate.date()

                if lastDate == None:
                    pricesHistory = self.retrieveStockPriceHistory(id, start, end)
                elif lastDate >= start:
                    lastDate = lastDate + datetime.timedelta(days=1)
                    if lastDate < end:
                        pricesHistory = self.retrieveStockPriceHistory(id, lastDate, end)
                elif lastDate == datetime.now():
                    pass


    def retrieveStockPriceHistory(self, id, start, end):

        symbol = DBManager.DBManager().getSymbolOfStockByID(id)[0]

        try:
            results = web.DataReader(symbol, 'morningstar', start, end)
            print(type(results))
            print(results)
        except BaseException as exception:
             print("--- Exception: ", exception)

        #print(type(results))
        #print(results)

        DBManager.DBManager().priceHistoryDataframeToAdd(id, results)

        

