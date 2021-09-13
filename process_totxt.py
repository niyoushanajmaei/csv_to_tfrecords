#To process the raw data remove the unnecessary tags and add useful ones 
#that are used in the description

from pandas import read_excel
from pathlib import Path
import numpy as np
import lxml.html

def read_csv():
    my_sheet = 'BatchImport' 
    file_name = '01_batch_import_Carrera.xlsx'
    df = read_excel(Path('raw_data',file_name), sheet_name = my_sheet,keep_default_na=False)
    cleaned = clean(df)
    return df

def clean(df):
    df["description_en"] = df["description-en"]
    to_keep=["brand","name","madein","category","subcategory","season",
            "color","bicolors","gender","description_en"]
    to_drop=[]
    for col in df.columns:
        if col not in to_keep:
            to_drop.append(col)
    df.drop(to_drop, inplace=True, axis=1)
    df.drop(df[df.description_en==""].index, inplace=True)
    df["description_en"] = df["description_en"].apply(erase_tags)
    return df

def erase_tags(str):
    return lxml.html.fromstring(str).text_content()


def write_as_txt(df):
   #Split the data Train 60%, Val 20%, Test 20%
   train, validate, test = np.split(df.sample(frac=1), [int(.6*len(df)), int(.8*len(df))])
   write(train, "train")
   write(validate,"validate")
   write(test,"test")

def write(df, type):
    dir ="/Users/niyoush/dataset/"
    if type=="train":
        path = dir+"train_text/"
    elif type=="validate":
        path = dir+"val_text/"
    elif type=="test":
        path = dir+"test_text/"
    
    c=0
    if not path:
        print("Wrong type")
    else:
        data= df.to_dict('index')
        for k,v in data.items():
            with open(path+"product"+str(c)+".txt", 'w') as f:
                print(v, file=f)
            print(c)
            c+=1
        

write_as_txt(read_csv())
