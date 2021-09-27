#Read the generated descriptions
#remove "description" from the tags.
#remove name upto madein from tags
#append all read rows, shuffle and cut into train and validate and write features and generated columns into txt files.

import pandas as pd
from pandas import read_excel
from pathlib import Path
import numpy as np
import lxml.html
import string
import os
import re

def read_csv(path):
    #file_name = '02_batch_import_Dior.xlsx'
    #df = read_excel(Path(path,file_name), sheet_name = my_sheet,keep_default_na=False)
    df = pd.read_excel(path, sheet_name='Sheet1')
    return df

def write_as_txt(df,write_dir):
   # Shuffle indices and split the data Train 70%, val 30%
   df = df.iloc[np.random.permutation(len(df))]
   #TODO check if this is correct
   #train, validate= np.split(df.sample(frac=1), [int(.7*len(df))])
   train = df
   write(train, "train",write_dir)
   #write(validate,"validate",write_dir)
   #write(test,"test",write_dir)

def write(df, t,write_dir):
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
        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'}
        write_dict(value,path+"product"+str(c)+".txt","n")
        c+=1
    print("writing "+t+ " successful")

# writes the file with format:
# when type in "n" for normal
# {"tag1" : "value1", "tag2": "value2", ....} \n description: "description_en" \n ### \n
# when type is "t" for test
# {"tag1" : "value1", "tag2": "value2", ....} \n description: 
def write_dict(dict, path, type):
    feat,desc,gen = get_data(dict) # only write the features and the generated descriptions
    with open(path, 'w') as f:
        txt = feat + "\n"
        if type == "n":
            if txt[-1] != '\n':
                txt+='\n'
            txt += gen + "###\n"
        print(txt,file =f)

def get_data(dict):
    feat = dict.pop("tags", None)
    desc = dict.pop("list-desc", None)
    gen = dict.pop("generated-desc", None)
    feat = feat.replace("description","")
    if 'name' in feat:
        i = feat.split().index("name:")
        j = feat.split().index("madein:")
        remove=''
        for st in feat.split()[i:j]: 
            remove+=st +' '
        feat = feat.replace(remove,'')
    return feat,desc,gen

def df_stat(df):
    df["desc_len"] =df['description_en'].apply(lambda x: len(x))
    print(df["desc_len"].describe())
    # the third quartile of the length of the descriptions is 210

read_dir = "/Users/niyoush/accepted_results/TOP5_TEMP8_2_accepted.xlsx"
write_dir = "/Users/niyoush/accepted_results/"
write_as_txt(read_csv(read_dir),write_dir)
#test_write(read_csv())
#df_stat(read_batch())