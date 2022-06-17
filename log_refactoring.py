import pandas as pd
import openpyxl


#with open('LOG00194.csv', 'r') as file :
 # filedata = file.read()
#
#filedata = filedata.replace('"', '')
#
#with open('LOG00194.csv', 'w') as file:
 # file.write(filedata)


df = pd.read_csv("LOG00194.csv")

df.to_excel('log.xlsx', sheet_name='new_sheet')
