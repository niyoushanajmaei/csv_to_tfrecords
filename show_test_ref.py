# Write the features, the list like description and the description infered by GPT-J in csv

# IMPORTANT
# THE RESULTS WRITTEN IN THE EXCEL FILE ARE ALWAYS IN THE SECOND SHEET OF THE DOCUMENT
# THE FIRST SHEET IS EMPTY. DELETE THAT ONE.

import os
import pandas as pd
import re
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def show(ref_dir,gen_dir,output_dir):
    c=0
    columns=["tags","generated-desc","list-desc"]
    df = pd.DataFrame(columns=columns)
    for path in os.listdir(gen_dir):
        full_path = os.path.join(gen_dir, path)
        if os.path.isfile(full_path) and re.search('product',full_path):
            with open(full_path,'r') as f:
                gen = f.read()
            with open(os.path.join(ref_dir, path),'r') as f:
                ref = f.read()
            #print(ref)
            #print(gen)
            desc = re.search('description\:.+\n',ref).group(0)
            feat = re.search('features\:.+description', gen).group(0)
            gen = re.search('description\:.+\n',gen).group(0)
            feat = clean_str(feat)
            gen = clean_str(gen)
            desc = clean_str(desc)
            df = df.append({"tags":feat,"generated-desc":gen,"list-desc":desc},ignore_index=True)
            c+=1
            #print(f"feat: {feat} \n, gen: {gen} \n, desc: {desc}")
            #print(df.head())
            #break
        
    wb= Workbook()
    ws=wb.active
    with pd.ExcelWriter(output_dir + "results.xlsx", engine="openpyxl") as writer:
        writer.book=wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        df.to_excel(writer,index=False)
        writer.save()    

    print("writing successful")

#remove openpyxl's illegal characters
def clean_str(st):
    st = ILLEGAL_CHARACTERS_RE.sub('', st)
    return st
                     
ref_dir = "/Users/niyoush/dataset_grifatti_test_only/ref/"
gen_dir = "/Users/niyoush/dataset_grifatti_test_only/gen/"
output_dir = "/Users/niyoush/dataset_grifatti_test_only/"
show(ref_dir,gen_dir,output_dir)