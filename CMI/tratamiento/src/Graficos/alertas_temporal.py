import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from io import BytesIO

def alertas_temporal():
    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "alerts" table
    query_alert = 'SELECT * FROM alerts'

    # Read the query into a df
    df_alerts = pd.read_sql_query(query_alert, conn)

    # Change dates to date time
    df_alerts['timestamp'] = pd.to_datetime(df_alerts['timestamp'])

    # Set the index as the timestamp
    df_alerts = df_alerts.set_index('timestamp')

    # Group x day and count
    alerts_per_day = df_alerts['prioridad'].resample('D').count()

    print(alerts_per_day)

    # Create a graph
    plt.plot(alerts_per_day.index, alerts_per_day.values, color='black')
    plt.xlabel('Fecha')
    plt.ylabel('Número de alertas')
    plt.title('Número de alertas por día')

    pdf_buffer = BytesIO()
    plt.savefig(pdf_buffer, format='pdf')
    pdf_buffer.seek(0)

    return pdf_buffer