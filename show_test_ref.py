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
    columns=["url","tags","generated-desc","list-desc"]
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
            code = re.search('code:.+\n',ref).group(0)
            desc = re.search('description\:.+\n',ref).group(0)
            feat = re.search('features\:.+description', gen).group(0)
            gen = re.search('description:.+\n',gen).group(0)
            #if (re.search('description\:.+?###',gen,re.DOTALL)):
            #    gen = re.search('description\:.+?###',gen,re.DOTALL).group(0)
            #else:
            #    gen = re.search('description\:.+$',gen,re.DOTALL).group(0)
            feat = clean_str(feat)
            gen = clean_str(gen)
            desc = clean_str(desc)
            code = clean_str(code)
            feat = feat.replace('description','')
            gen = gen.replace("read more","")
            gen = gen.replace('[0m','')
            df = df.append({"url":f"=HYPERLINK(\"https://www.griffati.com/it/product/{str(code.split()[1])}\")","tags":feat,"generated-desc":gen,"list-desc":desc},ignore_index=True)
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
                     
ref_dir = "/Users/niyoush/griffati_with_material/ref/"
gen_dir = "/Users/niyoush/griffati_with_material/gen/"
output_dir = "/Users/niyoush/griffati_with_material/"
show(ref_dir,gen_dir,output_dir)