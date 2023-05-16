import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "devices" table
query_puertos = 'SELECT puertos FROM analisis'

# Read the querys into the dataframe
df_puertos = pd.read_sql_query(query_puertos, conn)
df_puertos['puertos'] = df_puertos['puertos'].apply(lambda x: eval(x) if x != None else [])


# Calculate mean and standard dev. of open ports
media = df_puertos['puertos'].apply(len).mean()
desv_tipica = df_puertos['puertos'].apply(len).std()
max = df_puertos['puertos'].apply(lambda x: len(x)).max()
min = df_puertos['puertos'].apply(lambda x: len(x)).min()

# Create a result dataframe
results = pd.DataFrame({
    'Media': [media],
    'Desv. estándar': [desv_tipica], 
    'Max' : [max],
    'Min' : [min]
})

# Print a dataframe with the results
print("\n")
print("Dataframe análisis de los puertos abiertos encontrados\n")
print(results.to_string(index=False))

# Close database connection
conn.close()