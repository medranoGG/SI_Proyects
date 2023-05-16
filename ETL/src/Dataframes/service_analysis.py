import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "analisis" table
query_servicios = "SELECT servicios FROM analisis"
query_servicios_vulnerables = "SELECT servicios_vulnerables FROM analisis"
query_vulnerabilidades = "SELECT vulnerabilidades FROM analisis"

# Read the querys into dataframes
df_servicios = pd.read_sql_query(query_servicios, conn)
df_servicios_vulnerables = pd.read_sql_query(query_servicios_vulnerables, conn)
df_vulnerabilidades =  pd.read_sql_query(query_vulnerabilidades, conn)

'''
SERVICES
'''
# Calculate mean and standard dev. of services
media = df_servicios['servicios'].mean()
desv_tipica = df_servicios['servicios'].std()

# Create a result dataframe
results_servicios = pd.DataFrame({
    'Media': [media],
    'Desv. estándar': [desv_tipica]
})

# Print a dataframe with the results
print("\n")
print("Análisis de los servicios encontrados\n")
print(results_servicios.to_string(index=False))

'''
VULNERABLE SERVICES
'''
# Calculate mean and standard dev. of vulnerable services
media = df_servicios_vulnerables['servicios_vulnerables'].mean()
desv_tipica = df_servicios_vulnerables['servicios_vulnerables'].std()

# Create a result dataframe
results_servicios_vulnerables = pd.DataFrame({
    'Media': [media],
    'Desv. estándar': [desv_tipica]
})

# Print a dataframe with the results
print("\n")
print("Análisis de los servicios vulnerables encontrados\n")
print(results_servicios_vulnerables.to_string(index=False))

'''
VULNERABILITIES FOUND
'''
# Calculate mean,standard dev. max & min of the vulnerabilities found
media = df_vulnerabilidades['vulnerabilidades'].mean()
desv_tipica = df_vulnerabilidades['vulnerabilidades'].std()
max = df_vulnerabilidades['vulnerabilidades'].max()
min = df_vulnerabilidades['vulnerabilidades'].min()

# Create a result dataframe
results_vulnerabilidades = pd.DataFrame({
    'Media': [media],
    'Desv. estándar': [desv_tipica],
    'Max' : [max],
    'Min' : [min]
})

# Print a dataframe with the results
print("\n")
print("Análisis de las vulnerabilidades encontradas\n")
print(results_vulnerabilidades.to_string(index=False))

# Close database connection
conn.close()