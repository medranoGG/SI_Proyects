import pandas as pd
import matplotlib.pyplot as plt

import sqlite3
import json


def get_most_vulned(number):
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

    chart_dict = {
            "labels": df_analisis['IP'].tolist(),
            "datasets": [{
                "label": "Total Vulnerabilitites",
                "backgroundColor": "white",
                "borderColor": "white",
                "borderWidth": 3,
                "data": df_analisis['Total Vulnerabilities'].tolist(),
                "fill": True,
                "maxBarThickness": 6
            }]
    }
    # Convert the dictionary to JSON format
    chart_json = json.dumps(chart_dict)

    print(chart_json)

    return chart_json