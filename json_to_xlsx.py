import json
import pandas as pd
from openpyxl import Workbook
import extract
import utils

def read(dir):
    dfs = []
    df = pd.DataFrame()
    # reading the JSON data using json.load()
    with open(dir) as f:
        data = f.read()
        dict =  json.loads(data)
    #for k,d in dict.items():
    #    for dd in d:
    #        dfs.append(pd.DataFrame(dd, index =[0]))
    df = pd.DataFrame(dict)
    #print(df.head())
    #df = pd.concat(dfs)
    df = clean_flipkart(df)
    return df

def clean_flipkart(df):
    df = df.drop_duplicates(subset=['description'])
    df = df.dropna(subset=['description'])
    index_to_delete = []
    new_desc = []
    for index,row in df.iterrows():
        new_desc.append(row["description"].encode("ascii", errors="ignore").decode())
        if row["description"] == "" or len(row["description"]) < 100:
            index_to_delete.append(index)
    df = df.assign(description=new_desc)
    df = df.drop(index_to_delete)
    df["color"] = df["description"].apply(extract.color)
    df["category"] = df["description"].apply(extract.category)
    df["gender"] = df["description"].apply(extract.gender)
    df["pattern"] = df["description"].apply(extract.pattern)
    df["neckline"]= df["description"].apply(extract.neckline)
    df["sleeves"] = df["description"].apply(extract.sleeves)
    df["material"] = df["description"].apply(extract.material)
    col_to_delete = []
    for c in df.columns:
        if c not in ["brand","color","category","gender","pattern","neckline","sleeves","material","description"]:
            col_to_delete.append(c)
    df = df.drop(col_to_delete,axis=1)
    df = df.dropna(subset=['category'])
    return df



read_dir = "flipkart_fashion_products_dataset.json"
output_dir = "/Users/niyoush/data_world/clean_xlsx/"
utils.write(read(read_dir),output_dir)