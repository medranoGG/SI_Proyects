import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "analisis" table
query_vulns = 'SELECT vulnerabilidades FROM analisis'

# Read the querys into the dataframe
df_vulns = pd.read_sql_query(query_vulns, conn)

'''
ANÁLISIS VULNERABILIDADES
'''
# Number of entrys
print('\nNumero de observaciones: ', df_vulns['vulnerabilidades'].count())

# Number of NULL
print('Numero de valores ausentes: ', df_vulns['vulnerabilidades'].isnull().sum())

# Median
print('Mediana: ', df_vulns['vulnerabilidades'].median())

# Mean
print('Media: ', df_vulns['vulnerabilidades'].mean())

# Var
print('Varianza: ', df_vulns['vulnerabilidades'].var())

# Max & Min
print('Maximo: ', df_vulns['vulnerabilidades'].max(), " Minimo: ", df_vulns['vulnerabilidades'].min())
