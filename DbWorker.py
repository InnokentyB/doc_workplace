#Class for work with patient database
import json
import os
import sqlite3

class DbWorker():
    def __init__(self):
        self.filename = 'data\patients.json'
        self.add_field_file = 'data\\add_fields.json'
        self.patients = None

    def get_db(self):
        with open(self.filename,'r', encoding="utf-8") as patient_file:
            self.patients = json.load(patient_file, encoding='utf-8')

    def get_by_id(self,id):
        if self.patients == None:
            self.get_db()
        patient = self.patients.get(id)
        return patient

    def get_all(self):
        if self.patients == None:
            self.get_db()
        return self.patients

    def save_patient(self, patient, id='new'):
        if id == 'new':
            id = str(int(list(self.patients.keys())[-1]) + 1)
        self.patients[id] = patient
        self.update_db()
        return id

    def update_db(self):
        with open(self.filename, 'w', encoding="utf-8") as patient_file:
            json.dump(self.patients, patient_file)

    def add_field(self, f_name, f_title, f_value = ""):
        patients = self.get_all()
        for cardnum, value in patients.items():
            if cardnum == "0000":
                value[f_name] = f_title
            else:
                value[f_name] = f_value
        self.update_db()

    def get_pat_by_view(self,view):# перенести в класс печати отображения
        pat_dict = {}
        patient_s = self.get_all()
        for key, value in patient_s.items():
            ins_dict = {}
            for field in view.values():
                ins_dict[field] = value.get(field)
            pat_dict[key] = ins_dict
        return pat_dict

    def get_pat_for_journal(self,fields): # перенести в класс печати
        pat_list = []
        patient_s = self.get_all()
        for key, value in patient_s.items():
            patient = []
            for field in fields:
                if field =="FIO":
                    patient.append(f'{ value.get("Last_name")} { value.get("First_name")} { value.get("Second_name")}')
                else:
                    patient.append(value.get(field))
            pat_list.append(patient)
        return pat_list

    def check_need_field_update(self):
        try:
            with open(self.add_field_file, 'r', encoding="utf-8") as field_file:
                self.fields = json.load(field_file, encoding='utf-8')
            need_update = True
        except:
            need_update = False
        return need_update

    def update_fields(self):
        for key, value in self.fields.items():
            self.add_field(key,value)
        os.remove(self.add_field_file)

    def update_dianosys(self):
        pats = self.get_all()
        i=0
        for pat in pats.values():
            if i==0:
                i+=1
                continue
            f_list = ['DS_for_journal', 'DS_concom1_for_journal',
                      'DS_concom2_for_journal', 'DS_concom3_for_journal']
            diagnosys = ""
            for field in f_list:
                text = pat.get(field)
                if text:
                    if diagnosys:
                        diagnosys = f"{diagnosys}, {text}"
                    else:
                        diagnosys = text
            pat["DS_for_journal_full"] = diagnosys
            f_list = ['DS_second_code', 'DS_concom1_code',
                      'DS_concom2_code', 'DS_concom3_code']
            diagnosys_code = ""
            for field in f_list:
                text = pat.get(field)
                if text:
                    if diagnosys_code:
                        diagnosys_code = f"{diagnosys_code}, {text}"
                    else:
                        diagnosys_code = text
            pat["DS_code_for_journal_full"] = diagnosys_code
            pat["Visit_type"] = "ВВК"
        self.patients = pats
        self.update_db()

    '''
    def get_filtered_patients(self, filter):
        df = pandas.read_json(self.filename, orient="index")
        filter_str = ""
        pattern = f"pat['Last_name'].str.contains('Бодров'))"
        for f_key, f_value in filter.items():
            if filter_str:
                filter_str = filter_str + (f'&({df[f_key].str.contains(f_value)})')
            else:
                filter_str = (f'({df[f_key].str.contains(f_value)})')
        df = df[filter_str]
        return
    '''
    def convert_db(self,path):
        conn = sqlite3.connect(f"{path}/patients.db")
        cursor = conn.cursor()
        #Create tune tables


class RefWorker():
    def __init__(self):
        self.doc_filename = 'data\doctors.json'
        self.region_filename = 'data\\region.json'
        self.mkd_filename = 'data\\mkd10_lite.json'
        self.services_filename = 'data\\services.json'
        self.works_filename = 'data\\works.json'
        self.diagnosys_filename = 'data\\diagnosys.json'
        self.SMO_filename = 'data\\SMO.json'
        self.docs = None
        self.regions = None
        self.mkd = None
        self.services = None
        self.works = None
        self.diagnosys = None
        self.SMO = None

    def get_doc_db(self):
        with open(self.doc_filename,'r', encoding="utf-8") as doc_file:
            self.docs = json.load(doc_file, encoding='utf-8')


    def get_doc_list(self):
        if self.docs == None:
            self.get_doc_db()
        return self.docs

    def get_doc_by_id(self, id):
        if self.docs == None:
            self.get_doc_db()
        if not id:
            id = self.get_default_doctor()
        doc = self.docs.get(id)
        return doc

    def get_regions_list(self):
        with open(self.region_filename,'r', encoding="utf-8") as reg_file:
            self.regions = json.load(reg_file, encoding='utf-8')
        return list(self.regions.values())

    def get_default_doctor(self):
        default = DefaultWorker()
        doc = default.get_default_doctor()
        return doc

    def get_mkd_list(self):
        with open(self.mkd_filename,'r', encoding="utf-8") as reg_file:
            self.mkd = json.load(reg_file, encoding='utf-8')
        return self.mkd

    def get_services_list(self):
        with open(self.services_filename, 'r', encoding="utf-8") as file:
            self.services = json.load(file, encoding='utf-8')
        return self.services

    def get_work_list(self):
        with open(self.works_filename, 'r', encoding="utf-8") as file:
            self.works = json.load(file, encoding='utf-8')
            self.works_count = len(self.works)
        return list(self.works)

    def add_work(self,work):
        if self.works == None:
            self.get_work_list()
        wset = set(self.works)
        wset.add(work)
        if len(wset) > self.works_count:
            self.works = wset
            self.update_works_db()

    def update_works_db(self):
        with open(self.works_filename, 'w', encoding="utf-8") as file:
            json.dump(list(self.works), file)

    def get_diagnosys_list(self):
        with open(self.diagnosys_filename, 'r', encoding="utf-8") as file:
            self.diagnosys = json.load(file, encoding='utf-8')
            self.diagnosys_count = len(self.diagnosys)
        return list(self.diagnosys)

    def add_diagnosys(self,diagnosys):
        if self.diagnosys == None:
            self.get_diagnosys_list()
        wset = set(self.diagnosys)
        wset.add(diagnosys)
        if len(wset) > self.diagnosys_count:
            self.diagnosys = wset
            self.update_diagnosys_db()

    def update_diagnosys_db(self):
        with open(self.diagnosys_filename, 'w', encoding="utf-8") as file:
            json.dump(list(self.diagnosys), file)

    def get_SMO_list(self):
        with open(self.SMO_filename, 'r', encoding="utf-8") as file:
            self.SMO = json.load(file, encoding='utf-8')
            self.SMO_count = len(self.SMO)
        return list(self.SMO)

    def add_SMO(self, SMO):
        if self.SMO == None:
            self.get_SMO_list()
        wset = set(self.SMO)
        wset.add(SMO)
        if len(wset) > self.SMO_count:
            self.SMO = wset
            self.update_SMO_db()

    def update_SMO_db(self):
        with open(self.SMO_filename, 'w', encoding="utf-8") as file:
            json.dump(list(self.SMO), file)

    def check_list_value_exists(self,reference,value):
        ref_dict = {
            "service": self.services_filename,
            "mkd": self.mkd_filename
        }
        try:
            filename = ref_dict.get(reference)
        except:
            return None
        with open(filename, 'r', encoding="utf-8") as file:
            file_value = set(json.load(file, encoding='utf-8'))
            if value in file_value:
                return True
            else:
                return False


class ViewWorker(): #гуглить контейнер зависимостей
    def __init__(self):
        self.patlist_filename = 'data\patlist.json'
        self.patlist = None

    def get_patlist_view(self):
        with open(self.patlist_filename,'r', encoding="utf-8") as patlist_file:
            self.patlist = json.load(patlist_file, encoding='utf-8')
        return self.patlist

class DefaultWorker():
    def __init__(self):
        self.default_filename = 'data\\default.json'
        self.add_default_filename = 'data\\add_fields_to_def.json'
        self.default = None
        self.fields = None

    def get_default_list(self):
        with open(self.default_filename,'r', encoding="utf-8") as delault_file:
            self.default = json.load(delault_file, encoding='utf-8')
        return self.default

    def get_default_doctor(self, param = "Doctor"):
        if self.default == None:
            self.get_default_list()
        doc = self.default.get(param)
        return doc

    def updateDB(self):
        with open(self.default_filename, 'w', encoding="utf-8") as file:
            json.dump(self.default, file)

    def save(self, default):
        self.default = default
        self.updateDB()

    def check_need_field_update(self):
        try:
            with open(self.add_default_filename, 'r', encoding="utf-8") as field_file:
                self.fields = json.load(field_file, encoding='utf-8')
            need_update = True
        except:
            need_update = False
        return need_update

    def update_fields(self):
        for key, value in self.fields.items():
            self.add_field(key,value)
        os.remove(self.add_default_filename)

    def add_field(self, f_name, f_title):
        default = self.get_default_list()
        default[f_name] = f_title
        self.updateDB()