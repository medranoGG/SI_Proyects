import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to the SQLite3 database file
conn = sqlite3.connect('../../database/base.db')

# Querys to "alerts" table
query_alert = 'SELECT * FROM alerts'

# Read the query into a df
df_alerts = pd.read_sql_query(query_alert, conn)

# Select priority 1
df_p1 = df_alerts[df_alerts['prioridad'] == 1]

# Count the aparitions of the 'origen'IP column
df_counts = df_p1.groupby('origen').size().reset_index(name='counts')

# Select top 10
df_top10 = df_counts.nlargest(10, 'counts')

print(df_top10)

# Crear un graph (simple bar graph with titles)
plt.bar(df_top10['origen'], df_top10['counts'], color='red')
plt.xticks(rotation=90)
plt.xlabel('IP de origen')
plt.ylabel('Número de alertas')
plt.title('Las 10 IP de origen más problemáticas')
plt.show()