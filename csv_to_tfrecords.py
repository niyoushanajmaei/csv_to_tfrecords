# read csv into a dict with format: 
# dict to tf.train.Features
# tf.train.Features to tf.train.Example
# write tf.train.Example to tf.records

#change both read and write directories before use

from pandas import read_excel
from pathlib import Path
import tensorflow as tf

def read_csv():
    my_sheet = 'BatchImport' 
    file_name = '09_batch_import_Versace_Jeans.xlsx'
    df = read_excel(Path('output',file_name), sheet_name = my_sheet,keep_default_na=False)
    data= df.to_dict('index') #each value in data is one instant of a product. (tags and description)
    return data

def write_as_record(data):
    c=0
    for k,v in data.items():
        ex_to_rec(create_example(v),c)
        print(c)
        c+=1

def create_example(dict):
    #dict is the data of one product with the following format
    #{'cat1':'tag1, 'cat2':'tag2',...}
    feature={}
    for k,v in dict.items():
        if(isinstance(v,str)):
            feature[k]=tf.train.Feature(bytes_list=tf.train.BytesList(
            value=[v.encode('utf-8')]))
        elif(isinstance(v,float)):
            feature[k]=tf.train.Feature(float_list=tf.train.FloatList(
            value=[v]))
        elif(isinstance(v,int)):
            feature[k]=tf.train.Feature(int64_list=tf.train.Int64List(
            value=[v]))        
    example = tf.train.Example(features=tf.train.Features(feature=feature))
    return example

def ex_to_rec(example,c):
    with tf.io.TFRecordWriter('val/val'+str(c+1)+'.tfrecord') as writer:
        writer.write(example.SerializeToString())

def read_tfrecord(file):
    #to check the created tfrecords
    raw_dataset = tf.data.TFRecordDataset(file)
    for raw_record in raw_dataset.take(1):
        example = tf.train.Example()
        example.ParseFromString(raw_record.numpy())
        print(example)

write_as_record(read_csv())


