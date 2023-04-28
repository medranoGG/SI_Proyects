import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from io import BytesIO

def tipo_alerta():
    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "alerts" table
    query_alert = 'SELECT * FROM alerts'

    # Read the query into a df
    df_alerts = pd.read_sql_query(query_alert, conn)

    # Group by the classification and count
    alertas_por_clasificacion = df_alerts.groupby('clasificacion')['msg'].count()

    print(alertas_por_clasificacion)

    # Create a graph (simple bar graph)
    alertas_por_clasificacion.plot(kind='bar', color='red')
    plt.title('Número de alertas por categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Número de alertas')

    pdf_buffer = BytesIO()
    plt.savefig(pdf_buffer, format='pdf')
    pdf_buffer.seek(0)

    return pdf_buffer