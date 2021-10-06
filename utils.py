from openpyxl import Workbook
import lxml.html
import re
import pandas as pd

def write(df, output_dir):
    wb= Workbook()
    ws=wb.active
    with pd.ExcelWriter(output_dir + "home_sdf.xlsx", engine="openpyxl") as writer:
        writer.book=wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        df.to_excel(writer,index=False)
        writer.save()    

    print("writing successful")

def remove_tags(st):
    st =  lxml.html.fromstring(st).text_content()
    st = re.sub(r"(\w)([A-Z])", r"\1 \2", st)
    return re.sub(r"\s+", " ",st)
