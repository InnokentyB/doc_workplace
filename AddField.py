from DbWorker import DbWorker

def add_field():
    d = DbWorker()
    d.add_field("DS_for_journal_full", "Диагноз для журнала")
    d.add_field("DS_code_for_journal_full", "Код МКБ-10")

