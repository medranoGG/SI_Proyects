import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from io import BytesIO

def puertos_vulns():

    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "devices" table & "alerts" table
    query_analisis = 'SELECT * FROM analisis'

    # Read the querys into the dataframe
    df_analisis = pd.read_sql_query(query_analisis, conn)

    print(df_analisis)

    # Querys to "devices" table
    query_puertos = 'SELECT puertos FROM analisis'

    # Dataframe of the ports
    df_puertos = pd.read_sql_query(query_puertos, conn)
    df_puertos['puertos'] = df_analisis['puertos'].apply(lambda x: eval(x) if x != None else [])
    df_puertos['numero_puertos'] = df_puertos['puertos'].apply(lambda x: len(x))

    print(df_puertos)

    # Data configure
    x = df_puertos['numero_puertos']
    y1 = df_analisis['servicios_vulnerables']
    y2 = df_analisis['servicios']

    # Graph configuration
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title('Media de puertos abiertos frente a servicios inseguros y frente al total de servicios detectados')
    ax.set_xlabel('Media de puertos abiertos')
    ax.set_ylabel('Número de servicios')
    ax.grid(True)

    # Data plotting
    ax.bar(x, y2, color='red', label='Total de servicios')
    ax.stem(x, y1, markerfmt ='black', basefmt  ='black', label='Servicios inseguros')

    # Legend
    ax.legend()

    pdf_buffer = BytesIO()
    plt.savefig(pdf_buffer, format='pdf')
    pdf_buffer.seek(0)

    return pdf_buffer