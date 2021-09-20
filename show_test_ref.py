# Write the features, the list like description and the description infered by GPT-J in csv

import os
import pandas as pd
import re
from pandas import ExcelWriter
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def show(gen_dir,output_dir):
    c=0
    columns=["tags","generated-desc"]
    df = pd.DataFrame(columns=columns)
    for path in os.listdir(gen_dir):
        full_path = os.path.join(gen_dir, path)
        if os.path.isfile(full_path) and re.search('product',full_path):
            with open(full_path,'r') as f:
                gen = f.read()
            #print(ref)
            #print(gen)
            feat = re.search('features\:.+description', gen).group(0)
            gen = re.search('description\:.+\n',gen).group(0)
            feat = clean_str(feat)
            gen = clean_str(gen)
            df = df.append({"tags":feat,"generated-desc":gen},ignore_index=True)
            c+=1

        wb= Workbook()
        ws=wb.active
        with pd.ExcelWriter(output_dir+"results.xlsx", engine="openpyxl") as writer:
            writer.book=wb
            writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
            df.to_excel(writer,index=False)
            writer.save()
    print("writing successful")


def clean_str(st):
    st = ILLEGAL_CHARACTERS_RE.sub('', st)
    return st
                     
gen_dir = "/Users/niyoush/dataset_test_only/gen/"
output_dir = "/Users/niyoush/dataset_test_only/"
show(gen_dir,output_dir)