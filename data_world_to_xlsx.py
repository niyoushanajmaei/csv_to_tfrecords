
import datadotworld as dw
from openpyxl import Workbook
import pandas as pd
import utils

def amazon():
    dataset = dw.load_dataset('promptcloud/amazon-australia-product-listing')
    print(dataset.dataframes)
    query = "SELECT * FROM marketing_sample_for_amazon_com_au_ecommerce_au_20191101_20191130_30k_data WHERE product_category LIKE 'Clothing%'"
    fashion = dw.query('promptcloud/amazon-australia-product-listing', query)

    df = fashion.dataframe
    return df

def john_lewis():
    dataset = dw.load_dataset('crawlfeeds/john-lewis-partners-products-dataset')
    print(dataset.dataframes)
    query = "SELECT * FROM sheet WHERE Category LIKE '%Women%' OR Category LIKE '%Men%'"
    fashion = dw.query('crawlfeeds/john-lewis-partners-products-dataset', query)
    df = fashion.dataframe
    df["product_description"] = df["product_description"].apply(utils.remove_tags)
    return df


output_dir = "/Users/niyoush/data_world/clean_xlsx/john_lewis_2.xlsx"
#dataset = dw.load_dataset('crawlfeeds/john-lewis-partners-products-dataset')
#print(dataset.dataframes)
utils.write(john_lewis(),output_dir)

