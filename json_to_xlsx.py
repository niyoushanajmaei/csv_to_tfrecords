import json
import pandas as pd
from openpyxl import Workbook

def read(dir):
    dfs = []
    df = pd.DataFrame()
    # reading the JSON data using json.load()
    with open(dir) as f:
        dict = json.load(f)
    #for k,d in dict.items():
    #    for dd in d:
    #        dfs.append(pd.DataFrame(dd, index =[0]))
    df = pd.DataFrame(dict)
    #print(df.head())
    #df = pd.concat(dfs)
    return df

def write(df,output_dir):
    wb= Workbook()
    ws=wb.active
    with pd.ExcelWriter(output_dir + "dataset.xlsx", engine="openpyxl") as writer:
        writer.book=wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        df.to_excel(writer,index=False)
        writer.save()    

    print("writing successful")


read_dir = "/Users/niyoush/data_world/flipkart_fashion_products_dataset.json"
output_dir = "/Users/niyoush/data_world/"
write(read(read_dir),output_dir)