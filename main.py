import sqlite3 as sq
import pandas as pd
import json

conn = sq.connect('base.db')

curs = conn.cursor()

#CREAR TABLAS DEVICES, RESPONSABLE & ANALISIS
create_table_responsable_query = '''
    CREATE TABLE IF NOT EXISTS responsables (
        nombre TEXT,
        telefono INTEGER NOT NULL,
        rol TEXT NOT NULL,
        
        PRIMARY KEY (nombre)
    )
'''
curs.execute(create_table_responsable_query)

create_table_devices_query = '''
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER NOT NULL,
        ip TEXT NOT NULL,
        localizacion TEXT,
        responsable TEXT,

        PRIMARY KEY (ip),
        FOREIGN KEY (responsable)
            REFERENCES responsables(nombre) ON DELETE SET NULL
    )
'''
curs.execute(create_table_devices_query)
 
create_table_analisis_query = '''
    CREATE TABLE IF NOT EXISTS analisis (
        ip TEXT NOT NULL,
        puertos TEXT,
        servicios INTEGER,
        servicios_vulnerables INTEGER,
        vulnerabilidades INTEGER,
        
        FOREIGN KEY (ip)
            REFERENCES devices(ip) ON DELETE SET NULL
    )
'''
curs.execute(create_table_analisis_query)

##Campos del csv timestamp, sid, msg, clasificacion, prioridad, protocolo, origen, destino, puerto

create_table_alerts_query = '''
    CREATE TABLE IF NOT EXISTS alerts (
        timestamp TEXT NOT NULL,
        sid INTEGER,
        message TEXT,
        clasificacion TEXT,
        prioridad INTEGER,
        protocolo TEXT,
        origen TEXT,
        destino TEXT,
        puerto INTEGER,

        PRIMARY KEY (sid)
    )
'''
curs.execute(create_table_alerts_query)

#CSV
print("Started reading the csv file")
alerts = pd.read_csv('alerts.csv')
#Write the data to a sqlite table
alerts.to_sql('alerts', conn, if_exists='append', index = False)

#JSON
print("Started reading the json file")

with open('devices.json') as d:
    devices = json.load(d)

for device in devices:
    id = device['id']
    ip = device['ip']
    localizacion = device['localizacion']
    responsable_nombre = device['responsable']['nombre']
    responsable_telefono = device['responsable']['telefono']
    responsable_rol = device['responsable']['rol']
    puertos_abiertos = device['analisis']['puertos_abiertos']
    servicios = device['analisis']['servicios']
    servicios_inseguros = device['analisis']['servicios_inseguros']
    vulnerabilidades_detectadas = device['analisis']['vulnerabilidades_detectadas']

    print(id, ip, localizacion, responsable_nombre, responsable_telefono, responsable_rol, puertos_abiertos, servicios, servicios_inseguros, vulnerabilidades_detectadas)

    # Insert the data into the database
    curs.execute("INSERT INTO devices (id, ip, localizacion, responsable) VALUES (?, ?, ?, ?)", (id, ip, localizacion, responsable_nombre))
    curs.execute("INSERT OR IGNORE INTO responsables (nombre, telefono, rol) VALUES (?, ?, ?)", (responsable_nombre, responsable_telefono, responsable_rol))
    curs.execute("INSERT INTO analisis (ip, puertos, servicios, servicios_vulnerables, vulnerabilidades) VALUES (?, ?, ?, ?, ?)", (ip, json.dumps(puertos_abiertos), servicios, servicios_inseguros, vulnerabilidades_detectadas))

    conn.commit()
    conn.close()
