# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PatienList.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton, QStatusBar
import sys



class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 600)
        self.setWindowIcon(QtGui.QIcon("Plague_Inc._logo.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.statusBar().showMessage("State bar")
        self.setStatusBar(self,QStatusBar)
        self.statusbar
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(610, 10, 64, 23))
        self.label2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label2.setAutoFillBackground(True)
        self.label2.setObjectName("label2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(710, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        #self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        #self.lcdNumber.setGeometry(QtCore.QRect(610, 10, 64, 23))
        #self.lcdNumber.setObjectName("lcdNumber")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 60, 801, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action)
        self.menu.addSeparator()
        self.menu.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Кабинет врача"))
        self.label.setText(_translate("MainWindow", "СПИСОК ПАЦИЕНТОВ"))

        self.label2.setText(_translate("MainWindow", "1111"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер карты"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ФИО"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "СНИЛС"))
        self.menu.setTitle(_translate("MainWindow", "МЕНЮ"))
        self.menu_2.setTitle(_translate("MainWindow", "ПЕЧАТЬ"))
        self.action.setText(_translate("MainWindow", "СПИСОК ПАЦИЕНТОВ"))
        self.action_3.setText(_translate("MainWindow", "СПИСОК ПОСЕЩЕНИЙ"))

app = QtWidgets.QApplication(sys.argv)
window = Ui_MainWindow()
window.show()
app.exec_()