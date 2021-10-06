
import pandas as pd
from openpyxl import Workbook
import lxml.html
import re
import utils

def read_csv(read_dir):
    df = pd.read_csv(read_dir)
    df = clean(df)
    return df

def clean(df):
    df["product_descrition"] = df["product_descrition"].apply(utils.remove_tags)
    #df = ebay_clean(df)
    return df

def ebay_clean(df):
    #only keep the fashio products which have the product information in the description column.
    index_to_keep = []
    for index, row in df.iterrows():
        if "Clothes, Shoes & Accessories" in row["breadcrumbs"] :
            index_to_keep.append(index)
    df = df.loc[index_to_keep]
    return df
        

read_dir = "/Users/niyoush/data_world/home_sdf.csv"
output_dir = "/Users/niyoush/data_world/clean_xlsx/"
utils.write(read_csv(read_dir),output_dir)