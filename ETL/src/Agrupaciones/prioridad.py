import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Create the querys to the SQLite3
query_dataframe_prioridad_1 = 'SELECT * FROM alerts WHERE prioridad == 1'

query_dataframe_prioridad_2 = 'SELECT * FROM alerts WHERE prioridad == 2'

query_dataframe_prioridad_3 = 'SELECT * FROM alerts WHERE prioridad == 3'

# Create the dataframes using pandas
df_prioridad_1 = pd.read_sql_query(query_dataframe_prioridad_1, conn)
df_prioridad_2 = pd.read_sql_query(query_dataframe_prioridad_2, conn)
df_prioridad_3 = pd.read_sql_query(query_dataframe_prioridad_3, conn)

# Print the dataframes
print("\n")
print("Alteras de mayor prioridad")
print(df_prioridad_1)
print("Alertas de media prioridad")
print(df_prioridad_2)
print("Alertas de baja prioridad")
print(df_prioridad_3)

# Close database connection
conn.close()