from DB import DBManager


def getXYForGraph(symbol, shift):
    # Get stockID from symbol
    stockID = DBManager.DBManager().getStockIDBySymbol(symbol)

    # Get close prices dict
    closeDict = DBManager.DBManager().getDateCloseDictById(stockID[0])

    # Create changeClose from close
    closeList = list(closeDict.items())
    changeCloseListTemp = []
    for i in range(len(closeList)):
        if i != 0:
            changeCloseListTemp.append((closeList[i][0], closeList[i][1] / closeList[i-1][1])) #(key, value)
    changeCloseDict = dict(changeCloseListTemp)

    # Get avg sentiment
    avgSentiment = DBManager.DBManager().getAvgSentimentByStockID(stockID[0][0])

    # Create changeClose & avgSentiment lists with same dates entrys
    closeKeys = changeCloseDict.keys()
    avgSentimentKeys = avgSentiment.keys()
    changeCloseList = []
    avgSentimentList = []

    for date in avgSentimentKeys:
        if date in closeKeys:
            changeCloseList.append([changeCloseDict[date]])
            avgSentimentList.append([avgSentiment[date]])

    # Do shift between changeClose and avgSentiment
    if len(changeCloseList) >= shift and len(avgSentimentList) >= shift:
        for i in range(shift):
            del changeCloseList[0]
            del avgSentimentList[len(avgSentimentList) - 1]

    return [changeCloseList, avgSentimentList]

