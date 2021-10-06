import re

with open ("/Users/niyoush/data_world/clean_xlsx/ready/train_text/concat.txt","r") as f:
    st = f.read()

print(len(re.findall(r"###", st)))