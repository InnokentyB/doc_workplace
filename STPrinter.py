from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import QDate, Qt, QRect, QEvent
from PyQt5.QtWidgets import (QPushButton, QStatusBar, QAction, QWidget, QMenu, QMenuBar, QMainWindow, QApplication,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox, QGridLayout, QHBoxLayout, QLineEdit, QDateEdit,
                             QLabel, QCalendarWidget,QFileDialog, QDialog)
from PyQt5.QtGui import QIcon

import sys
from DbWorker import DbWorker, RefWorker, ViewWorker, DefaultWorker
from PatientCard import Patient
from DefaultDialog import DefaultvalueDialog
from JournalPrinter import print_journal
import os
import datetime
import subprocess
import json

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))
        self.title = 'Рабочее место врача'
        self.file_path = ''
        #Place current date to status bar
        self.statusBar().showMessage("Текущая дата: " + QDate.currentDate().toString(Qt.DefaultLocaleLongDate))
        #Put Geometry
        self.top = 50
        self.left = 50
        self.width = 1800
        self.height = 900
        self.new_db = False
        #before start we need to check config file and DB path

        self.DB = DbWorker()
        #if self.new_db:
           # new_path = self.new_db_path_dialog()
           # self.DB.convert_db(new_path)
        self.DW = DefaultWorker()
        self.default = self.DW.get_default_list()

        self.refDb = RefWorker()

        #Call window
        self.setupUi()
        self.createTable()
        self.show()
    def setupUi(self):
        leftmargin = 20
        #Make menu bar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        listMenu = mainMenu.addMenu("Список посещений")
        printMenu = mainMenu.addMenu("Печать")
        exitButton = QAction(QIcon('icon\exit.png'),"Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("App exit")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        #Show json complite file
        #add list button
        PListButton = QAction(QIcon('icon\OpenList.png'), "Список пациетов", self)
        PListButton.setShortcut("Ctrl+O")
        PListButton.setStatusTip("Открыть список пациентов")
        PListButton.triggered.connect(self.openPatienBase)
        fileMenu.addAction(PListButton)
        #add add patient button
        AddPatientButton = QAction(QIcon('icon\AddToList.png'), "Добавить пациента", self)
        AddPatientButton.setShortcut("Ctrl+N")
        AddPatientButton.setStatusTip("Добавить пациента")
        AddPatientButton.triggered.connect(self.AddPatienToBaseCard)
        fileMenu.addAction(AddPatientButton)
        button = QPushButton("Добавить пациента", self)
        #button.move(20, 30)
        geo_but = QRect(leftmargin, 30, 150,30 )
        button.setGeometry(geo_but)

        button.clicked.connect(self.AddPatienToBaseCard)

        # add default dialog button
        leftmargin+=200
        button_dialog = QPushButton("Значения по-умолчанию", self)
        geo_but_visit = QRect(leftmargin, 30, 200, 30)
        button_dialog.setGeometry(geo_but_visit)
        button_dialog.clicked.connect(self.default_dialog)

        # add print journal button
        button_journal = QPushButton("Распечатать журнал", self)
        geo_but_journal  = QRect(580, 30, 150, 30)
        button_journal.setGeometry(geo_but_journal)
        button_journal.clicked.connect(self.print_journal)

        if self.DB.check_need_field_update():
            leftmargin += 200
            # add field button
            button_add_field = QPushButton("Добавить поля", self)
            geo_but_add_field  = QRect(leftmargin, 30, 150, 30)
            button_add_field.setGeometry(geo_but_add_field)
            button_add_field.clicked.connect(self.DB.update_fields)

        if self.DW.check_need_field_update():
            leftmargin += 200
            # add field button
            button_add_d_field = QPushButton("Добавить поля по умолчанию", self)
            geo_but_add_d_field = QRect(leftmargin, 30, 150, 30)
            button_add_d_field.setGeometry(geo_but_add_d_field)
            button_add_d_field.clicked.connect(self.DW.update_fields)

        """leftmargin += 200
        # add field button
        button_add_field = QPushButton("Обновить диагнозы", self)
        geo_but_add_field = QRect(leftmargin, 30, 150, 30)
        button_add_field.setGeometry(geo_but_add_field)
        button_add_field.clicked.connect(self.DB.update_dianosys)
        """

        #Set window params
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def createTable(self):
        self.table = QTableWidget(self)
        self.view = self.get_tab_view()
        patients = self.openPatienBase(self.view)
        headerline = patients.get('0000')
        colnum = len(headerline)+1
        self.table.setColumnCount(colnum)
        #rowcount = len(patients)
        #table.setRowCount(rowcount)
        hlist = ["ИД"]
        hlist.extend(headerline.values())
        self.table.setHorizontalHeaderLabels(hlist)
        i=0
        for cardnum, value in patients.items():

            if i>0:
                self.table.insertRow(i-1)
                a=0
                self.table.setItem(i-1,a,QTableWidgetItem(cardnum))
                pDict = value
                for key, value in pDict.items():
                    a+=1
                    if key == "Doctor":
                        if value:
                            value = self.get_doc_FIO(value)
                    self.table.setItem(i-1, a, QTableWidgetItem(value))
            i+=1

        self.table.itemDoubleClicked.connect(self.EditPatient)

        # add grid with patients
        self.grid_layout = QGridLayout()

        self.table.resizeColumnsToContents()
        self.grid_layout.addWidget(self.table)
        geo = QRect(self.left - 30, self.top + 30, self.width - 50, self.height - 100)
        self.grid_layout.setGeometry(geo)
        self.setLayout(self.grid_layout)
        #return self.table

    def openPatienBase(self, view):
        #init DB object to work with all files
        patients = self.DB.get_pat_by_view(view)# формитировать набор полей тут, а не в воркере
        return patients

    def AddPatienToBaseCard(self):
        self.Patient = Patient(patlist = self)

    def EditPatient(self):
        send = self.sender()
        RowNum = send.currentRow()
        item = send.item(RowNum,0)
        cardnum = item.text()
        self.Patient = Patient(patlist = self, id = cardnum)

    def updatelist(self):
        self.hide()
        self.createTable()
        self.show()

    def get_doc_FIO(self,doc_id):
        self.docs = self.refDb.get_doc_list()
        doc = self.docs.get(doc_id)
        doc_to_show = f'{doc.get("Last_name")} {doc.get("First_name")[0]}.{doc.get("Second_name")[0]}.'
        return doc_to_show

    def get_tab_view(self):
        self.view = ViewWorker()
        return self.view.get_patlist_view()

    def print_journal(self):
        path = self.default.get("file_path")
        today = datetime.date.today()
        self.filename = f"{path}\Журнал посещений за {str(today)}.xlsx"
        fields = ['Num_visit','Visit_Date','Visit_type','Card_num', 'Kont' ,'FIO','Sex','B_Date','Address_full','Work', 'DS_for_journal_full',
                  'DS_code_for_journal_full', 'Appointments', 'Notes']
        data = self.DB.get_pat_for_journal(fields) # тут добавить приведение в нужный вид, а не в воркере
        print_journal(data, self.filename)
        self.open_doc(self.filename)

    def open_doc(self, docname):
        #open statistic bill
        if os.name == 'nt':
            os.startfile(f'"{docname}"')
            #subprocess.Popen(['cmd.exe', '/c', docname])
        elif os.name == 'posix':
            os.startfile(f'"{docname}"')

    def default_dialog(self):
        DD = DefaultvalueDialog()
        DD.setModal(True)
        DD.exec()

    def db_file_dialog(self):
        while True:
            self.file = QFileDialog()
            #self.file.setFileMode(2)
            #self.file.setOption(QFileDialog.ShowDirsOnly, True)
            if self.file.exec_() == QDialog.Accepted:
                path = self.file.selectedFiles()[0]  # returns a list
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка выбора файла")
                MB.setText("Для работы приложения необходимо подключение к файлу базы данных")
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                raise FileNotFoundError("Для работы приложения необходимо подключение к файлу базы данных")
            #check for db extention
            if path.split('.')[1] =="db":
                break
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка выбора файла")
                file = path.split("\\")[-1]
                MB.setText(f'Выбранный вами файл "{file}" имеет расширение отличное от db')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()

        return path

#Run the app
app = QtWidgets.QApplication(sys.argv)
window = Ui_MainWindow()
window.show()
app.exec_()