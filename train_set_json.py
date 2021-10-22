
import pandas as pd
from pandas import read_excel
from pathlib import Path
import numpy as np
import json

def read_csv(path):
    #file_name = '02_batch_import_Dior.xlsx'
    #df = read_excel(Path(path,file_name), sheet_name = my_sheet,keep_default_na=False)
    df = pd.read_excel(path, sheet_name='Sheet1')
    df.reset_index(drop=True, inplace=True)
    return clean(df)

def clean(df):
    to_keep=["brand","category","description","color","gender","pattern","neckline","sleeves","material"]
    to_drop=[]
    for col in df.columns:
        if col not in to_keep:
            to_drop.append(col)
    df.drop(to_drop, inplace=True, axis=1)
    return df

def write_as_json(df,write_dir,name):
   # Shuffle indices and split the data Train 70%, val 30%
   df = df.iloc[np.random.permutation(len(df))]
   #TODO check if this is correct
   #train, validate= np.split(df.sample(frac=1), [int(.7*len(df))])
   train = df
   write(train, "train",write_dir,name)
   #write(validate,"validate",write_dir)
   #write(test,"test",write_dir)

def write(df, t,write_dir,name):
    dict_list=[]
    dir = write_dir
    if t=="train":
        path = dir+"train_text/"
    elif t=="validate":
        path = dir+"val_text/"
    #elif t=="test":
    #    path = dir+"test_text/"
    #ref_path = dir+"test_text_ref/"
    c=0
    data= df.to_dict('index')
    #if t == "test":
    #    #write the test set with and without the lables to have a reference
    #    for k,value in data.items():
    #        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'}
    #        write_dict(value,ref_path+"product"+str(c)+".txt","n")
    #        c+=1
    #    c=0
    #    for k,value in data.items():
    #        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'}
    #        write_dict(value,path+"product"+str(c)+".txt","t")
    #        c+=1 
    #else :
    for k,value in data.items():
        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null' and str(v)!=  '[]'}
        #write_dict(value,path+"product"+str(c)+".txt","n")
        dict_list.append(value)
        c+=1
    json_output = {"data":dict_list}
    write_json(write_dir,json_output,name)
    

def write_json(dir,dict,name):
    with open(dir + name + ".jsonl", 'w') as f:
        json.dump(dict, f)
    print("writing json successful")

read_dir = "/Users/niyoush/accepted_results/TOP5_TEMP8_2_accepted.xlsx"
write_dir = "/Users/niyoush/accepted_results/"
name = "gptj"
write_as_json(read_csv(read_dir),write_dir,name)
