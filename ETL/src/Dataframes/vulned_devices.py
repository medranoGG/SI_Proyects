import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "devices" table & "alerts" table
query_devices = 'SELECT id, ip, responsable FROM devices'
query_alerts = 'SELECT sid, prioridad, origen, destino, puerto from alerts'

# Read the querys into the dataframe
df_devices = pd.read_sql_query(query_devices, conn)
df_alerts = pd.read_sql_query(query_alerts, conn)

# Merge the dataframe
    # Left merge keeps all df_merged rows, and put null values on the non matching ips from the right dataset
    # Inner merge just keeps the matching rows.
df_merged = pd.merge(df_alerts, df_devices, left_on = 'destino', right_on= 'ip', how = 'left')

# Drop columns 'origen' and 'ip' (ip is duplicated)
df_merged.drop(['origen', 'ip', 'sid', 'puerto'], axis = 1, inplace=True)

# Rename columns
df_merged.rename(columns = {'prioridad': 'Prioridad', 'destino' : 'IP', 'id' : 'ID', 'responsable' : 'Responsable'}, inplace= True)

# Print 1st merged dataframe
'''
print("Printing 1st merged dataframe")
print(df_merged)
'''

# Replace NULL value -> unknown
df_merged['ID'].fillna('Unknown', inplace=True)
df_merged['Responsable'].fillna('Unknown', inplace=True)

# Print 2nd merged dataframe
'''
print("Printing 2nd merged dataframe")
print(df_merged)
'''

'''
RESULT DATAFRAMES
'''
# Auxiliar dataframe
df_aux = df_merged.groupby(['IP', 'Responsable', 'ID', 'Prioridad']).size().reset_index(name='apariciones')


# Vulned devices grouped by its IP
df_result_ip = df_aux.groupby('IP').agg({
    'Responsable': 'first',
    'ID': 'first',
    'Prioridad': 'first',
    'apariciones': 'sum'
}).reset_index().rename(columns={'apariciones': 'Apariciones'})

# Print result dataframe
print("\n")
print("IPs de los equipos vulnerados junto al número ataques registrados")
print(df_result_ip)

# Vulned devices grouped by its ID
df_result_id = df_aux.groupby('ID').agg({
    'Responsable': 'first',
    'IP': 'first',
    'Prioridad': 'first',
    'apariciones': 'sum'
}).reset_index().rename(columns={'apariciones': 'Apariciones'})

# Print result dataframe
print("\n")
print("IDs de los equipos vulnerados junto al número ataques registrados")
print(df_result_id)

# Close database connection
conn.close()