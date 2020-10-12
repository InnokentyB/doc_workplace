#Receive JSON file with patient print information
from docxtpl import DocxTemplate
import jinja2
import datetime

def printST(patient, filename):

    Template_name = "StatSheetTemplate_new.docx"

    # Get Templete
    doc = DocxTemplate(Template_name)
    # Get today date
    today = datetime.date.today()
    Day = patient.get('Visit_Date').split('.')[0]
    Month = patient.get('Visit_Date').split('.')[1]
    Year = patient.get('Visit_Date').split('.')[2]

    # Get insurance number
    Polis_Series = patient.get('Polis_Series')
    Polis_Num = patient.get('Polis_Num')
    SMO = patient.get('SMO')
    SNILS = patient.get('SNILS')

    # Get patient name
    Num_card = patient.get('Card_num')
    Contingent = patient.get('Kont')
    Last_name = patient.get('Last_name')
    First_name = patient.get('First_name')
    Second_name = patient.get('Second_name')
    Sex = patient.get('Sex')
    Visit_type = patient.get('Visit_type')
    if Visit_type == "Первичный" or Visit_type == "Повторный":
        Visit_type =""

    # Get birthDate
    B_Day = patient.get('B_Date').split('.')[0]
    B_Month = patient.get('B_Date').split('.')[1]
    B_Year = patient.get('B_Date').split('.')[2]

    # Get passport document
    Pass_Series = patient.get('Pass_Series')
    Pass_Num = patient.get('Pass_Num')
    Pass_Type = patient.get('Pass_Type')

    # Get Adress
    Subject = patient.get('Subject')
    District = patient.get('District')
    City = patient.get('City')
    Locality = patient.get('Locality')
    Street = patient.get('Street')
    House = patient.get('House')
    if House:
        if len(House) > 10:
            House = House[0:10]
    Flat = patient.get('Flat')
    Phone = ''

    # Get job info
    Work = patient.get('Work')
    Work2 = ''
    # print(len(Work))
    if len(Work) > 50:
        Work2 = Work[50:]
        Work = Work[0:49]
        # print(Work2)
    Work_Post = patient.get('Work_Post')
    if len(Work2) > 0:
        Work_Post = Work2 + ', ' + Work_Post

    # Get Diagnosis
    DS_first = patient.get('DS_first')
    DS_first_code = patient.get('DS_first_code')
    DS_second = patient.get('DS_second')
    DS_second_code = patient.get('DS_second_code')
    DS_concom1 = patient.get('DS_concom1')
    DS_concom1_code = patient.get('DS_concom1_code')
    DS_concom2 = patient.get('DS_concom2')
    DS_concom2_code = patient.get('DS_concom2_code')
    DS_concom3 = patient.get('DS_concom3')
    DS_concom3_code = patient.get('DS_concom3_code')

    # Get Doctor
    Doc_Spec = patient.get('Doc_Spec')
    Doc_name = patient.get('Doc_name')
    Doc_code = patient.get('Doc_code')
    Doc_name_full = patient.get('Doc_name_full')

    # Get Service
    Service = patient.get('Service')
    Service_code = patient.get('Service_code')

    #Get illness type
    type_ill = patient.get('DS_Type')
    type0 = (type_ill == "")
    type1 = (type_ill == "острое")
    type2 = (type_ill == "впервые в жизни установленное хроническое")
    type3 = (type_ill == "ранее установленное хроническое")

    #Get work type
    type_work = patient.get('Work_type')
    wtype1 = (type_work == "работает")
    wtype2 = (type_work == "проходит военную службу или приравненную к ней службу")
    wtype3 = (type_work == "пенсионер(ка)")
    wtype4 = (type_work == "студент(ка)")
    wtype5 = (type_work == "не работает")
    wtype6 = (type_work == "прочие")


    # Create context
    context = {
        'Day': Day,
        'Month': Month,
        'Year': Year,
        'In_Series': Polis_Series,
        'In_Num': Polis_Num,
        'Last_name': Last_name,
        'First_name': First_name,
        'Second_name': Second_name,
        'man': Sex=='муж',
        'B_Day': B_Day,
        'B_Month': B_Month,
        'B_Year': B_Year,
        'Pass_Series': Pass_Series,
        'Pass_Num': Pass_Num,
        'Num_card': Num_card,
        'Contingent': Contingent,
        'SMO': SMO,
        'SNILS': SNILS,
        'Pass_Type': Pass_Type,
        'Subject': Subject,
        'District': District,
        'City': City,
        'Locality': Locality,
        'Street': Street,
        'House': House,
        'Phone': Phone,
        'Work': Work,
        'Work_Post': Work_Post,
        'DS_first': DS_first,
        'DS_first_code': DS_first_code,
        'DS_second': DS_second,
        'DS_second_code': DS_second_code,
        'DS_concom1': DS_concom1,
        'DS_concom1_code': DS_concom1_code,
        'DS_concom2': DS_concom2,
        'DS_concom2_code': DS_concom2_code,
        'DS_concom3': DS_concom3,
        'DS_concom3_code': DS_concom3_code,
        'Doc_Spec': Doc_Spec,
        'Doc_name': Doc_name,
        'Doc_code': Doc_code,
        'Service': Service,
        'Service_code': Service_code,
        'type0': type0,
        'type1': type1,
        'type2': type2,
        'type3': type3,
        'Doc_name_full': Doc_name_full,
        'wtype1': wtype1,
        'wtype2': wtype2,
        'wtype3': wtype3,
        'wtype4': wtype4,
        'wtype5': wtype5,
        'wtype6': wtype6,
        'Flat': Flat,
        'Visit_type': Visit_type,
        'Pass_Type': Pass_Type
    }

    doc.render(context)
    doc.save(filename)
    #self.OpenDoc(filename)


