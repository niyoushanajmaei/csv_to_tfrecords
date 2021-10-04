
import pandas as pd
from openpyxl import Workbook

def read_csv():
    my_sheet = 'BatchImport' 
    file_name = '09_batch_import_Versace_Jeans.xlsx'
    df = read_excel(Path('output',file_name), sheet_name = my_sheet,keep_default_na=False)
    cleaned = clean(df)
    data= cleaned.to_dict('index') #each value in data is one instant of a product. (tags and description)
    return data

def write(df,output_dir):
    wb= Workbook()
    ws=wb.active
    with pd.ExcelWriter(output_dir + "dataset.xlsx", engine="openpyxl") as writer:
        writer.book=wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        df.to_excel(writer,index=False)
        writer.save()    

    print("writing successful")