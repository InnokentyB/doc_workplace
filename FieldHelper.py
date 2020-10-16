from  PyQt5.QtCore import QDate, Qt, QRect
from PyQt5.QtWidgets import ( QLineEdit, QDateEdit,QLabel, QCalendarWidget, QListWidget, QComboBox, QGroupBox,
                              QCompleter, QPlainTextEdit, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem,)
from PyQt5.QtGui import QFont


class FieldHelper():
    LABEL_FONT_SIZE = 8

    def __init__(self, parent,refDb = None):
        self.refDb = refDb
        self.parent = parent
        self.width_step = 50
        self.field_size = 4


    def add_line_field(self ,f_title ,top ,left ,default_value ,widthchange = 0, readonly = False, label_margin = 2,
                       label_font_size = LABEL_FONT_SIZE, field_size = 4):
        # control for base line edit field, set geometry, label
        label = QLabel(self.parent)
        label.setText(f_title)
        font = QFont()
        font.setPointSize(label_font_size)
        label.setFont(font)
        geo_label = QRect(left*self.width_step, top, label_margin*self.width_step, 30)
        label.setGeometry(geo_label)
        field = QLineEdit(self.parent)
        geo_field = QRect((left +label_margin)*self.width_step, top, field_size*self.width_step, 30)
        field.setGeometry(geo_field)
        field.setText(str(default_value))
        field.setReadOnly(readonly)
        return field

    def add_cbox_field(self, f_title, top, left, items, default_value ,widthchange = 0 ,readonly = False, label_margin = 2,
                       label_font_size = LABEL_FONT_SIZE, field_size = 4):
        # add control to combobox field, set geometry, label and items
        label = QLabel(self.parent)
        label.setText(f_title)
        font = QFont()
        font.setPointSize(label_font_size)
        label.setFont(font)
        geo_label = QRect(left*self.width_step, top, label_margin*self.width_step, 30)
        label.setGeometry(geo_label)
        field = QComboBox(self.parent)
        field.addItems(items)
        geo_field = QRect((left +label_margin)*self.width_step, top, field_size*self.width_step, 30)
        field.setGeometry(geo_field)
        field.setCurrentText(str(default_value))
        field.setEditable(not readonly)
        return field

    def add_date_field(self, f_title, top, left, f_date, widthchange=0, need_calendar = True, default_value = QDate(1980, 1, 1)
                       ,readonly = False, label_margin = 2, label_font_size = LABEL_FONT_SIZE, field_size = 4):
        label = QLabel(self.parent)
        label.setText(f_title)
        font = QFont()
        font.setPointSize(label_font_size)
        label.setFont(font)
        geo_label = QRect(left*self.width_step, top, label_margin*self.width_step, 30)
        label.setGeometry(geo_label)
        field = QDateEdit(self.parent)
        field.setCalendarPopup(need_calendar)
        geo_field = QRect((left +label_margin)*self.width_step, top, field_size*self.width_step, 30)
        field.setGeometry(geo_field)
        if f_date:
            Defdate = QDate(int(f_date.split('.')[2]), int(f_date.split('.')[1]), int(f_date.split('.')[0]))
        else:
            Defdate = default_value
        field.setDate(Defdate)
        field.setReadOnly(readonly)
        return field

    def add_doc_field(self, f_title, top, left ,default_value, label_margin = 2, label_font_size = LABEL_FONT_SIZE, field_size = 4):
        # special field for displaing doctor at the form, contains doc name (Last+First+Second) and docs personal number
        self.docs = self.refDb.get_doc_list()
        doc_list = []
        i = 0
        for key ,value in self.docs.items():
            if i > 0:
                doc = self.format_doc_to_field(key ,value)
                doc_list.append(doc)
            i += 1
        docfield = self.add_cbox_field( f_title, top, left, doc_list ,default_value, 80, label_margin= label_margin, label_font_size=label_font_size,
                                        field_size = field_size)
        return docfield

    def add_big_line_field(self ,f_title ,top ,left, default_value, label_pos = 'left', height=30 ,widthchange = 0, readonly = False,
                           label_margin = 2, label_font_size = LABEL_FONT_SIZE, field_size = 4):
        # control for base line edit field, set geometry, label
        label = QLabel(self.parent)
        label.setText(f_title)
        font = QFont()
        font.setPointSize(label_font_size)
        label.setFont(font)
        geo_label = QRect(left*self.width_step, top, label_margin*self.width_step, 30)
        label.setGeometry(geo_label)
        field = QPlainTextEdit(self.parent)
        if label_pos == 'left':
            geo_field = QRect((left +label_margin)*self.width_step, top, field_size*self.width_step, height)
        else:
            geo_field = QRect(left, top +50, 200 + widthchange, height)
        field.setGeometry(geo_field)
        field.setPlainText(str(default_value))
        field.setReadOnly(readonly)
        return field



    def add_compliter_line_field(self ,f_title, top, left, items, default_value, widthchange = 0 ,readonly = False,
                                 label_margin = 2, label_font_size = LABEL_FONT_SIZE, field_size = 4, callback = None):
        # make line edit field with compliter, including items
        field = self.add_line_field(f_title, top, left, default_value, widthchange ,readonly, label_margin=label_margin,
                                    label_font_size=label_font_size, field_size = field_size)
        compliter = QCompleter(items)
        compliter.setCaseSensitivity(0)
        compliter.setCompletionMode(0)
        q = compliter.filterMode()
        compliter.setFilterMode(Qt.MatchContains)
        field.setCompleter(compliter)

        if callback:
            field.editingFinished.connect(callback)

        return field

    def add_radio_button_field(self, f_title, top, left, items, default_value ,layout = 'vertical', label_margin = 2,
                       label_font_size = LABEL_FONT_SIZE, field_size = 4):
        # add control to radio button field, set geometry, label and items
        label = QLabel(self.parent)
        label.setText(f_title)
        font = QFont()
        font.setPointSize(label_font_size)
        label.setFont(font)
        geo_label = QRect(left*self.width_step, top, label_margin*self.width_step, 30)
        label.setGeometry(geo_label)
        i = 0
        button_group = QButtonGroup(self.parent)
        for but in items:
            button = QRadioButton(self.parent)
            if layout == 'vertical':
                geo_button = QRect((left +label_margin)*self.width_step, top+(i)*10, field_size*self.width_step, 30)
                i+=2
            else:
                add = round((len(but)/7),0)
                geo_button = QRect((left + label_margin+i+1) * self.width_step, top, field_size * self.width_step, 30)
                i+=1
                i+=add
            button.setText(but)
            if but==default_value:
                button.setChecked(True)
            button.setGeometry(geo_button)
            button_group.addButton(button)
        return button_group

    def format_doc_to_field(self ,id, doc):
        # make special format for doc field
        doctor = f'{doc.get("Last_name")} {doc.get("First_name")} {doc.get("Second_name")}, {id}'
        return doctor

    def get_doc_to_field(self ,id):
        # get value for doc field
        doctor = self.refDb.get_doc_by_id(id)
        doctor = self.format_doc_to_field(id ,doctor)
        return doctor

    def get_table_from_list(self,list_ref,name, action = None):
        self.table = QTableWidget(self.parent)
        i=0
        a = 0
        self.table.insertRow(i)
        self.table.setItem(i - 1, a, QTableWidgetItem(name))
        i+=1
        for str in list_ref:
            self.table.setItem(i, a, QTableWidgetItem(str))
            i += 1
        if action:
            self.table.currentCellChanged.connect(action)
        return self.table