import pandas as pd
from openpyxl import Workbook

def write(df,output_dir):
    wb= Workbook()
    ws=wb.active
    with pd.ExcelWriter(output_dir + "amazon_fixed.xlsx", engine="openpyxl") as writer:
        writer.book=wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        df.to_excel(writer,index=False)
        writer.save()    

    print("writing successful")

read_dir = "/Users/niyoush/data_world/clean_xlsx/amazon.xlsx"
write_dir = "/Users/niyoush/data_world/clean_xlsx/"

df = pd.read_csv(read_dir,encoding = 'unicode_escape')
df2 = pd.DataFrame(df["records"])

write(df2,write_dir)