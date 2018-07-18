import pandas_datareader.data as web
import datetime
from DB import DBManager


class PandasDatareder(object):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.whatToretrieve()


    def whatToretrieve(self):
        start = datetime.datetime(2018, 5, 1)
        start = start.date()
        end = datetime.datetime.now()
        end = end.date()
        
        allStockID = DBManager.DBManager().getAllStocksIDs()

        if allStockID:
            for stockID in allStockID:
                id = stockID[0]
                # Getting the last date already exists
                lastDate = DBManager.DBManager().getLastPriceHistoryDateByID(id)
                if lastDate:
                    lastDate = lastDate[0]
                if type(lastDate) == 'datetime':
                    lastDate = lastDate.date()

                # Retrieves stock price history
                pricesHistory = False
                if lastDate == None: # No data
                    pricesHistory = self.retrieveStockPriceHistory(id, start, end)
                elif lastDate >= start: # There is some date
                    lastDate = lastDate + datetime.timedelta(days=1)
                    if lastDate < end: 
                        pricesHistory = self.retrieveStockPriceHistory(id, lastDate, end)
                elif lastDate == datetime.now(): # The date is up to date
                    pass
                if not (isinstance(pricesHistory, bool) and pricesHistory == False):
                    self.addPriceHistoryToDB(id, pricesHistory)
        else:
            print("PandasDatareder Error In whatToretrieve.")


    def retrieveStockPriceHistory(self, id, start, end):
        # Get symbol by id
        symbol = DBManager.DBManager().getSymbolByID(id)
        if symbol:
            symbol = symbol[0]

        try:
            results = web.DataReader(symbol, 'morningstar', start, end)
        except BaseException as e:
             print("Error in retrieveStockPriceHistory: ", e)
             return False

        print(results)
        return results


    def addPriceHistoryToDB(self, id, priceHistory):
        DBManager.DBManager().addPriceHistoryDataframe(id, priceHistory)

        

