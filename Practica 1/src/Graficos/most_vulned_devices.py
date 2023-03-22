import pandas as pd
import matplotlib.pyplot as plt

import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "devices" table & "alerts" table
query_analisis = 'SELECT ip, servicios_vulnerables, vulnerabilidades FROM analisis'

# Read the querys into the dataframe
df_analisis = pd.read_sql_query(query_analisis, conn)

# Create a new column with the sum of vulnerabilities 
df_analisis['Total Vulnerabilities'] = df_analisis['servicios_vulnerables'] + df_analisis['vulnerabilidades']
df_analisis = df_analisis.sort_values(by='Total Vulnerabilities', ascending=False)
df_analisis.rename(columns = {'ip': 'IP', 'servicios_vulnerables' : 'Vunerable Services', 'vulnerabilidades' : 'Vulnerbility number'}, inplace= True)

print(df_analisis)

# Create a graph (simple bar chart)
plt.bar(df_analisis['IP'], df_analisis['Total Vulnerabilities'], color='red')
plt.xticks(rotation=90)
plt.xlabel('IP del dispositivo')
plt.ylabel('Total Vulnerabilidades')
plt.title('Equipos más vulnerados')
plt.show()

