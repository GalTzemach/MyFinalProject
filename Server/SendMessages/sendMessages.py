from DB import DBManager
import datetime
import smtplib


class sendMessages(object):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.send()


    def send(self):
        # Get all stocks id
        allStocksIDs = DBManager.DBManager().getAllStocksIDs()
        for stockID in allStocksIDs:
            stockID = stockID[0]
            # Just if exsist prediction of stock id today
            if DBManager.DBManager().isExsistPredictionByIDAndDate(stockID, datetime.datetime.now().date()):
                # Get prediction details
                prediction = DBManager.DBManager().getPredictionByIDAndDate(stockID, datetime.datetime.now().date())
                # Get all users that register to this stock
                allRegistered = DBManager.DBManager().getAllRegisterToStockByID(stockID)
                if allRegistered:
                    for userID in allRegistered:
                        userID = userID[0]
                        # Add user prediction to DB
                        DBManager.DBManager().addUserPrediction(userID, prediction[0][0])
                        # prepare parameters to email
                        toEmail = DBManager.DBManager().getEmailByID(userID)
                        subject = 'Sentiment Editor- the Holy Grail'
                        self.readEmailKeys()
                        # Sending Email
                        self.sendEmail(self.email, self.password, toEmail[0][0], subject, prediction[0])


    def sendEmail(self, user, pwd, recipient, subject, body):
        FROM = user
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = subject

        nameSymbol = DBManager.DBManager().getNameAndSymbolByID(body[1])
        TEXT = "Prediction for %s(%s) stock, to %s, is: %s, with %f%% of accuracy." % (nameSymbol[0], nameSymbol[0], str(body[2].date()), body[5], body[6]) 

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print ("Email successfully sent to %s, on %s (%s) stock." % (recipient, nameSymbol[0], nameSymbol[0]))
        except BaseException as e:
            print("e:", e)
            print ("failed to send mail")


    def readEmailKeys(self):
        path = "C:\\myFinalProject\\emailKeys.txt"
        # Open a file
        try:
            dataBaseKeysFile = open(path,"r") # r Opens a file for reading only.
        except FileNotFoundError:
            print("--- MyError: In readEmailKeys function, File ", path, " not found.")
            return False

        # Read all file
        listOfKeys = dataBaseKeysFile.read().splitlines()
        self.email = listOfKeys[0]
        self.password = listOfKeys[1]

        # Close opened file
        dataBaseKeysFile.close()




