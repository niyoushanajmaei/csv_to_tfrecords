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
import utils

def read_batch(read_dir):
    dfs = []
    c=0
    for path in os.listdir(read_dir):
        full_path = os.path.join(read_dir, path)
        if os.path.isfile(full_path):
            dfs.append(read_csv(read_dir,path))
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

    # I deleted name from this column.
    to_keep=["brand","madein","category","subcategory","season",
            "color","bicolors","gender","neckline","sleeves","pattern","fastening","sole","pockets","description_en","dimensions","material",
            "uv","spray","anti-reflective","original_box","wash","sole","neck","sleeve"
            ,"strap","handle","fit","heel","model"]
    to_drop=[]
    for col in df.columns:
        if col not in to_keep:
            to_drop.append(col)
    df.drop(to_drop, inplace=True, axis=1)
    df.drop(df[df.description_en==""].index, inplace=True)
    df["description_en"] = df["description_en"].apply(utils.remove_tags)
    df = add_features(df)
    return df

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
            
        except:
            # Does it matter? and why does this happen?
            # yes it matters. happens because we need to add space between potential words
            # These instances will be deleted from the dataset
            to_delete.append(index)
    df = df.drop(to_delete,axis=0)
    print(f"deleted {len(to_delete)} rows. remaining: {len(df.index)}")
    return df

def clean_txt(st):
    d = {'Occhiali da sole':'sunglasses','Orologio':'watch',"'season': 'ss'":"'season': 'spring/summer'","'":'',"{":'',"}":'','sandali':'sandals','Sciarpe':'scarf'
        ,'Tracolla':'shoulder bag','Infradito':'flip-flops','Ciabatte':'slippers','Portafoglio':'wallet','Portafogli':'Wallet','Portadocumenti':'Document Holder','A mano': 'handbag',
        'Sandali':'sandals','Custodia':'Cover','Zeppa':'wedge','A spalla':'Shoulder Bag','Cintura':'Belt','Pochette':'clutch','Mocassino':'Mocassin','Borse':'Bags'
        ,'Caschi':'helmets','Da viaggio':'travel bag',"Stivaletto":"Boots","Stivale":"Boots","Giacca":"Jacket","Portachiavi":"Key holder","Pantaloni":"Pants","Zaini":"Back-pack"
        ,'Maglia':'Knitwear','season: fw':'season: Fall Winter',"Felpa":"Sweatshirt","Intimo":"Underwear","Cappello":"Hat","Uomo":"Man","Donna":"Woman","Francia":"France"
        ,"Camicia":"Shirt","Giubbotto":"Jacket","Gonna":"Skirt","Abito":"Dress","Vestito":"Dress","Tutina":"Tracksuit","Scarpe":"Shoes","Stringate":"Lace Up","Canotta":"Tank top"
        ,'Ballerine':'Ballet Shoes',"Tuta":"Tracksuit","Borsa":"Bag"}
    for k,v in d.items():
        st = st.replace(k,v)
    st = st.strip()
    if 'watch' in st:
        st = st.replace('strap', 'material')
    return st

def write_as_txt(df,write_dir):
   # Shuffle indices and split the data Train 60%, Val 20%, Test 20%
   df = df.iloc[np.random.permutation(len(df))]
   train, validate, test = np.split(df.sample(frac=1), [int(.6*len(df)), int(.8*len(df))])
   write(train, "train",write_dir)
   write(validate,"validate",write_dir)
   write(test,"test",write_dir)

def write(df, t,write_dir):
    dir = write_dir
    if t=="train":
        path = dir+"train_text/"
    elif t=="validate":
        path = dir+"val_text/"
    elif t=="test":
        path = dir+"test_text/"
    ref_path = dir + "test_text_ref/"
    c=0
    data= df.to_dict('index')
    if t == "test":
        #write the test set with and without the lables to have a reference
        for k,value in data.items():
            value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'}
            write_dict(value,ref_path+"product"+str(c)+".txt","n")
            c+=1
        c=0
        for k,value in data.items():
            value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'}
            write_dict(value,path+"product"+str(c)+".txt","t")
            c+=1 
    else :
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
    desc = dict.pop("description_en", None)
    with open(path, 'w') as f:
        txt = str(dict) + "\ndescription: "
        txt = clean_txt(txt)
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

read_dir = "/Users/niyoush/csv_to_tfrecords/raw_data/"
write_dir = "/Users/niyoush/dataset/"
write_as_txt(read_batch(read_dir),write_dir)
#test_write(read_csv())
#df_stat(read_batch())