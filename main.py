import xmltodict
import json
import pandas as pd
import csv
import logging
import time
import argparse
import os
import ntpath
import json
import ast
from openpyxl.workbook import Workbook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
    #AQUÍ EMPIEZAN LOS REPLACES. COGE HASTA 50 REGISTROS. CADA REGISTRO ESTA FORMADO POR UN RECORD Y UNA ERROR.

    data = []

    text = text.replace("#","")

    text = text.replace("Record 50","record").replace("Record 49","record").replace("Record 48","record").replace("Record 47","record").replace("Record 46","record").replace("Record 45","record").replace("Record 44","record").replace("Record 43","record").replace("Record 42","record").replace("Record 41","record")

    text = text.replace("Record 40","record").replace("Record 39","record").replace("Record 38","record").replace("Record 37","record").replace("Record 36","record").replace("Record 35","record").replace("Record 34","record").replace("Record 33","record").replace("Record 32","record").replace("Record 31","record")

    text = text.replace("Record 30","record").replace("Record 29","record").replace("Record 28","record").replace("Record 27","record").replace("Record 26","record").replace("Record 25","record").replace("Record 24","record").replace("Record 23","record").replace("Record 22","record").replace("Record 21","record")

    text = text.replace("Record 20","record").replace("Record 19","record").replace("Record 18","record").replace("Record 17","record").replace("Record 16","record").replace("Record 15","record").replace("Record 14","record").replace("Record 13","record").replace("Record 12","record").replace("Record 11","record")

    text= text.replace("Record 10","record").replace("Record 9","record").replace("Record 8","record").replace("Record 7","record").replace("Record 6","record").replace("Record 5","record").replace("Record 4","record").replace("Record 3","record").replace("Record 2","record").replace("Record 1","record").replace("Record 0","record")

    text = text.replace('"',"'").replace("Error record","{'error':{'message':'").replace(":'",':"')

    text = text.replace("record","{'record':").replace('<?xml','"<?xml').replace('JOBPROFILE_DELTA_INTEGRATION>','JOBPROFILE_DELTA_INTEGRATION>"},')

    text = text.replace("tns1:","").replace(":tns1","").replace("ns1:","").replace("ns2:","").replace(":ns1","").replace(":ns2","").replace("","")

    text = text.replace(", Subentity and Input:","''', 'Subentity and Input':").replace("'''",'"').replace('<Message xmlns','"<Message xmlns')

    s = f'</Message>"'+'}'+'}'+','

    text = text.replace('</Message>',f'{s}')

    text = text.split('},')

    text = text[:-1]

    for item in text:

        item = item.replace('</JOBPROFILE_DELTA_INTEGRATION>"','</JOBPROFILE_DELTA_INTEGRATION>"}')

        item = " ".join(item.split())

        item = convert_xml_to_dictionary(item)

        data.append(item)

    return data

def convert_xml_to_dictionary(text):

    dictionary = {}

    try:
        dictionary = ast.literal_eval(text)    

    except:
        text = text[9:]
        text = ast.literal_eval(text)
        dictionary['error'] = text

    return dictionary

# This method just read the xml. Within the code we have an other method called clean_text(). 
# Clean text give the code the correct format before reading.
def read_xml(name_file):
    with open(name_file, 'r',encoding='utf-8-sig') as text:
        doc = text.read()
        new_text = clean_text(doc)

    return new_text

# This method is to create a structured dictionary that allows us to obtain the information in a simple and orderly way.
def write_json_error(data):

    xml = xmltodict.parse(data['Subentity and Input'])

    xml['Message']['Elements']['message'] = data['message']
    xml['Message']['Elements']['@xmlns'] = xml['Message']['@xmlns']
    del xml['Message']['@xmlns']

    new_data = json.dumps(xml)

    return new_data

# This method is to create a structured dictionary that allows us to obtain the information in a simple and orderly way.
def write_json_record(data):
    
    xml = xmltodict.parse(data)
    new_data = json.dumps(xml)
    return new_data

# This method is to format the json before create the dataframe.
def format_json_error(file):

    df = pd.read_json(file)

    columns = list(df['Message']['Elements'].keys())
    dictionary = {}

    for item in columns:            
        dictionary[item] = df['Message']['Elements'][item]

    return dictionary

# This method is to format the json before create the dataframe.
def format_json_record(file):

    df = pd.read_json(file)

    columns = list(df['JOBPROFILE_DELTA_INTEGRATION']['JobProfile']['Job_Profile'].keys())

    dictionary = {}

    for item in columns:            
        dictionary[item] = df['JOBPROFILE_DELTA_INTEGRATION']['JobProfile']['Job_Profile'][item]

    return dictionary

# This method serves to ensure that each row has the same number of fields. This is necessary to create the dataframe
def check_columns(data):

    main_element = len(data[0])
    main_position = 0

    for ix,item in enumerate(data):
        if len(item) > main_element:
            main_element = len(item)
            main_position = ix

    columns = list(data[main_position].keys())
    
    for item in data:
        for key in columns:
            if key not in item.keys():
                item[key] = ''

    return data

# This method created the new tables .xlsx. Create a table for errors, and other for records.
def create_dataframe(data_record, data_error,name_xml):

    logger.info('Creating Dataframe....')
    if data_record:
        data_record = check_columns(data_record)
        df_record = pd.DataFrame(data_record)
        df_record.to_excel(f"excel_results/{name_xml}/records.xlsx", sheet_name = 'records')

    if data_error:
        data_error = check_columns(data_error)
        df_error = pd.DataFrame(data_error)
        df_error.to_excel(f"excel_results/{name_xml}/errors.xlsx", sheet_name = 'errors')
    
    logger.info('Dataframe created')

# This is the main method where we use all the methods mentioned before in the right order. 
def main():

    parser = argparse.ArgumentParser()
  
    parser.add_argument('--name-xml', help='', required=True)

    args = parser.parse_args()
    logging.info(f"Arguments received: {args}")

    config = {'name_xml': args.name_xml}

    name_xml = str(config["name_xml"]).replace(".xml","")

    os.makedirs(f'excel_results', exist_ok= True)
    os.makedirs(f"excel_results/{name_xml}", exist_ok = True)

    t0 = time.time()
    data_record = []
    data_error = []
    logger.info('Reading .xml....')
    table = read_xml(f"xml_files/{config['name_xml']}")
    logger.info('.xml readed')
    for item in table:
        for key in item:
            if key == 'error':                
                data = item[key] 
                new_data = write_json_error(data)
                row = format_json_error(new_data)
                data_error.append(row)
            
            if key == 'record':
                xml = item[key] 
                new_data = write_json_record(xml)
                row = format_json_record(new_data)
                data_record.append(row)

                    
    create_dataframe(data_record, data_error,name_xml)

    t1 = time.time()
    logger.info('.xmls created')
    logger.info(f'Total processing time {t1-t0}')

if __name__ == '__main__':

    main()
    
