from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore.Qt import
from  PyQt5.QtCore import QDate, Qt, QRect, QEvent, Q_FLAGS
from PyQt5.QtWidgets import (QPushButton, QStatusBar, QAction, QWidget, QMenu, QMenuBar, QMainWindow, QApplication,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox, QGridLayout, QHBoxLayout, QLineEdit, QDateEdit,
                             QLabel, QCalendarWidget, QListWidget, QComboBox, QGroupBox, QCompleter, QPlainTextEdit)
from PyQt5.QtGui import QIcon
import datetime
import subprocess
import os
from PrintStateBill import printST
from DbWorker import RefWorker, DefaultWorker
from FieldHelper import  FieldHelper
import re


class Patient(QtWidgets.QMainWindow):

    STATUS_NEW = 'Создание'
    STATUS_EDIT = 'Изменение'

    def __init__(self,patlist, id = '' ):
        super().__init__()
        #field init
        self.num_card = id
        self.field_init()

        #DB init from list
        self.patlist = patlist
        self.DB = self.patlist.DB
        self.refDb = self.patlist.refDb
        self.mkd = self.refDb.get_mkd_list()
        self.services = self.refDb.get_services_list()
        self.workDB = self.refDb.get_work_list()
        self.SMODb = self.refDb.get_SMO_list()
        self.DW = DefaultWorker()
        self.default = self.DW.get_default_list()
        self.FH = FieldHelper(self, self.refDb)
        self.diagnosysDB = self.refDb.get_diagnosys_list()

        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))
        self.title = 'Карточка пациента'
        # Place current date to status bar
        self.statusBar().showMessage("Текущая дата: " + QDate.currentDate().toString(Qt.DefaultLocaleLongDate))
        # Put Geometry
        self.top = 50
        self.left = 50
        self.width = 1800
        self.height = 900
        self.mrg = 0.2
        #if not new record - get data and place to fields
        if self.num_card:
            self.parse_data()
            self.state = self.STATUS_EDIT
        else:
            self.set_default()
            self.state = self.STATUS_NEW
        self.setup_buttons()
        self.setup_card_fields()
        self.setup_personal_fields()
        self.setup_document_fields()
        self.setup_address_fields()
        self.setup_work_fields()
        self.setup_med_fields()
        #self.runapp()
        # Set window params
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def field_init(self):
        self.fname = ""
        self.sname = ""
        self.lname = ""
        self.snils = ""
        self.dob = ""
        self.sex = ""
        self.card_num = ""
        self.kont = ""
        self.Pass_Type = ""
        self.Pass_Series = ""
        self.Pass_Num = ""
        self.Subject = ""
        self.District = ""
        self.City = ""
        self.Locality = ""
        self.Street = ""
        self.House = ""
        self.Flat = ""
        self.Doctor = ""
        self.Work = ""
        self.Work_Post = ""
        self.DS_first = ""
        self.DS_first_code = ""
        self.Service = ""
        self.Service_code = ""
        self.DS_second = ""
        self.DS_second_code = ""
        self.DS_concom1 = ""
        self.DS_concom1_code = ""
        self.DS_concom2 = ""
        self.DS_concom2_code = ""
        self.DS_concom3 = ""
        self.DS_concom3_code = ""
        self.DS_Type = ""
        self.Visit_Date = ""
        self.Close_Date = ""
        self.Work_type = ""
        self.DS_for_journal = ""
        self.Notes = ""
        self.Appointments = ""
        self.DS_concom1_for_journal = ""
        self.DS_concom2_for_journal = ""
        self.DS_concom3_for_journal = ""
        self.Address_full =""
        self.DS_for_journal_full = ""
        self.Num_visit = ""
        self.Visit_type = ""
        self.Polis_Series = ""
        self.Polis_Num = ""
        self.SMO = ""

    def setup_buttons(self):
        # Make menu bar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        listMenu = mainMenu.addMenu("Список посещений")
        printMenu = mainMenu.addMenu("Печать")
        exitButton = QAction(QIcon('icon\exit.png'), "Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("App exit")
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        # Show json complite file
        # add add patient menu point
        SavePatientButton = QAction(QIcon('icon\Save.png'), "Сохранить пациента", self)
        SavePatientButton.setShortcut("Ctrl+S")
        SavePatientButton.setStatusTip("Сохранить пациента")
        SavePatientButton.triggered.connect(self.save_patient)
        fileMenu.addAction(SavePatientButton)
        # add visit menu point
        #PListButton = QAction(QIcon('icon\VisitIcon.png'), "Добавить посещение", self)
        #PListButton.setShortcut("Ctrl+K")
        #PListButton.setStatusTip("Добавить посещение пациентf")
        #PListButton.triggered.connect(self.AddVisit)
       # fileMenu.addAction(PListButton)
        # add save button
        button = QPushButton("Сохранить пациента", self)
        geo_but = QRect(50, 30, 150, 30)
        button.setGeometry(geo_but)
        #add cancel button
        button_Cancel = QPushButton("Закрыть", self)
        geo_but_сan = QRect(250, 30, 150, 30)
        button_Cancel.setGeometry(geo_but_сan)

        # add print button
        button_Print= QPushButton("Печать стат талона", self)
        geo_but_prt = QRect(450, 30, 150, 30)
        button_Print.setGeometry(geo_but_prt)

        #connect buttons to actions
        button.clicked.connect(self.save_patient)
        button_Cancel.clicked.connect(self.close)
        button_Print.clicked.connect(self.print_ST)


    def setup_card_fields(self):
        #add card fields
        # card num
        label_margin = 2
        self.vheight = 2
        left = 1
        fsize = 2
        self.CN_filed = self.FH.add_line_field("Номер карты",self.vheight*50,left, self.card_num, label_margin=label_margin, field_size=fsize)
        left+=(fsize+ label_margin+ self.mrg)
        fsize,label_margin = 1,2
        # kontingent
        self.kont_filed = self.FH.add_cbox_field("Контингент",self.vheight*50, left, ['Г','С','Г78','П','Р','ЧС'],self.kont,label_margin=label_margin, field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 5,2
        #Doctor
        self.Doctor_filed = self.FH.add_doc_field("Врач", self.vheight*50, left,self.FH.get_doc_to_field(self.Doctor),label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 2,2

        self.Visit_Date_filed = self.FH.add_date_field("Дата посещения", self.vheight * 50, left, self.Visit_Date,
                                                    default_value=QDate.currentDate(), readonly=True,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 2,3
        self.Num_visit_filed = self.FH.add_line_field("Номер посещения", self.vheight * 50, left, str(self.Num_visit),label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 3,2
        self.Visit_type_buttons = self.FH.add_radio_button_field("Тип посещения", self.vheight * 50, left,['ВВК', 'Первичный', 'Повторный', 'Диспансеризация', 'ФЗ-302'],
                                                       self.Visit_type,label_margin=label_margin,field_size=fsize)
        self.Visit_type_buttons.buttonClicked.connect(self.visit_button_clicked)

    def visit_button_clicked(self,button):
        self.Visit_type = button.text()

    def setup_personal_fields(self):
        #add personal patient's fields
        label_margin = 2
        left = 1
        fsize = 2
        #Last Name
        self.vheight+=1
        self.lname_filed = self.FH.add_line_field("Фамилия",self.vheight*50,left, self.lname,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 2,2
        #First name
        self.fname_filed = self.FH.add_line_field("Имя",self.vheight*50,left, self.fname,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        # Second name
        self.sname_filed = self.FH.add_line_field("Отчество",self.vheight*50,left, self.sname,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
         # Date of Birth
        self.DBirth_filed = self.FH.add_date_field("Дата рождения",self.vheight*50, left, self.dob,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize,label_margin = 3,1
        # sex
        self.sex_buttons = self.FH.add_radio_button_field('Пол', self.vheight * 50, left, ['муж','жен'], self.sex,label_margin=label_margin,field_size=fsize, layout="horizontal")
        self.sex_buttons.buttonClicked.connect(self.sex_button_clicked)
        left += (fsize + label_margin + self.mrg)
        # SNILS
        self.SNILS_filed = self.FH.add_line_field("СНИЛС",self.vheight*50,left,self.snils,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        #self.sex_filed = self.add_cbox_field("Пол",self.vheight*50, 1290, ['муж','жен'],self.sex)
    def sex_button_clicked(self,button):
        self.sex =button.text()

    def setup_document_fields(self):
        #add identifing document fields
        left = 1
        self.vheight+=1
        fsize, label_margin = 2, 2
        # Pass_Type
        self.Pass_Type_filed = self.FH.add_line_field("Тип документа",self.vheight*50,left, self.Pass_Type,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        # Pass_Series
        self.Pass_Series_filed = self.FH.add_line_field("Серия",self.vheight*50,left,self.Pass_Series,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        # Pass_Num
        self.Pass_Num_filed = self.FH.add_line_field("Номер",self.vheight*50,left,self.Pass_Num,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize, label_margin = 1, 2
        # Polis_Series
        self.Polis_Series_filed = self.FH.add_line_field("Полис серия", self.vheight * 50, left, self.Polis_Series,
                                                     label_margin=label_margin, field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize = 2
        # Pass_Num
        self.Polis_Num_filed = self.FH.add_line_field("Полис номер", self.vheight * 50, left, self.Polis_Num,
                                                     label_margin=label_margin, field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize, label_margin = 4, 1
        self.SMO_filed = self.FH.add_compliter_line_field("СМО", self.vheight * 50, left, self.SMODb,
                                                           self.SMO, label_margin=label_margin, field_size=fsize)
        self.SMO_filed.editingFinished.connect(self.check_SMO)
        left += (fsize + label_margin + self.mrg)


    def setup_address_fields(self):
        #add patient's address fields
        left = 1
        self.vheight += 1
        fsize, label_margin = 4, 2
        # Subject
        self.RList = self.refDb.get_regions_list()
        self.Subject_filed = self.FH.add_compliter_line_field("Регион", self.vheight*50, left,self.RList,self.Subject,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize, label_margin = 3, 1
        # District
        self.District_filed = self.FH.add_line_field("Район", self.vheight*50, left, self.District,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        # City
        self.City_filed = self.FH.add_line_field("Город", self.vheight*50, left, self.City,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        label_margin = 2
        # Locality
        self.Locality_filed = self.FH.add_line_field("Нас. пункт", self.vheight*50, left, self.Locality,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        label_margin = 1
        # Street
        self.Street_filed = self.FH.add_line_field("Улица", self.vheight*50, left, self.Street,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize=  1
        # House
        self.House_filed = self.FH.add_line_field("Дом",self.vheight*50, left, self.House,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        label_margin = 2
        # Flat
        self.Flat_filed = self.FH.add_line_field("Квартира", self.vheight*50, left, self.Flat,label_margin=label_margin,field_size=fsize)

    def setup_work_fields(self):
        wtype_list = ['работает','проходит военную службу или приравненную к ней службу','пенсионер(ка)','студент(ка)','не работает','прочие']
        #add patient's work fields
        left = 1
        self.vheight += 1
        fsize, label_margin = 7, 2
        #Work type
        self.Work_type_filed = self.FH.add_cbox_field("Занятость", self.vheight*50, left,wtype_list, self.Work_type,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize=3
        # Work
        self.Work_filed = self.FH.add_compliter_line_field("Место работы", self.vheight*50, left,self.workDB, self.Work,label_margin=label_margin,field_size=fsize)
        self.Work_filed.editingFinished.connect(self.check_work)
        left += (fsize + label_margin + self.mrg)
        fsize = 4
        # Work_Post
        self.Work_Post_filed = self.FH.add_line_field("Должность", self.vheight*50, left,self.Work_Post,label_margin=label_margin,field_size=fsize)

    def setup_med_fields(self):
        #add patient's work fields
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # DS_first
        self.DS_first_filed = self.FH.add_compliter_line_field("Диагноз предв.", self.vheight*50, left, self.mkd, self.DS_first,label_margin=label_margin,field_size=fsize)
        self.DS_first_filed.editingFinished.connect(self.set_code_DS_first)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # DS_first_code
        self.DS_first_code_filed = self.FH.add_line_field("Код по МКБ-10", self.vheight*50, left,self.DS_first_code, readonly=True,label_margin=label_margin,field_size=fsize)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # Service
        self.Service_filed = self.FH.add_compliter_line_field("Мед услуга.", self.vheight*50, left,self.services, self.Service,label_margin=label_margin,field_size=fsize)
        self.Service_filed.editingFinished.connect(self.set_code_Service)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # Service_code
        self.Service_code_filed = self.FH.add_line_field("Код", self.vheight*50, left,self.Service_code, readonly=True,label_margin=label_margin,field_size=fsize)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # DS_second
        self.DS_second_filed = self.FH.add_compliter_line_field("Диагноз заключ.", self.vheight*50, left,self.mkd,self.DS_second,label_margin=label_margin,field_size=fsize)
        self.DS_second_filed.editingFinished.connect(self.set_code_DS_second)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # DS_second_code
        self.DS_second_code_filed = self.FH.add_line_field("Код по МКБ-10", self.vheight*50, left,self.DS_second_code,readonly=True,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize = 10
        #Diagnosis to journal
        self.DS_for_journal_filed = self.FH.add_compliter_line_field("Диагноз заключ.", self.vheight*50, left,self.refDb.get_diagnosys_list(),
                                                                     self.DS_for_journal,label_margin=label_margin,field_size=fsize)
        self.DS_for_journal_filed.editingFinished.connect(self.check_diagnosys)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # DS_concom1
        self.DS_concom1_filed = self.FH.add_compliter_line_field("Диагноз сопут. 1.", self.vheight*50, left,self.mkd,self.DS_concom1,label_margin=label_margin,field_size=fsize)
        self.DS_concom1_filed.editingFinished.connect(self.set_code_DS_add1)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # DS_concom1_code
        self.DS_concom1_code_filed = self.FH.add_line_field("Код по МКБ-10", self.vheight*50, left,self.DS_concom1_code, readonly=True,label_margin=label_margin,field_size=fsize)
        #DS to journal
        left += (fsize + label_margin + self.mrg)
        fsize = 10
        self.DS_concom1_for_journal_filed = self.FH.add_compliter_line_field("Диагноз сопут. 1", self.vheight*50, left,self.refDb.get_diagnosys_list(),
                                                                             self.DS_concom1_for_journal,label_margin=label_margin,field_size=fsize)
        self.DS_concom1_for_journal_filed.editingFinished.connect(self.check_diagnosys)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # DS_concom2
        self.DS_concom2_filed = self.FH.add_compliter_line_field("Диагноз сопут. 2.", self.vheight*50, left,self.mkd,self.DS_concom2,label_margin=label_margin,field_size=fsize)
        self.DS_concom2_filed.editingFinished.connect(self.set_code_DS_add2)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # DS_concom2_code
        self.DS_concom2_code_filed = self.FH.add_line_field("Код по МКБ-10", self.vheight*50, left,self.DS_concom2_code, readonly=True,label_margin=label_margin,field_size=fsize)
        # DS to journal
        left += (fsize + label_margin + self.mrg)
        fsize = 10
        self.DS_concom2_for_journal_filed = self.FH.add_compliter_line_field("Диагноз сопут. 2", self.vheight * 50, left,
                                                                     self.refDb.get_diagnosys_list(), self.DS_concom2_for_journal,label_margin=label_margin,
                                                                             field_size=fsize, callback = self.check_diagnosys)
        #self.DS_concom2_for_journal_filed.editingFinished.connect(self.check_diagnosys)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        # DS_concom3
        self.DS_concom3_filed = self.FH.add_compliter_line_field("Диагноз сопут. 3.", self.vheight*50, left,self.mkd,self.DS_concom3,label_margin=label_margin,field_size=fsize)
        self.DS_concom3_filed.editingFinished.connect(self.set_code_DS_add3)
        left += (fsize + label_margin + self.mrg)
        fsize = 3
        # DS_concom3_code
        self.DS_concom3_code_filed = self.FH.add_line_field("Код по МКБ-10", self.vheight*50, left,self.DS_concom3_code, readonly=True,label_margin=label_margin,field_size=fsize)
        # DS to journal
        left += (fsize + label_margin + self.mrg)
        fsize = 10
        self.DS_concom3_for_journal_filed = self.FH.add_compliter_line_field("Диагноз сопут. 3", self.vheight * 50, left,
                                                                     self.refDb.get_diagnosys_list(), self.DS_concom3_for_journal,label_margin=label_margin,field_size=fsize)
        self.DS_concom3_for_journal_filed.editingFinished.connect(self.check_diagnosys)
        left = 1
        self.vheight += 1
        fsize, label_margin = 10, 2
        #DS_Type
        self.DS_Type_buttons = self.FH.add_radio_button_field('Тип заболевания', self.vheight * 50, left, ['','острое','впервые в жизни установленное хроническое','ранее установленное хроническое']
                                                              , self.DS_Type, label_margin=label_margin, field_size=fsize,
                                                          layout="horizontal")
        self.DS_Type_buttons.buttonClicked.connect(self.DS_Type_button_clicked)

        #self.DS_Type_filed = self.FH.add_cbox_field("Тип заболевания", self.vheight*50, left,
        #                                         ['','острое','впервые в жизни установленное хроническое','ранее установленное хроническое'],self.DS_Type,label_margin=label_margin,field_size=fsize)
        left = 1
        self.vheight += 1
        fsize, label_margin = 2, 2
        #Close_Date
        self.Close_Date_filed = self.FH.add_date_field("Дата закрытия",self.vheight*50, left,self.Close_Date, default_value=QDate.currentDate(),label_margin=label_margin,field_size=fsize)

        left += (fsize + label_margin + self.mrg)
        fsize = 6
        #Notes
        self.Notes_filed = self.FH.add_big_line_field("Примечения", self.vheight * 50, left, self.Notes,
                                                          height=80,label_margin=label_margin,field_size=fsize)
        left += (fsize + label_margin + self.mrg)
        fsize = 15
        # Appointments
        self.Appointments_filed = self.FH.add_big_line_field("Назначения", self.vheight * 50, left, self.Appointments,
                                                          height=80,label_margin=label_margin,field_size=fsize)

    def DS_Type_button_clicked(self,button):
        self.DS_Type = button.text()

    def parse_data(self):
        #place data rom db to fields
        patient = self.DB.get_by_id(self.num_card)
        #patient = patients.get()
        self.lname = patient.get("Last_name")
        self.fname = patient.get("First_name")
        self.sname = patient.get("Second_name")
        self.snils = patient.get("SNILS")
        self.dob = patient.get("B_Date")
        self.sex = patient.get("Sex")
        self.card_num = patient.get("Card_num")
        self.kont = patient.get("Kont")
        self.Pass_Type = patient.get("Pass_Type")
        self.Pass_Series = patient.get("Pass_Series")
        self.Pass_Num = patient.get("Pass_Num")
        self.Subject = patient.get("Subject")
        self.District = patient.get("District")
        self.City = patient.get("City")
        self.Locality = patient.get("Locality")
        self.Street = patient.get("Street")
        self.House = patient.get("House")
        self.Flat = patient.get("Flat")
        self.Doctor = patient.get("Doctor")
        self.Work_type = patient.get("Work_type")
        self.Work = patient.get("Work")
        self.Work_Post = patient.get("Work_Post")
        self.DS_first = patient.get("DS_first")
        self.DS_first_code = patient.get("DS_first_code")
        self.Service = patient.get("Service")
        self.Service_code = patient.get("Service_code")
        self.DS_second = patient.get("DS_second")
        self.DS_second_code = patient.get("DS_second_code")
        self.DS_concom1 = patient.get("DS_concom1")
        self.DS_concom1_code = patient.get("DS_concom1_code")
        self.DS_concom2 = patient.get("DS_concom2")
        self.DS_concom2_code = patient.get("DS_concom2_code")
        self.DS_concom3 = patient.get("DS_concom3")
        self.DS_concom3_code = patient.get("DS_concom3_code")
        self.DS_Type = patient.get("DS_Type")
        self.Visit_Date = patient.get("Visit_Date")
        self.Close_Date = patient.get("Close_Date")
        self.DS_for_journal = patient.get("DS_for_journal")
        self.Notes = patient.get("Notes")
        self.Appointments = patient.get("Appointments")
        self.DS_concom1_for_journal = patient.get("DS_concom1_for_journal_filed")
        self.DS_concom2_for_journal = patient.get("DS_concom2_for_journal_filed")
        self.DS_concom3_for_journal = patient.get("DS_concom3_for_journal_filed")
        self.Address_full = patient.get("Address_full")
        self.DS_for_journal_full = patient.get("DS_for_journal_full")
        self.Num_visit = patient.get("Num_visit")
        self.Visit_type = patient.get("Visit_type")
        self.Polis_Series = patient.get("Polis_Series")
        self.Polis_Num = patient.get("Polis_Num")
        self.SMO = patient.get("SMO")

    def save_patient(self):
        #make dict wiht patint data
        patient = {}
        dignosys_full = ""
        patient["Last_name"] = self.lname_filed.text()
        patient["First_name"] = self.fname_filed.text()
        patient["Second_name"] = self.sname_filed.text()
        patient["SNILS"] = self.SNILS_filed.text()
        В = self.DBirth_filed
        Date = self.DBirth_filed.date()
        Date = Date.toString(Qt.DefaultLocaleShortDate)
        patient["B_Date"] = Date
        patient["Sex"] = self.sex
        patient["Card_num"] = self.CN_filed.text()
        patient["Kont"] = self.kont_filed.currentText()
        patient["Pass_Type"] = self.Pass_Type_filed.text()
        patient["Pass_Series"] = self.Pass_Series_filed.text()
        patient["Pass_Num"] = self.Pass_Num_filed.text()
        patient["Subject"] = self.Subject_filed.text()
        patient["District"] = self.District_filed.text()
        patient["City"] = self.City_filed.text()
        patient["Locality"] = self.Locality_filed.text()
        patient["Street"] = self.Street_filed.text()
        patient["House"] = self.House_filed.text()
        patient["Flat"] = self.Flat_filed.text()
        #doctor
        patient["Doctor"] = self.Doctor_filed.currentText().split(', ')[1]
        patient["Work_type"] = self.Work_type_filed.currentText()
        patient["Work"] = self.Work_filed.text()
        patient["Work_Post"] = self.Work_Post_filed.text()
        patient["DS_first"] = self.DS_first_filed.text()
        patient["DS_first_code"] = self.DS_first_code_filed.text()
        patient["Service"] = self.Service_filed.text()
        patient["Service_code"] = self.Service_code_filed.text()
        patient["DS_second"] = self.DS_second_filed.text()
        patient["DS_second_code"] = self.DS_second_code_filed.text()
        patient["DS_concom1"] = self.DS_concom1_filed.text()
        patient["DS_concom1_code"] = self.DS_concom1_code_filed.text()
        patient["DS_concom2"] = self.DS_concom2_filed.text()
        patient["DS_concom2_code"] = self.DS_concom2_code_filed.text()
        patient["DS_concom3"] = self.DS_concom3_filed.text()
        patient["DS_concom3_code"] = self.DS_concom3_code_filed.text()
        patient["DS_Type"] = self.DS_Type
        DateV = self.Visit_Date_filed.date()
        patient["Visit_Date"] = DateV.toString(Qt.DefaultLocaleShortDate)
        DateC = self.Close_Date_filed.date()
        patient["Close_Date"] = DateC.toString(Qt.DefaultLocaleShortDate)
        patient["DS_for_journal"] = self.DS_for_journal_filed.text()
        patient["Appointments"] = self.Appointments_filed.toPlainText()
        patient["Notes"] = self.Notes_filed.toPlainText()
        patient["DS_concom1_for_journal_filed"] = self.DS_concom1_for_journal_filed.text()
        patient["DS_concom2_for_journal_filed"] = self.DS_concom2_for_journal_filed.text()
        patient["DS_concom3_for_journal_filed"] = self.DS_concom3_for_journal_filed.text()
        patient["Address_full"] = self.fill_address()
        patient["DS_for_journal_full"] = self.fill_diagnosys()
        patient["DS_code_for_journal_full"] = self.fill_diagnosys_code()
        patient["Num_visit"] = self.Num_visit_filed.text()
        patient["Visit_type"] = self.Visit_type
        patient["Polis_Series"] = self.Polis_Series_filed.text()
        patient["Polis_Num"] = self.Polis_Num_filed.text()
        patient["SMO"] = self.SMO_filed.text()

        if not self.num_card:
            self.num_card = 'new'#str(int(list(patients.keys())[-1]) + 1)
        #save patint to DB
        self.num_card = self.DB.save_patient(patient,self.num_card)
        #refresh layout to update data in list view
        self.patlist.updatelist()
        if self.state == self.STATUS_NEW:
            self.default["Num_visit"] = int(self.Num_visit)+1
            self.DW.save(self.default)
        self.hide()
        self.show()
        #to do поправить каскадное переоткрытие интерфесов

    def fill_address(self):
        f_list = [self.Subject_filed,self.District_filed,self.City_filed,self.Locality_filed,self.Street_filed, self.House_filed,self.Flat_filed]
        address = ""
        for field in f_list:
            text = field.text()
            if text:
                if address:
                    address = f"{address}, {text}"
                else:
                    address = text
        return address

    def fill_diagnosys(self):
        f_list = [self.DS_for_journal_filed, self.DS_concom1_for_journal_filed,
                  self.DS_concom2_for_journal_filed, self.DS_concom3_for_journal_filed]
        diagnosys = ""
        for field in f_list:
            text = field.text()
            if text:
                if diagnosys:
                    diagnosys = f"{diagnosys}, {text}"
                else:
                    diagnosys = text
        return diagnosys

    def fill_diagnosys_code(self):
        f_list = [self.DS_second_code_filed,self.DS_concom1_code_filed,
                  self.DS_concom2_code_filed, self.DS_concom3_code_filed]
        diagnosys_code = ""
        for field in f_list:
            text = field.text()
            if text:
                if diagnosys_code:
                    diagnosys_code = f"{diagnosys_code}, {text}"
                else:
                    diagnosys_code = text
        return diagnosys_code

    def set_default(self):


        self.DS_first = self.default.get("DS_first")
        self.Pass_Type = self.default.get("Pass_Type")
        self.Service = self.default.get("Service")
        if self.Service:
            self.Service_code = self.default.get("Service").split(',')[0]
        if self.DS_first:
            self.DS_first_code = self.default.get("DS_first").split(',')[0]
        self.Appointments = self.default.get("Appointments")
        self.Num_visit = self.default.get("Num_visit")

    def print_ST(self):
        #launch printer for statistic bill
        patient = self.DB.get_by_id(self.num_card).copy()
        docID = patient.get("Doctor")
        if docID != "":
            doctor = self.refDb.get_doc_by_id(docID)
            patient["Doc_Spec"] = doctor.get("Spec")
            patient["Doc_name"] = f'{doctor.get("Last_name")} {doctor.get("First_name")[0]}.{doctor.get("Second_name")[0]}.'
            patient["Doc_code"] = docID
            patient["Doc_name_full"] = f'{doctor.get("Last_name")} {doctor.get("First_name")} {doctor.get("Second_name")}'
        else:
            patient["Doc_Spec"] = ""
            patient["Doc_name"] = ""
            patient["Doc_code"] = ""
        # if no value in field - no processing
        f_list = ['DS_first', 'DS_second', 'DS_concom1', 'DS_concom2','DS_concom3','Service']
        pattern = '[A-Z]\d{2}'
        pattern2 = '[А-Я]\d{2}'
        for field in f_list:
            DS_f = patient.get(field)
            if DS_f == "":
                patient[field] = ""
            elif re.match(pattern, DS_f) or re.match(pattern2, DS_f):
                try:
                    field_value = DS_f[len(DS_f.split(",")[0]) + 1::]
                    if len(field_value)>0:
                        patient[field] = field_value
                    else:
                        patient[field] = DS_f
                except:
                    patient[field] = DS_f
            else:
                patient[field] = DS_f
        path = self.default.get("file_path")
        today = datetime.date.today()
        self.filename = f"{path}/СтатТалон {patient['Last_name']}({self.num_card}) от {str(today)}.docx"
        try:
            printST(patient,self.filename)
        except:
            MB = QMessageBox()
            MB.setWindowTitle("Ошибка")
            MB.setText(f"При печати талона произошла ошибка. Удостоверьтесь, что файл стат талона закрыт!")
            MB.setIcon(QMessageBox.Critical)
            x = MB.exec_()
        self.open_doc(self.filename)

    def open_doc(self, docname):
        #open statistic bill
        if os.name == 'nt':
            os.startfile(f'"{docname}"')
            #subprocess.call(['cmd.exe', '/c', docname])
        elif os.name == 'posix':
            os.startfile(f'"{docname}"')

    def set_code_DS_first(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('mkd', text):
                self.DS_first_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.DS_first_code_filed.setText("")

    def set_code_DS_second(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('mkd', text):
                self.DS_second_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.DS_second_code_filed.setText("")

    def set_code_DS_add1(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('mkd', text):
                self.DS_concom1_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.DS_concom1_code_filed.setText("")

    def set_code_DS_add2(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('mkd', text):
                self.DS_concom2_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.DS_concom2_code_filed.setText("")

    def set_code_DS_add3(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('mkd', text):
                self.DS_concom3_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.DS_concom3_code_filed.setText("")

    def set_code_Service(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            text = send.text()
            # check if it's a reference value and show error message if it's not
            if self.refDb.check_list_value_exists('service', text):
                self.Service_code_filed.setText(send.text().split(',')[0])
            else:
                MB = QMessageBox()
                MB.setWindowTitle("Ошибка ввода")
                MB.setText(f'Введенное вами значение "{text}" отсутствует в списке услуг')
                MB.setIcon(QMessageBox.Critical)
                x = MB.exec_()
                send.setText("")
                self.Service_code_filed.setText("")
    def check_work(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            self.refDb.add_work(send.text())

    def check_diagnosys(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            self.refDb.add_diagnosys(send.text())

    def check_SMO(self):
        send = self.sender()
        if isinstance(send, QLineEdit):
            self.refDb.add_SMO(send.text())

