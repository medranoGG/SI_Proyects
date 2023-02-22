import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "devices" table
query_devices = 'SELECT ip FROM devices'

# Read the querys into the dataframe
df_devices = pd.read_sql_query(query_devices, conn)

# Count the rows
num_rows = df_devices.shape[0]

# Print the row numbers
print("\n")
print("Número total de dispositivos")
print(num_rows)

# Close database connection
conn.close()