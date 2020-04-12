import json
import ast

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

