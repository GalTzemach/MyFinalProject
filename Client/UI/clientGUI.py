# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 766)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.sugn_up_in_tab = QtWidgets.QWidget()
        self.sugn_up_in_tab.setObjectName("sugn_up_in_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sugn_up_in_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QtWidgets.QToolBox(self.sugn_up_in_tab)
        self.toolBox.setObjectName("toolBox")
        self.sign_up_page = QtWidgets.QWidget()
        self.sign_up_page.setGeometry(QtCore.QRect(0, 0, 238, 238))
        self.sign_up_page.setObjectName("sign_up_page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.sign_up_page)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.firstName_label = QtWidgets.QLabel(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.firstName_label.setFont(font)
        self.firstName_label.setObjectName("firstName_label")
        self.verticalLayout_3.addWidget(self.firstName_label)
        self.lastName_label = QtWidgets.QLabel(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.lastName_label.setFont(font)
        self.lastName_label.setObjectName("lastName_label")
        self.verticalLayout_3.addWidget(self.lastName_label)
        self.email_label = QtWidgets.QLabel(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.verticalLayout_3.addWidget(self.email_label)
        self.phoneNumber_label = QtWidgets.QLabel(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.phoneNumber_label.setFont(font)
        self.phoneNumber_label.setObjectName("phoneNumber_label")
        self.verticalLayout_3.addWidget(self.phoneNumber_label)
        self.password_label = QtWidgets.QLabel(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.verticalLayout_3.addWidget(self.password_label)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.firstName_lineEdit = QtWidgets.QLineEdit(self.sign_up_page)
        self.firstName_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.firstName_lineEdit.setClearButtonEnabled(False)
        self.firstName_lineEdit.setObjectName("firstName_lineEdit")
        self.verticalLayout_4.addWidget(self.firstName_lineEdit)
        self.lastName_lineEdit = QtWidgets.QLineEdit(self.sign_up_page)
        self.lastName_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.lastName_lineEdit.setClearButtonEnabled(False)
        self.lastName_lineEdit.setObjectName("lastName_lineEdit")
        self.verticalLayout_4.addWidget(self.lastName_lineEdit)
        self.email_lineEdit = QtWidgets.QLineEdit(self.sign_up_page)
        self.email_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.email_lineEdit.setClearButtonEnabled(False)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.verticalLayout_4.addWidget(self.email_lineEdit)
        self.phoneNumber_lineEdit = QtWidgets.QLineEdit(self.sign_up_page)
        self.phoneNumber_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.phoneNumber_lineEdit.setClearButtonEnabled(False)
        self.phoneNumber_lineEdit.setObjectName("phoneNumber_lineEdit")
        self.verticalLayout_4.addWidget(self.phoneNumber_lineEdit)
        self.password_lineEdit = QtWidgets.QLineEdit(self.sign_up_page)
        self.password_lineEdit.setEnabled(True)
        self.password_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.password_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.password_lineEdit.setClearButtonEnabled(False)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.verticalLayout_4.addWidget(self.password_lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem1)
        self.error_label = QtWidgets.QLabel(self.sign_up_page)
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.verticalLayout_10.addWidget(self.error_label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.sign_up_page)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.buttonBox.setFont(font)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_10.addWidget(self.buttonBox)
        self.verticalLayout_5.addLayout(self.verticalLayout_10)
        self.toolBox.addItem(self.sign_up_page, "")
        self.sign_in_page = QtWidgets.QWidget()
        self.sign_in_page.setGeometry(QtCore.QRect(0, 0, 217, 151))
        self.sign_in_page.setObjectName("sign_in_page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.sign_in_page)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.email_label_2 = QtWidgets.QLabel(self.sign_in_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.email_label_2.setFont(font)
        self.email_label_2.setObjectName("email_label_2")
        self.verticalLayout_12.addWidget(self.email_label_2)
        self.password_label_2 = QtWidgets.QLabel(self.sign_in_page)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.password_label_2.setFont(font)
        self.password_label_2.setObjectName("password_label_2")
        self.verticalLayout_12.addWidget(self.password_label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_12)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.email_lineEdit_2 = QtWidgets.QLineEdit(self.sign_in_page)
        self.email_lineEdit_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.email_lineEdit_2.setObjectName("email_lineEdit_2")
        self.verticalLayout_13.addWidget(self.email_lineEdit_2)
        self.password_lineEdit_2 = QtWidgets.QLineEdit(self.sign_in_page)
        self.password_lineEdit_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.password_lineEdit_2.setObjectName("password_lineEdit_2")
        self.verticalLayout_13.addWidget(self.password_lineEdit_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_13)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_11.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem4)
        self.error_label_2 = QtWidgets.QLabel(self.sign_in_page)
        self.error_label_2.setText("")
        self.error_label_2.setObjectName("error_label_2")
        self.verticalLayout_11.addWidget(self.error_label_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem5)
        self.buttonBox_2 = QtWidgets.QDialogButtonBox(self.sign_in_page)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.buttonBox_2.setFont(font)
        self.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox_2.setObjectName("buttonBox_2")
        self.verticalLayout_11.addWidget(self.buttonBox_2)
        self.verticalLayout_6.addLayout(self.verticalLayout_11)
        self.toolBox.addItem(self.sign_in_page, "")
        self.verticalLayout_2.addWidget(self.toolBox)
        self.tabWidget.addTab(self.sugn_up_in_tab, "")
        self.my_account_tab = QtWidgets.QWidget()
        self.my_account_tab.setObjectName("my_account_tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.my_account_tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.helloUser_label = QtWidgets.QLabel(self.my_account_tab)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.helloUser_label.setFont(font)
        self.helloUser_label.setObjectName("helloUser_label")
        self.verticalLayout_7.addWidget(self.helloUser_label)
        self.myStocks_groupBox = QtWidgets.QGroupBox(self.my_account_tab)
        self.myStocks_groupBox.setObjectName("myStocks_groupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.myStocks_groupBox)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.myStocks_tableWidget = QtWidgets.QTableWidget(self.myStocks_groupBox)
        self.myStocks_tableWidget.setAcceptDrops(False)
        self.myStocks_tableWidget.setAutoFillBackground(False)
        self.myStocks_tableWidget.setAlternatingRowColors(True)
        self.myStocks_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.myStocks_tableWidget.setObjectName("myStocks_tableWidget")
        self.myStocks_tableWidget.setColumnCount(3)
        self.myStocks_tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myStocks_tableWidget.setItem(2, 2, item)
        self.myStocks_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.myStocks_tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_9.addWidget(self.myStocks_tableWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addStocks_pushButton = QtWidgets.QPushButton(self.myStocks_groupBox)
        self.addStocks_pushButton.setAcceptDrops(True)
        self.addStocks_pushButton.setObjectName("addStocks_pushButton")
        self.horizontalLayout_4.addWidget(self.addStocks_pushButton)
        self.deleteStocks_pushButton = QtWidgets.QPushButton(self.myStocks_groupBox)
        self.deleteStocks_pushButton.setObjectName("deleteStocks_pushButton")
        self.horizontalLayout_4.addWidget(self.deleteStocks_pushButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addWidget(self.myStocks_groupBox)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.myMessages_groupBox = QtWidgets.QGroupBox(self.my_account_tab)
        self.myMessages_groupBox.setObjectName("myMessages_groupBox")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.myMessages_groupBox)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.myMessages_tableWidget = QtWidgets.QTableWidget(self.myMessages_groupBox)
        self.myMessages_tableWidget.setAlternatingRowColors(True)
        self.myMessages_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.myMessages_tableWidget.setObjectName("myMessages_tableWidget")
        self.myMessages_tableWidget.setColumnCount(4)
        self.myMessages_tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.myMessages_tableWidget.setItem(2, 3, item)
        self.myMessages_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_17.addWidget(self.myMessages_tableWidget)
        self.verticalLayout_8.addWidget(self.myMessages_groupBox)
        self.tabWidget.addTab(self.my_account_tab, "")
        self.all_stocks_tab = QtWidgets.QWidget()
        self.all_stocks_tab.setObjectName("all_stocks_tab")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.all_stocks_tab)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.allStocks_groupBox = QtWidgets.QGroupBox(self.all_stocks_tab)
        self.allStocks_groupBox.setMaximumSize(QtCore.QSize(16777215, 250))
        self.allStocks_groupBox.setObjectName("allStocks_groupBox")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.allStocks_groupBox)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.allStocks_tableWidget = QtWidgets.QTableWidget(self.allStocks_groupBox)
        self.allStocks_tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.allStocks_tableWidget.setAcceptDrops(False)
        self.allStocks_tableWidget.setAutoFillBackground(False)
        self.allStocks_tableWidget.setAlternatingRowColors(True)
        self.allStocks_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.allStocks_tableWidget.setObjectName("allStocks_tableWidget")
        self.allStocks_tableWidget.setColumnCount(3)
        self.allStocks_tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.allStocks_tableWidget.setItem(2, 2, item)
        self.allStocks_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.allStocks_tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_14.addWidget(self.allStocks_tableWidget)
        self.verticalLayout_15.addWidget(self.allStocks_groupBox)
        self.groupBox = QtWidgets.QGroupBox(self.all_stocks_tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_16.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_16.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_16.addWidget(self.label_3)
        self.verticalLayout_15.addWidget(self.groupBox)
        self.tabWidget.addTab(self.all_stocks_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 933, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.firstName_label.setText(_translate("MainWindow", "First name:"))
        self.lastName_label.setText(_translate("MainWindow", "Last name:"))
        self.email_label.setText(_translate("MainWindow", "Email:"))
        self.phoneNumber_label.setText(_translate("MainWindow", "Phone number:"))
        self.password_label.setText(_translate("MainWindow", "Password:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sign_up_page), _translate("MainWindow", "Sign Up"))
        self.email_label_2.setText(_translate("MainWindow", "Email:"))
        self.password_label_2.setText(_translate("MainWindow", "Password:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.sign_in_page), _translate("MainWindow", "Sign In"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sugn_up_in_tab), _translate("MainWindow", "Sign Up/In"))
        self.helloUser_label.setText(_translate("MainWindow", "Hello User"))
        self.myStocks_groupBox.setTitle(_translate("MainWindow", "My stocks"))
        self.myStocks_tableWidget.setSortingEnabled(True)
        item = self.myStocks_tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.myStocks_tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.myStocks_tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.myStocks_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Symbol"))
        item = self.myStocks_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.myStocks_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Description"))
        __sortingEnabled = self.myStocks_tableWidget.isSortingEnabled()
        self.myStocks_tableWidget.setSortingEnabled(False)
        item = self.myStocks_tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "APPL"))
        item = self.myStocks_tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "Apple Inc."))
        item = self.myStocks_tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "Computer Manufacturing"))
        item = self.myStocks_tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "GOOG"))
        item = self.myStocks_tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "Alphabet Inc."))
        item = self.myStocks_tableWidget.item(1, 2)
        item.setText(_translate("MainWindow", "Computer Software: Programming, Data Processing"))
        item = self.myStocks_tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "FB"))
        item = self.myStocks_tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "Facebook, Inc."))
        item = self.myStocks_tableWidget.item(2, 2)
        item.setText(_translate("MainWindow", "Computer Software: Programming, Data Processing"))
        self.myStocks_tableWidget.setSortingEnabled(__sortingEnabled)
        self.addStocks_pushButton.setText(_translate("MainWindow", "Add Stocks"))
        self.deleteStocks_pushButton.setText(_translate("MainWindow", "Delete Stock"))
        self.myMessages_groupBox.setTitle(_translate("MainWindow", "My messages"))
        self.myMessages_tableWidget.setSortingEnabled(True)
        item = self.myMessages_tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.myMessages_tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.myMessages_tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.myMessages_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.myMessages_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Stock"))
        item = self.myMessages_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Prediction"))
        item = self.myMessages_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "True Prediction"))
        __sortingEnabled = self.myMessages_tableWidget.isSortingEnabled()
        self.myMessages_tableWidget.setSortingEnabled(False)
        item = self.myMessages_tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "01/01/2018"))
        item = self.myMessages_tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "GOOG"))
        item = self.myMessages_tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "Rise"))
        item = self.myMessages_tableWidget.item(0, 3)
        item.setText(_translate("MainWindow", "N/A"))
        item = self.myMessages_tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "01/01/2018"))
        item = self.myMessages_tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "FB"))
        item = self.myMessages_tableWidget.item(1, 2)
        item.setText(_translate("MainWindow", "Fall"))
        item = self.myMessages_tableWidget.item(1, 3)
        item.setText(_translate("MainWindow", "N/A"))
        item = self.myMessages_tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "01/01/2018"))
        item = self.myMessages_tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "AAPL"))
        item = self.myMessages_tableWidget.item(2, 2)
        item.setText(_translate("MainWindow", "Same"))
        item = self.myMessages_tableWidget.item(2, 3)
        item.setText(_translate("MainWindow", "N/A"))
        self.myMessages_tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_account_tab), _translate("MainWindow", "My Account"))
        self.allStocks_groupBox.setTitle(_translate("MainWindow", "All stocks"))
        self.allStocks_tableWidget.setSortingEnabled(True)
        item = self.allStocks_tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.allStocks_tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.allStocks_tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.allStocks_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Symbol"))
        item = self.allStocks_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.allStocks_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Description"))
        __sortingEnabled = self.allStocks_tableWidget.isSortingEnabled()
        self.allStocks_tableWidget.setSortingEnabled(False)
        item = self.allStocks_tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "APPL"))
        item = self.allStocks_tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "Apple Inc."))
        item = self.allStocks_tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "Computer Manufacturing"))
        item = self.allStocks_tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "GOOG"))
        item = self.allStocks_tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "Alphabet Inc."))
        item = self.allStocks_tableWidget.item(1, 2)
        item.setText(_translate("MainWindow", "Computer Software: Programming, Data Processing"))
        item = self.allStocks_tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "FB"))
        item = self.allStocks_tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "Facebook, Inc."))
        item = self.allStocks_tableWidget.item(2, 2)
        item.setText(_translate("MainWindow", "Computer Software: Programming, Data Processing"))
        self.allStocks_tableWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "Information about a particular stock"))
        self.label_2.setText(_translate("MainWindow", "Messages/Recommendations"))
        self.label_4.setText(_translate("MainWindow", "Regression"))
        self.label_3.setText(_translate("MainWindow", "Other graphs and information"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.all_stocks_tab), _translate("MainWindow", "All Stocks"))




