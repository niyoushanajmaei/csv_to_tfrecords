import os

p =[]
d = "val"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        p.append(full_path)

with open('product_desc.val.index', 'w') as writer:
    for path in p:
        writer.write('gs://test-gpt-j/dataset/'+path+'\n')