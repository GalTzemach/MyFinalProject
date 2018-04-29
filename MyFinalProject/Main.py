import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog 
from UI import signUpIn
import Twitterr


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = signUpIn.Ui_Form()
        self.ui.setupUi(self)
        self.show()  

#    def x(self):
 #       print("x()")
  #      t = Twitterr.tw.Twtr.api

app = QApplication(sys.argv)
main = Main()
main.show()
sys.exit(app.exec_())



