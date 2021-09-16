# To process the raw data remove the unnecessary tags and add useful ones 
# that are used in the description

import pandas as pd
from pandas import read_excel
from pathlib import Path
import numpy as np
import lxml.html
import string
import os
import re

def read_batch():
    dfs = []
    p =[]
    d = "/Users/niyoush/csv_to_tfrecords/raw_data/"
    c=0
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            dfs.append(read_csv(d,path))
            c+=1
            print("read file #"+ str(c)) 
    df = pd.concat(dfs)
    df.reset_index(drop=True, inplace=True)
    return df

def read_csv(path,file_name):
    my_sheet = 'BatchImport' 
    #file_name = '02_batch_import_Dior.xlsx'
    df = read_excel(Path(path,file_name), sheet_name = my_sheet,keep_default_na=False)
    return clean(df)


def clean(df):
    
    df["material"] = ""
    df["dimensions"] = ""
    df["uv"] = ""
    df["spray"] = ""
    df["anti-reflective"] = ""
    df["original_box"] = ""
    df["wash"] =""
    df["sole"] = ""
    df["neck"] = ""
    df["sleeve"] =""
    df["strap"] =""
    df["handle"] =""
    df["fit"] =""
    df["heel"]=""
    df["model"]=""

    df["description_en"] = df["description-en"]

    to_keep=["brand","name","madein","category","subcategory","season",
            "color","bicolors","gender","description_en","dimensions","material",
            "uv","spray","anti-reflective","original_box","wash","sole","neck","sleeve"
            ,"strap","handle","fit","heel","model"]
    to_drop=[]
    for col in df.columns:
        if col not in to_keep:
            to_drop.append(col)
    df.drop(to_drop, inplace=True, axis=1)
    df.drop(df[df.description_en==""].index, inplace=True)
    df["description_en"] = df["description_en"].apply(erase_tags).apply(separate_words).apply(remove_spaces)
    df = add_features(df)
    return df

def erase_tags(st):
    return lxml.html.fromstring(st).text_content()

def separate_words(st):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", st)

def remove_spaces(st):
    return re.sub(r"\s+", " ",st)

def add_features(df):
    to_delete=[]
    for index, row in df.iterrows():
        # A version of the description, all low case, all punctuations removed
        # The possible words are separated after removing the punctuations
        desc_procs = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation))
        desc_procs = separate_words(desc_procs)
        if len(desc_procs) < 30 :
            to_delete.append(index)
        try:
            if "material" in desc_procs:
                i = desc_procs.split().index("material")   
                row["material"] = desc_procs.split()[i+1]
            
            if "sunglasses" in desc_procs:
                dim = False
                if "uv" in desc_procs or "protection" in desc_procs:
                    row["uv"] = True
                if "anti-reflective" in desc_procs:
                    row["anti-reflective"] = True
                if "diameter" in desc_procs :
                    i = desc_procs.split().index("diameter")   
                    d = desc_procs.split()[i+1]
                    dim = True
                if "width" in desc_procs: 
                    i = desc_procs.split().index("width")   
                    w = desc_procs.split()[i+1]
                    dim = True
                if "length" in desc_procs:
                    i = desc_procs.split().index("length")   
                    l = desc_procs.split()[i+1]
                    dim = True
                if dim:
                    row["dimensions"] = d +", "+w +", "+l +", "


            if "eau de toilette" in desc_procs:
                dim = False
                if "spray" in desc_procs:
                    row["spray"] = True
                if "ml" in desc_procs:
                    i = desc_procs.split().index("ml")   
                    v = desc_procs.split()[i-1]
                    dim = True
                if dim:
                    row["dimensions"] = v

            if "shoes" in desc_procs:
                if "leather" in desc_procs:
                    row["material"] = "leather"
                if "sole" in desc_procs:
                    i = desc_procs.split().index("sole")   
                    row["sole"] = desc_procs.split()[i-1]
                if "heel" in desc_procs:
                    i = desc_procs.split().index("heel")   
                    row["heel"] = desc_procs.split()[i-1]
        
            if "original box" in desc_procs:
                row["original_box"] = True

            if "100%" in desc_procs:
                i = desc_procs.split().index("100%")   
                row["material"] = "100% "+ desc_procs.split()[i+1]
            
            if "wash" in desc_procs:
                i = desc_procs.split().index("wash")   
                row["wash"] = desc_procs.split()[i+1]

            if "dimensions" in desc_procs:
                i = desc_procs.split().index("dimensions")   
                j = i+2
                if "cm" in desc_procs:
                    j = desc_procs.split().index("cm")   
                if "mm" in desc_procs:
                    j = desc_procs.split().index("mm")   
                if "m" in desc_procs:
                    j = desc_procs.split().index("m")   
                row["dimensions"] = desc_procs.split()[i+1:j]

            if "size" in desc_procs:
                i = desc_procs.split().index("size")   
                j = i+2
                if "cm" in desc_procs:
                    j = desc_procs.split().index("cm")   
                if "mm" in desc_procs:
                    j = desc_procs.split().index("mm")   
                if "m" in desc_procs:
                    j = desc_procs.split().index("m")   
                row["size"] = desc_procs.split()[i+1:j]

            if "neck" in desc_procs:
                    i = desc_procs.split().index("neck")   
                    row["neck"] = desc_procs.split()[i-1]

            if "sleeve" in desc_procs:
                    i = desc_procs.split().index("sleeve")   
                    row["sleeve"] = desc_procs.split()[i-1]

            if "strap" in desc_procs:
                    i = desc_procs.split().index("strap")   
                    row["strap"] = desc_procs.split()[i-1]
            
            if "handle" in desc_procs:
                    i = desc_procs.split().index("handle")   
                    row["handle"] = desc_procs.split()[i-1]

            if "fit" in desc_procs:
                    i = desc_procs.split().index("fit")   
                    row["fit"] = desc_procs.split()[i-1]
            
            if "model" in desc_procs:
                i = desc_procs.split().index("model")   
                j = i+2
                if "cm" in desc_procs:
                    j = desc_procs.split().index("cm")   
                    row["model"] = desc_procs.split()[i+1:j]
        except:
            # Does it matter? and why does this happen?
            # yes it matters. happens because we need to add space between potential words
            # These instances will be deleted from the dataset
            to_delete.append(index)
    df = df.drop(to_delete,axis=0)
    print(f"deleted {len(to_delete)} rows. remaining: {len(df.index)}")
    return df

def write_as_txt(df):
   # Shuffle indices and split the data Train 60%, Val 20%, Test 20%
   df = df.iloc[np.random.permutation(len(df))]
   train, validate, test = np.split(df.sample(frac=1), [int(.6*len(df)), int(.8*len(df))])
   write(train, "train")
   write(validate,"validate")
   write(test,"test")

def write(df, t):
    dir ="/Users/niyoush/dataset/"
    if t=="train":
        path = dir+"train_text/"
    elif t=="validate":
        path = dir+"val_text/"
    elif t=="test":
        path = dir+"test_text/"
    ref_path = "/Users/niyoush/dataset/test_text_ref/"
    c=0
    data= df.to_dict('index')
    if t == "test":
        #write the test set with and without the lables to have a reference
        for k,value in data.items():
            value = {k:v for k,v in value.items() if v!= '' or v.strip() != ''}
            write_dict(value,ref_path+"product"+str(c)+".txt","n")
            c+=1
        c=0
        for k,v in data.items():
            value = {k:v for k,v in value.items() if v!= '' or v.strip() != ''}
            write_dict(value,path+"product"+str(c)+".txt","t")
            c+=1 
    else :
        for k,value in data.items():
            value = {k:v for k,v in value.items() if v!= '' or v.strip() != ''}
            write_dict(value,path+"product"+str(c)+".txt","n")
            c+=1
    print("writing "+t+ " successful")

# writes the file with format:
# when type in "n" for normal
# {"tag1" : "value1", "tag2": "value2", ....} \n description: "description_en" \n ### \n
# when type is "t" for test
# {"tag1" : "value1", "tag2": "value2", ....} \n description: 
def write_dict(dict, path, type):
    desc = dict.pop("description_en", None)
    with open(path, 'w') as f:
        txt = str(dict) + "\ndescription: "
        if type == "n":
            txt += desc + "\n###\n"
        print(txt,file =f)

def test_write(df):
    dir ="/Users/niyoush/dataset/train_text/"
    data= df.to_dict('index')
    c=0
    for k,v in data.items():
        with open(dir+"product"+str(c)+".txt", 'w') as f:
            print(v, file=f)
            c+=1
    print("writing successful")

def df_stat(df):
    df["desc_len"] =df['description_en'].apply(lambda x: len(x))
    print(df["desc_len"].describe())
    # the third quartile of the length of the descriptions is 210

write_as_txt(read_batch())
#test_write(read_csv())
#df_stat(read_batch())