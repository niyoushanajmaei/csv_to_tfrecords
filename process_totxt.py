#To process the raw data remove the unnecessary tags and add useful ones 
#that are used in the description

from pandas import read_excel
from pathlib import Path
import numpy as np
import lxml.html
import string

def read_csv():
    my_sheet = 'BatchImport' 
    file_name = '02_batch_import_Dior.xlsx'
    df = read_excel(Path('raw_data',file_name), sheet_name = my_sheet,keep_default_na=False)
    cleaned = clean(df)
    return df

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
    df["description_en"] = df["description_en"].apply(erase_tags)
    df = add_features(df)
    return df

def erase_tags(str):
    return lxml.html.fromstring(str).text_content()

def add_features(df):
    for index, row in df.iterrows():
        #add the material to features
        #the word that comes after "material"
        if "material" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("material")   
            row["material"] = row["description_en"].split()[i+1]
        
        #add UV protection
        #add the dimensions
        if "sunglasses" in row["description_en"].lower():
            dim = False
            if "uv" in row["description_en"].lower():
                row["uv"] = True
            if "anti-reflective" in row["description_en"].lower():
                row["anti-reflective"] = True
            if "diameter" in row["description_en"].lower() :
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("diameter")   
                d = row["description_en"].split()[i+1]
                dim = True
            if "width" in row["description_en"].lower(): 
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("width")   
                w = row["description_en"].split()[i+1]
                dim = True
            if "length" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("length")   
                l = row["description_en"].split()[i+1]
                dim = True
            if dim:
                row["dimensions"] = d +", "+w +", "+l +", "


        if "eau de toilette" in row["description_en"].lower():
            dim = False
            if "spray" in row["description_en"].lower():
                row["spray"] = True
            if "ml" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("ml")   
                v = row["description_en"].split()[i-1]
                dim = True
            if dim:
                row["dimensions"] = v
                print(v)
                print("here at " + str(index))

        if "shoes" in row["description_en"].lower():
            if "leather" in row["description_en"].lower():
                row["material"] = "leather"
            if "sole" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("sole")   
                row["sole"] = row["description_en"].split()[i-1]
            if "heel" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("heel")   
                row["heel"] = row["description_en"].split()[i-1]
       
        if "original box" in row["description_en"].lower():
            row["original_box"] = True

        if "100%" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("100%")   
            row["material"] = "100% "+ row["description_en"].split()[i+1]
        
        if "wash" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("wash")   
            row["wash"] = row["description_en"].split()[i+1]

        if "dimensions" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("dimensions")   
            j = i+2
            if "cm" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("cm")   
            if "mm" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("mm")   
            if "m" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("m")   
            row["dimensions"] = row["description_en"].split()[i+1:j]

        if "size" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("size")   
            j = i+2
            if "cm" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("cm")   
            if "mm" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("mm")   
            if "m" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("m")   
            row["size"] = row["description_en"].split()[i+1:j]

        if "neck" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("neck")   
                row["neck"] = row["description_en"].split()[i-1]

        if "sleeve" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("sleeve")   
                row["sleeve"] = row["description_en"].split()[i-1]

        if "strap" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("strap")   
                row["strap"] = row["description_en"].split()[i-1]
        
        if "handle" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("handle")   
                row["handle"] = row["description_en"].split()[i-1]

        if "fit" in row["description_en"].lower():
                i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("fit")   
                row["fit"] = row["description_en"].split()[i-1]
        
        if "model" in row["description_en"].lower():
            i = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("model")   
            j = i+2
            if "cm" in row["description_en"].lower():
                j = row["description_en"].lower().translate(str.maketrans('', '', string.punctuation)).split().index("cm")   
            row["model"] = row["description_en"].split()[i+1:j]
        

    return df

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
    ref_path = "/Users/niyoush/dataset/test_text_ref/"
    c=0
    if type == "test":
        #write the test set with and without the lables to have a reference
        data= df.to_dict('index')
        for k,v in data.items():
            with open(path+"product"+str(c)+".txt", 'w') as f:
                print(v, file=f)
                c+=1
        df["description_en"] = ""
        c=0
        data= df.to_dict('index')
        for k,v in data.items():
            with open(ref_path+"product"+str(c)+".txt", 'w') as f:
                print(v, file=f)
                c+=1 
    else :
        data= df.to_dict('index')
        for k,v in data.items():
            with open(path+"product"+str(c)+".txt", 'w') as f:
                print(v, file=f)
                c+=1
    print("writing "+type+ " successful")

def test_write(df):
    dir ="/Users/niyoush/dataset/train_text/"
    data= df.to_dict('index')
    c=0
    for k,v in data.items():
        with open(dir+"product"+str(c)+".txt", 'w') as f:
            print(v, file=f)
            c+=1
    print("writing successful")


#write_as_txt(read_csv())
test_write(read_csv())