from PyQt5.QtWidgets import QDialog, QPushButton, QFileDialog,QGridLayout, QTableWidget, QTableWidgetItem
from  PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect,Qt

from DbWorker import RefWorker
from FieldHelper import FieldHelper

class SelectReferenceDialog(QDialog):

    def __init__(self):
        super().__init__()
        # Put Geometry
        self.top = 50
        self.left = 50
        self.width = 900
        self.height = 900
        self.refdict = {
                    #"Врачи": "doctors",
                   #"Регионы": "region",
                   #"Услуги": "services",
                   "Места работы": "works",
                   "Диагнозы": "diagnosys",
                   "Страховые": "SMO"}
        #Set title
        self.setWindowTitle("Выберите справочник для редактирования")
        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))
        self.referenceButtons()

    def referenceButtons(self):
        leftmargin = 200

        for name, ref in self.refdict.items():
            button_dialog = QPushButton(name, self)
            geo_but_visit = QRect(leftmargin, 30, 150, 30)
            button_dialog.setGeometry(geo_but_visit)
            button_dialog.clicked.connect(self.RefIdentefier)
            leftmargin += 200

    def RefIdentefier(self):
        sender = self.sender().text()
        file = self.refdict.get(sender)+'.json'
        Reference = ShowRefForUpdate(file,sender)
        Reference.setModal(True)
        Reference.exec()

class ShowRefForUpdate(QDialog):
    def __init__(self,reffile, refname):
        super().__init__()
        # Put Geometry
        self.top = 50
        self.left = 50
        self.width = 1200
        self.height = 900
        self.reffile = reffile
        self.refname = refname
        self.fh = FieldHelper(self)
        self.rw = RefWorker()
        #Set title
        self.setWindowTitle(self.refname)
        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))
        self.reflist = self.rw.getRefByName(self.reffile)
        self.table = self.fh.get_table_from_list(self.reflist, self.refname, self.saveRef)
        # add grid with patients
        self.grid_layout = QGridLayout()

        self.table.resizeColumnsToContents()
        self.grid_layout.addWidget(self.table)
        #geo = QRect(self.left - 30, self.top + 30, self.width - 10, self.height - 10)
        #self.grid_layout.setGeometry(geo)
        self.setLayout(self.grid_layout)
        # add print button
        button_Print = QPushButton("Удалить строку", self)
        button_Print.setShortcut("Ctrl+D")
        button_Print.setShortcut("Delete")
        geo_but_prt = QRect(1450, 30, 150, 30)
        button_Print.setGeometry(geo_but_prt)
        button_Print.clicked.connect(self.removeRow)

    def removeRow(self):
        curRow = self.table.currentRow()
        self.table.removeRow(curRow)
        del self.reflist[curRow]
        self.rw.SaveRef(self.reffile, self.reflist)

    def saveRef(self):
        send = self.sender()
        RowNum = send.currentRow()
        item = send.item(RowNum, 0)
        value = item.text()
        self.reflist[RowNum] = value
        self.rw.SaveRef(self.reffile,self.reflist)
