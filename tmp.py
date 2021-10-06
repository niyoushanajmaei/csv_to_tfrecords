import re


read_dir = "/Users/niyoush/data_world/amazon.json"
write_dir = "/Users/niyoush/data_world/"

with open (read_dir,"r") as f:
   st = f.read()
st= st.replace("=>",":")
st = st.replace('""','')
st = st.replace('\\"','')
st = st.replace('\\','"')
st = st.replace('"n        "n              "n                ','')
st = st.replace('""n','"n')
st = st.replace('"n"','n"')
st = st.replace('"nThis','This')
st = st.replace('""','')
st = st.replace(":nil",':""')
st= st.replace('nil,','"",')
st = st.replace(', nil',',""')
st = st.replace(',nil',',""')
st = st.replace(':,',':"",')
st = st.replace('"n    "n    ','')
st = st.replace('"u{1F9E4}','')
st = st.replace(r"([a-z]|[A-Z])\"([a-z]|[A-Z])",'')
st = st.replace('€"u','')
#while r"\\([a-z]|[A-Z])" in st:
#   st = st.replace(r"\\([a-z]|[A-Z])",'')
st = st.replace('\\','')

with open(write_dir + "amazon_fixed.json","w") as f:
   f.write(st)


