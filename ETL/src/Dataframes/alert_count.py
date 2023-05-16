import pandas as pd
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('database/base.db')

# Querys to "devices" table
query_alerts = 'SELECT sid FROM alerts'

# Read the querys into the dataframe
df_alerts = pd.read_sql_query(query_alerts, conn)

# Count the rows
num_rows = df_alerts.shape[0]

# Print the row numbers
print("\n")
print("Número total de alertas:")
print(num_rows)

# Close database connection
conn.close()