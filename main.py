import sqlite3 as sq
import pandas as pd
import json
con = sq.connect('base.db')

c = con.cursor()

##Campos del csv timestamp,sid,msg,clasificacion,prioridad,protocolo,origen,destino,puerto

##c.execute('''CREATE TABLE alerts (timestamp text,sid int,msg text,clasificacion text,prioridad int,protocolo text,origen text,destino text, puerto int)''')


##alerts = pd.read_csv('alerts.csv')
# write the data to a sqlite table
##alerts.to_sql('alerts', con, if_exists='append', index = False)

with open('test.json') as f:
    data=json.load(f)

##df = pd.DataFrame(data)
##df.to_sql("devices",con)
datosprueba=pd.json_normalize(data)
print(datosprueba)
df=pd.DataFrame(datosprueba)
df.to_sql("devices",con)
