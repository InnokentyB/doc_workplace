from PyQt5.QtWidgets import QDialog, QPushButton, QFileDialog
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
        self.setWindowTitle(refname)
        self.setWindowIcon(QtGui.QIcon("icon\Plague_Inc._logo.png"))
        reflist = self.rw.getRefByName(reffile)
        self.table = self.fh.get_table_from_list(reflist, refname, self.saveRef)


    def saveRef(self):
        pass

