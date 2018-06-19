import pandas_datareader.data as web
#from datetime 
import datetime
from DB import DBManager
import matplotlib.pyplot as plt
import seaborn as sb

class PandasDatareder(object):
    """description of class"""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.whatToretrieve()


    def whatToretrieve(self):

        # Set dates
        start = datetime.datetime(2018, 5, 1)
        start = start.date()
        end = datetime.datetime.now()
        end = end.date()
        
        # Get all stock id
        allStockID = DBManager.DBManager().getAllStocksID()

        if allStockID:
            for stockID in allStockID:
                # Get the id
                id = stockID[0]

                # Getting the last date already exists
                lastDate = DBManager.DBManager().getLastDateOfStockPricesHistory(id)[0]
                if type(lastDate) == 'datetime':
                    lastDate = lastDate.date()

                # Retrieves stock price history
                if lastDate == None: # No data
                    pricesHistory = self.retrieveStockPriceHistory(id, start, end)
                elif lastDate >= start: # There is some date
                    lastDate = lastDate + datetime.timedelta(days=1)
                    if lastDate < end: 
                        pricesHistory = self.retrieveStockPriceHistory(id, lastDate, end)
                elif lastDate == datetime.now(): # The date is up to date
                    pass

                self.addPriceHistoryToDB(id, pricesHistory)


    def retrieveStockPriceHistory(self, id, start, end):

        # Get symbol by id
        symbol = DBManager.DBManager().getSymbolOfStockByID(id)[0]

        try:
            # Get stock price history
            results = web.DataReader(symbol, 'morningstar', start, end)
        except BaseException as exception:
             print("--- Exception: ", exception)

        print(type(results))
        print(results)

        #r0 = results.loc[symbol]
        #print(type(r0))
        #print(r0)

        #sb.regplot(x = "Open", y = "Close", data = r0)
        #plt.show()
        #plt.close()

        return results


    def addPriceHistoryToDB(self, id, priceHistory):

        DBManager.DBManager().addPriceHistoryDataframe(id, priceHistory)

        

