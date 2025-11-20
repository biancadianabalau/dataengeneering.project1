import requests
import numpy as np
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import sqlite3
import psycopg2


log_file = "log_file.txt" 


def extract_from_csv(file_to_process): 
    dataframe = pd.read_csv(file_to_process) 
    return dataframe 
  
def extract_from_json(file_to_process): 
    dataframe = pd.read_json(file_to_process, lines=True) 
    return dataframe 
  
def extract_from_xml(file_to_process): 
    dataframe = pd.DataFrame(columns=[
        "customer_id", 
        "store_name", 
        "transaction_date", 
        "aisle", 
        "product_name", 
        "quantity", 
        "unit_price", 
        "total_amount"
    ]) 
    tree = ET.parse(file_to_process) 
    root = tree.getroot() 
    for record in root: 
        customer_id = record.find("customer_id").text 
        store_name = record.find("store_name").text 
        transaction_date = record.find("transaction_date").text 
        aisle = record.find("aisle").text 
        product_name = record.find("product_name").text 
        quantity = float(record.find("quantity").text) 
        unit_price = float(record.find("unit_price").text) 
        total_amount = float(record.find("total_amount").text)
        dataframe = pd.concat([dataframe, pd.DataFrame([{
                "customer_id": customer_id,
                "store_name": store_name,
                "transaction_date": transaction_date,
                "aisle": aisle,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount
            }])], ignore_index=True)
 
    return dataframe 

def extract(csv_file, json_file,xml_file): 
    extracted_data = pd.DataFrame(columns=[
        "customer_id", 
        "store_name", 
        "transaction_date", 
        "aisle", 
        "product_name", 
        "quantity", 
        "unit_price", 
        "total_amount"
    ]) # create an empty data frame to hold extracted data  
         
   # extract from single CSV
    df_csv = extract_from_csv(csv_file)
    extracted_data = pd.concat([extracted_data, df_csv], ignore_index=True)
    
    # extract from single JSON
    df_json = extract_from_json(json_file)
    extracted_data = pd.concat([extracted_data, df_json], ignore_index=True)
    
    # extract from single XML
    df_xml = extract_from_xml(xml_file)
    extracted_data = pd.concat([extracted_data, df_xml], ignore_index=True)
    
    return extracted_data
       




