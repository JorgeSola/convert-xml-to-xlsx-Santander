import xmltodict
import json
import pandas as pd
import csv
from replace import clean_text
import logging
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# WRITE YOUR FILE_NAME HERE <'file_name'>
xml_name ='data.xml'

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
def create_dataframe(data_record, data_error):

    logger.info('Creating Dataframe....')
    if data_record:
        data_record = check_columns(data_record)
        df_record = pd.DataFrame(data_record)
        df_record.to_excel('excel_results/records.xlsx', sheet_name = 'records')

    if data_error:
        data_error = check_columns(data_error)
        df_error = pd.DataFrame(data_error)
        df_error.to_excel('excel_results/errors.xlsx', sheet_name = 'errors')
    
    logger.info('Dataframe created')

# This is the main method where we use all the methods mentioned before in the right order. 
def main():

    t0 = time.time()
    data_record = []
    data_error = []
    logger.info('Reading .xml....')
    table = read_xml(f'xml_files/{xml_name}')
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

                    
    create_dataframe(data_record, data_error)

    t1 = time.time()
    logger.info('.xmls created')
    logger.info(f'Total processing time {t1-t0}')

if __name__ == '__main__':

    main()
    
