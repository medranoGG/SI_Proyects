import pandas as pd
import matplotlib.pyplot as plt

import sqlite3
import json
from io import BytesIO


def most_vulned(number):
    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "devices" table & "alerts" table
    query_analisis = 'SELECT ip, servicios_vulnerables, vulnerabilidades FROM analisis'

    # Read the querys into the dataframe
    df_analisis = pd.read_sql_query(query_analisis, conn)

    # Create a new column with the sum of vulnerabilities 
    df_analisis['Total Vulnerabilities'] = df_analisis['servicios_vulnerables'] + df_analisis['vulnerabilidades']
    df_analisis = df_analisis.sort_values(by='Total Vulnerabilities', ascending=False)
    df_analisis.rename(columns = {'ip': 'IP', 'servicios_vulnerables' : 'Vunerable Services', 'vulnerabilidades' : 'Vulnerbility number'}, inplace= True)

    df_analisis = df_analisis.nlargest(number, 'Total Vulnerabilities')

    print(df_analisis)

    pdf_buffer = BytesIO()
    plt.savefig(pdf_buffer, format='pdf')
    pdf_buffer.seek(0)

    return pdf_buffer
