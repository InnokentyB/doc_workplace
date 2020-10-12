# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton
import sys


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setWindowIcon(QtGui.QIcon("Plague_Inc._logo.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 80, 791, 511))
        self.tableView.setProperty("CardID", 1)
        self.tableView.setObjectName("tableView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 20, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.button = QPushButton('Обновить', self)
        self.button.move(680, 20)
        self.button.setToolTip('Обновить список пациентов')
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Список пациентов"))
        self.button.setProperty("Refresh", _translate("MainWindow", "Обновить"))
        self.tableView.setProperty("PatientName", _translate("MainWindow", "Золина Анна Павловна"))
        self.label.setText(_translate("MainWindow", "СПИСОК ПАЦИЕНТОВ"))


app = QtWidgets.QApplication(sys.argv)
window = Ui_MainWindow()
window.show()
app.exec_()