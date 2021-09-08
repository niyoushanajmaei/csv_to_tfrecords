import os

p =[]
d = "train"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isdir(full_path):
        for path_path in os.listdir(full_path):
            full_full_path = os.path.join(d, path,path_path)
            if os.path.isfile(full_full_path):
                p.append(full_full_path)

with open('product_desc.train.index', 'w') as writer:
    for path in p:
        writer.write('gs://test-gpt-j/dataset/'+path+'\n')