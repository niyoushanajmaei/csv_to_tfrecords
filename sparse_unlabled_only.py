# Produces a labled set for reference and an unlabled test set
# Differs from process_to_txt.py in:
# Writes only unlabled test and the corresponding labeled reference
# With an even distribution of data over all catalogs
# All the italian tags are translated to English which was critical.

import pandas as pd
from pandas import read_excel
from pathlib import Path
import numpy as np
import lxml.html
import string
import os
import re



def read_batch(read_dir,limit):
    dfs = []
    c=0
    for path in os.listdir(read_dir):
        full_path = os.path.join(read_dir, path)
        if os.path.isfile(full_path):
            dfs.append(read_csv(read_dir,path))
            c+=1
            print("read file #"+ str(c)) 

    for i in range(len(dfs)):
        dfs[i] = dfs[i].sample(min(limit,len(dfs[i].index)))
    
    df = pd.concat(dfs)
    #print(len(df.index))
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

    #name and category were removed.
    to_keep=["brand","code","madein","subcategory","season",
            "color","bicolors","gender","neckline","neck_shirt","sleeves","pattern","fastening","sole","pockets","description_en","dimensions","material",
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
    materials = []
    for index, row in df.iterrows():
        # A version of the description, all low case, all punctuations removed
        # The possible words are separated after removing the punctuations
        desc_procs = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation))
        desc_procs = separate_words(desc_procs)
        if len(desc_procs) < 30:
            to_delete.append(index)
        try:
            #if "material" in desc_procs:
            #    i = desc_procs.split().index("material")   
            #    row["material"] = desc_procs.split()[i+1]
            
            material = add_material(desc_procs)
            materials.append(str(material))
            if (material == "[]") :
                to_delete.append(index)
            #print(material)

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
            
            #if "neck" in desc_procs:
            #        i = desc_procs.split().index("neck")   
            #        row["neck"] = desc_procs.split()[i-1]
#
            #if "sleeve" in desc_procs:
            #        i = desc_procs.split().index("sleeve")   
            #        row["sleeve"] = desc_procs.split()[i-1]

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
    df["material"] = materials
    df = df.drop(to_delete,axis=0)
    #print(df.material.to_string(index = False))
    print(f"deleted {len(to_delete)} rows. remaining: {len(df.index)}")
    return df

def add_material(desc):
    all_materials = ["canvas","cashmere","chenille","chiffon","cotton","crêpe","crepe","damask","georgette","gingham","jersey",
                    "lace","leather","linen","wool","modal","muslin","organza","polyester","satin","silk","spandex","suede","taffeta",
                    "toile","tweed","twill","velvet","viscose","synthetic matrials"]
    materials =  []
    for m in all_materials:
        if m in desc:
            materials.append(m)
    return materials

def clean_txt(st):
    d = {'Occhiali da sole':'sunglasses','Orologio':'watch',"'season': 'ss'":"'season': 'spring/summer'","'":'',"{":'',"}":'','sandali':'sandals','Sciarpe':'scarf'
        ,'Tracolla':'shoulder bag','Infradito':'flip-flops','Ciabatte':'slippers','Portafoglio':'wallet','Portafogli':'Wallet','Portadocumenti':'Document Holder','A mano': 'handbag',
        'Sandali':'sandals','Custodia':'Cover','Zeppa':'wedge','A spalla':'Shoulder Bag','Cintura':'Belt','Pochette':'clutch','Mocassino':'Mocassin','Borse':'Bags'
        ,'Caschi':'helmets','Da viaggio':'travel bag',"Stivaletto":"Boots","Stivale":"Boots","Giacca":"Jacket","Portachiavi":"Key holder","Pantaloni":"Pants","Zaini":"Back-pack"
        ,'Maglia':'Knitwear','season: fw':'season: Fall Winter',"Felpa":"Sweatshirt","Intimo":"Underwear","Cappello":"Hat","Uomo":"Man","Donna":"Woman","Francia":"France"
        ,"Camicia":"Shirt","Giubbotto":"Jacket","Gonna":"Skirt","Abito":"Dress","Vestito":"Dress","Tutina":"Tracksuit","Scarpe":"Shoes","Stringate":"Lace Up","Canotta":"Tank top"
        ,'Ballerine':'Ballet Shoes',"Tuta":"Tracksuit","Borsa":"Bag","Sciarpa":"Scarf"}
    for k,v in d.items():
        st = st.replace(k,v)
    st = st.strip()
    if 'watch' in st:
        st = st.replace('strap', 'material')
    st = st.replace("slip on","")
    st = st.replace('"','')
    st = st.replace('[','')
    st = st.replace(']','')
    st = st.replace("'",'')
    return st

def write(df,write_dir):
    path = write_dir + "test/"
    ref_path = write_dir + "ref/"
    c=0
    #print(df.material.to_string(index = False))
    data= df.to_dict('index')
    #write the test set with and without the lables to have a reference
    for k,value in data.items():
        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null' and str(v)!= '[]'}
        write_dict(value,ref_path+"product"+str(c)+".txt","n")
        c+=1
    c=0
    for k,value in data.items():
        value = {k:v for k,v in value.items() if str(v)!= '' and str(v).strip() != '' and str(v)!='nan' and str(v)!='null'and str(v)!= '[]'}
        write_dict(value,path+"product"+str(c)+".txt","t")
        c+=1 
    print("writing successful")

# writes the file with format:
# when type in "n" for normal
# {"tag1" : "value1", "tag2": "value2", ....} \n description: "description_en" \n ### \n
# when type is "t" for test
# {"tag1" : "value1", "tag2": "value2", ....} \n description: 
def write_dict(dict, path, type):
    desc = dict.pop("description_en", None)
    code = dict.pop("code",None)
    with open(path, 'w') as f:
        txt = ""
        if type == "n":
            txt += f"code: {code}\n"
        txt += f"features: {str(dict)} \ndescription: "
        txt = clean_txt(txt)
        if type == "n":
            txt += desc + "\n###\n"
        print(txt,file =f)

def test_write(df):
    dir ="/Users/niyoush/dataset_test_only/test/"
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
    # the third quartile of the length of the descriptions is 165

limit = 10
read_dir = "/Users/niyoush/raw_data_grifatti/Done/"
write_dir = "/Users/niyoush/griffati_with_material/"
write(read_batch(read_dir,limit),write_dir)
#test_write(read_csv())
#df_stat(read_batch())