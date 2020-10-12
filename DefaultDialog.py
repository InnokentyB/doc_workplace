from PyQt5.QtWidgets import QDialog, QPushButton, QFileDialog
from  PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect,Qt

import sys
from DbWorker import DefaultWorker, RefWorker, DbWorker
from FieldHelper import  FieldHelper

class DefaultvalueDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Put Geometry
        self.top = 50
        self.left = 50
        self.width = 900
        self.height = 900

        #Set title
        self.setWindowTitle("Значения по умолчанию")
        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))

        #init fields
        self.vheight = 1
        self.step = 40
        self.Doctor_filed = ""


        #init db
        self.refDB = RefWorker()
        self.defDB = DefaultWorker()
        self.FH = FieldHelper(self, self.refDB)
        self.services = self.refDB.get_services_list()
        self.mkd = self.refDB.get_mkd_list()

        #init def fields
        self.default_values()
        self.default_fields()
        self.buttons()

    def default_values(self):
        default = self.defDB.get_default_list()
        self.Doctor = default.get('Doctor')
        self.Pass_Type = default.get('Pass_Type')
        self.DS_first = default.get('DS_first')
        self.Service = default.get('Service')
        self.file_path = default.get('file_path')
        self.Appointments = default.get('Appointments')
        self.Num_visit = default.get('Num_visit')
        self.Need_update = default.get('Need_update')

    def default_fields(self):
        label_margin = 3
        self.Doctor_filed = self.FH.add_doc_field("Врач", self.vheight * self.step, 1, self.FH.get_doc_to_field(self.Doctor), field_size=5,label_margin=label_margin)
        self.vheight += 1
        self.Pass_Type_filed = self.FH.add_line_field("Тип документа", self.vheight * self.step, 1, self.Pass_Type, label_margin=label_margin)
        self.vheight += 1
        self.DS_first_filed = self.FH.add_compliter_line_field("Первичн. диагноз", self.vheight * self.step, 1,self.mkd, self.DS_first, field_size=8, label_margin=label_margin)
        self.vheight += 1
        self.Service_filed = self.FH.add_compliter_line_field("Услуга", self.vheight * self.step, 1,self.services, self.Service, field_size=8, label_margin=label_margin)
        self.vheight+=1
        self.Appointments_filed = self.FH.add_line_field("Назначения", self.vheight * self.step, 1, self.Appointments, label_margin=label_margin)
        self.vheight += 1
        self.Num_visit_filed = self.FH.add_line_field("Следующ. номер посещения", self.vheight * self.step, 1, self.Num_visit, label_margin=label_margin)
        self.vheight += 1
        self.file_path_filed = self.FH.add_line_field("Папка для талонов", self.vheight * self.step, 1, self.file_path, readonly=True, field_size=6, label_margin=label_margin)
        ###

    def save_default(self):
        default = {}
        default["Doctor"] = self.Doctor_filed.currentText().split(', ')[1]
        default["Pass_Type"] = self.Pass_Type_filed.text()
        default["DS_first"] = self.DS_first_filed.text()
        default["Service"] = self.Service_filed.text()
        default["file_path"] = self.file_path_filed.text()
        default["Appointments"] = self.Appointments_filed.text()
        default["Num_visit"] = self.Num_visit_filed.text()
        default["Need_update"] = self.Need_update
        self.defDB.save(default)

    def buttons(self):
        self.vheight += 1
        button = QPushButton("Сохранить значения", self)
        geo_but = QRect(50, self.vheight *self.step, 150, 30)
        button.setGeometry(geo_but)
        button.setShortcut("Ctrl+S")
        # add cancel button
        button_Cancel = QPushButton("Закрыть", self)
        geo_but_сan = QRect(250, self.vheight *self.step, 150, 30)
        button_Cancel.setGeometry(geo_but_сan)
        button_Cancel.setShortcut("Ctrl+Q")

        if self.Need_update != "":
            # add update num button
            button_U = QPushButton("Обновить номера посещений", self)
            geo_but_u = QRect(550, self.vheight *self.step, 250, 30)
            button_U.setGeometry(geo_but_u)
            button_U.clicked.connect(self.update_num)

        # add open directory button
        button_open = QPushButton("Выбрать папку", self)
        geo_but_сan = QRect(500, (self.vheight-1) * self.step, 150, 30)
        button_open.setGeometry(geo_but_сan)
        button_open.setShortcut("Ctrl+O")

        button.clicked.connect(self.save_default)
        button_Cancel.clicked.connect(self.close)
        button_open.clicked.connect(self.file_dialog)

    def file_dialog(self):
        self.file = QFileDialog()
        if self.file_path != '':
            self.file.setDirectory(str(self.file_path))
        self.file.setFileMode(2)
        self.file.setOption(QFileDialog.ShowDirsOnly, True)
        if self.file.exec_() == QDialog.Accepted:
            path = self.file.selectedFiles()[0]  # returns a list
        else:
            path = self.file_path
        self.file_path = path
        self.file_path_filed.setText(path)

    def update_num(self):
        if self.Num_visit:
            DB = DbWorker()
            pat_list = DB.get_all()
            for pat in pat_list.values():
                if pat['Last_name'] !="Фамилия":
                    pat['Num_visit'] = str(self.Num_visit)
                    self.Num_visit =int(self.Num_visit)+1
            DB.patients = pat_list
            DB.update_db()
            self.Need_update = ""
            self.Num_visit_filed.setText(self.Num_visit)
            self.save_default()

