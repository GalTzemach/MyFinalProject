import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI import signUpInGUI
from ClientServerNetwork import clientNetwork


class signUpInGUILogic(QMainWindow, signUpInGUI.Ui_MainWindow):

    OK = "ok"
    isSignInn = False
    userID = None


    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  

        # Events
        self.signUp_pushButton.clicked.connect(self.signUp_pushButton_clicked)
        self.signIn_pushButton.clicked.connect(self.signIn_pushButton_clicked)


    def signUp_pushButton_clicked(self):
        # Check values
        isValid = self.checkSignUpVlues()
        if isinstance(isValid, bool) and isValid == True:
            # Try to signup
            isSignup = self.signUp()
            if isinstance(isSignup, bool) and isSignup == True:
                # Switch to signin
                self.toolBox.setCurrentIndex(1)

                self.success_label.setText("The signup was successful, now signin.")
                self.cleanSignUp()

                # Remove signup
                self.toolBox.removeItem(0)
            else:
                self.error_label.setText(str(isSignup))
        else:
            self.error_label.setText(str(isValid))


    def signIn_pushButton_clicked(self):
        # Check values
        isValid = self.checkSignInVlues()
        if isinstance(isValid, bool) and isValid == True:
            # Try signin
            isSignin = self.signIn()
            if isinstance(isSignin, bool) and isSignin == True:
                # Update flag
                self.isSignInn = True

                # Save userID
                self.userID = clientNetwork.clientNetwork().getIDByEmail(self.email_lineEdit_2.text())

                # Close signin window
                self.close()
            else:
                self.error_label_2.setText(str(isSignin))
        else:
            self.error_label_2.setText(str(isValid))


    def closeEvent(self, QCloseEvent):
        super().closeEvent(QCloseEvent)
        if not self.isSignInn:
            clientNetwork.clientNetwork().exit()


    def checkSignInVlues(self):
        result = ""

        # Get values
        email = self.email_lineEdit_2.text()
        password = self.password_lineEdit_2.text()

        # Check if the values are not empty
        if email == "" or password == "":
            result += "There are empty values, you must fill them all.\n"
            return result

        # Checking the validity of the values
        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) == None:
            result += "\"%s\" is invalid" % (self.email_label_2.text())

        if result == "":
            return True
        else:
            return result


    def checkSignUpVlues(self):
        result = ""

        # Get values
        firstName = self.firstName_lineEdit.text()
        lastName = self.lastName_lineEdit.text()
        email = self.email_lineEdit.text()
        phoneNumber = self.phoneNumber_lineEdit.text()
        password = self.password_lineEdit.text()

        # Check if the values are not empty
        if firstName == "" or lastName == "" or email == "" or phoneNumber == "" or password == "":
            result += "There are empty values, you must fill them all.\n"
            return result

        # Checking length
        if self.checkLength(firstName, 2, 15, self.firstName_label) != self.OK:
            result += self.checkLength(firstName, 2, 15, self.firstName_label)
        if self.checkLength(lastName, 2, 15, self.lastName_label) != self.OK:
            result += self.checkLength(lastName, 2, 15, self.lastName_label)
        if self.checkLength(phoneNumber, 8, 10, self.phoneNumber_label) != self.OK:
            result += self.checkLength(phoneNumber, 8, 10, self.phoneNumber_label)
        if self.checkLength(password, 3, 32, self.password_label) != self.OK:
            result += self.checkLength(password, 3, 32, self.password_label)

        if result != "":
            return result

        # Checking the validity of the values
        if not firstName.isalpha():
            result += "\"%s\" must be alphabetic only.\n" % (self.firstName_label.text())
        if not lastName.isalpha():
            result += "\"%s\" must be alphabetic only.\n" % (self.lastName_label.text())
        if not phoneNumber.isdigit():
            result += "\"%s\" must be digits only.\n" % (self.phoneNumber_label.text())

        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) == None:
            result += "\"%s\" is invalid" % (self.email_label.text())

        if result == "":
            return True
        else:
            return result


    def checkLength(self, str, min, max, name):
        length = len(str)

        if length > max or length < min:
            return "The length of \"%s\" must be between %d-%d.\n" % (name.text(), min, max)
        else:
            return self.OK


    def signUp(self):
        # Get values
        firstName = self.firstName_lineEdit.text()
        lastName = self.lastName_lineEdit.text()
        email = self.email_lineEdit.text()
        phoneNumber = self.phoneNumber_lineEdit.text()
        password = self.password_lineEdit.text()

        arg = (firstName, lastName, email, phoneNumber, password)

        response = clientNetwork.clientNetwork().signUp(arg)
        if isinstance(response, bool) and response == True:
            return True
        else:
            return response


    def signIn(self):
        # Get values
        email = self.email_lineEdit_2.text()
        password = self.password_lineEdit_2.text()

        arg = (email, password)

        response = clientNetwork.clientNetwork().signIn(arg)
        if isinstance(response, bool) and response == True:
            return True
        else:
            return response


    def cleanSignUp(self):
        self.firstName_lineEdit.clear()
        self.lastName_lineEdit.clear()
        self.email_lineEdit.clear()
        self.phoneNumber_lineEdit.clear()
        self.password_lineEdit.clear()
        self.error_label.clear()


def start():
    app = QApplication(sys.argv) # A new instance of QApplication
    form = signUpInGUILogic()                 
    form.show()   
    app.exec_()  
    return (form.isSignInn, form.userID)
    






