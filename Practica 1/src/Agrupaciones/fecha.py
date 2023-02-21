import sqlite3
import pandas as pd

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Query the database to get all the data
df = pd.read_sql_query("SELECT * FROM alerts", conn)

# Convert the timestamp column to a datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter the data to get alerts from July and August
july_df = df[df['timestamp'].dt.month == 7]
august_df = df[df['timestamp'].dt.month == 8]

print("Printing alerts recieved on July")
print(july_df)
print("Printing alerts recieved on August")
print(august_df)

# Close database connection
conn.close()