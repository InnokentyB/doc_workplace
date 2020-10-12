from openpyxl import Workbook
from openpyxl.styles import Border,Font,Side

def print_journal(data, filename, first_names = True):
    #receive data as list of lists - each lest is raw, in each row - fields
    #if first_names == True - first row containts columns name
    wb = Workbook()
    rows_count = len(data)
    colunmns_count = len(data[0])
    ws = wb.active
    BFont = Font(bold = True)
    double = Side(border_style="medium")
    Bord = Border(top=double, left=double, right=double, bottom=double)
    for r in range(0,rows_count):
        for c in range(0, colunmns_count):
            cell = ws.cell(row=r+1, column=c+1, value=data[r][c])
            if r == 0:
                cell.font = BFont
            cell.border = Bord


    wb.save(filename)
