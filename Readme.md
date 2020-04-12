## Activate your virtual enviroment

Activate a virtual enviroment or create new one.

## Installation

Use requirements.txt to install all the libraries you need to run the script.
Try with the next executable commands. The last two is only for conda enviroment.

```
pip install -r requirements.txt  
```
```
while read requirement; do conda install --yes $requirement; done < requirements.txt
```
```
conda install --yes --file requirements.txt
```

##  Create two files inside the main file.

The name of the files must be: 'excel_results' and 'xml_files' .

## Keep the .xml file

Keep your .xml file inside xml_files.

## Write the name of your .xml in the script.

You must change the value of xml_name. 
This variable is in main.py.

## Execute the script.
Write in your terminal the next command.
```
python main.py
```
You'll have the new tables in excel_results.