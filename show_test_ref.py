# Write the features, the list like description and the description infered by GPT-J in csv

import os
import pandas as pd
import re
import csv

def show(test_dir,gen_dir,output_dir):
    c=0
    df = pd.DataFrame(columns=["tags","generated-desc","list-desc"])
    for path in os.listdir(test_dir):
        full_path = os.path.join(test_dir, path)
        if os.path.isfile(full_path):
            with open(full_path,'r') as f:
                test = f.read()
            with open(os.path.join(output_dir, path)) as f:
                output = f.read()
            dict = re.search('({.+})', test).group(0)
            desc = re.search('description\:.+$',test).group(0)
            gen = re.search('description\:.+$',output).group(0)
            df.append([dict,gen,desc])
            c+=1
    res = df.to_csv(index = True)
    with open (output_dir + "results.csv",'w') as f:
        csv.writer(f).writerows(res)
        
             
test_dir = "/Users/niyoush/dataset_test_only/test/"
gen_dir = "/Users/niyoush/dataset_test_only/gen/"
output_dir = "/Users/niyoush/dataset_test_only/"
show(test_dir, gen_dir,output_dir)