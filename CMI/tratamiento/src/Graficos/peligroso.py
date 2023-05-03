import pandas as pd
import matplotlib.pyplot as plt

import sqlite3
import json

def get_most_dangerous(code):
    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "devices" table & "alerts" table
    query_analisis = 'SELECT ip, servicios, servicios_vulnerables FROM analisis'

    # Read the querys into the dataframe
    df_analisis = pd.read_sql_query(query_analisis, conn)
    df_analisis.rename(columns = {'ip': 'IP'}, inplace= True)

    df_analisis["porcentaje_inseguro"] = df_analisis["servicios_vulnerables"]  / df_analisis["servicios"]

    # print(df_analisis)

    df_seguros = df_analisis[df_analisis["porcentaje_inseguro"] <= 0.33]
    df_inseguros = df_analisis[df_analisis["porcentaje_inseguro"] > 0.33]
    
    # print(df_seguros)
    # print(df_inseguros)

    if (code == 0):
        chart_dict = {
                "labels": df_inseguros['IP'].tolist(),
                "datasets": [{
                    "label": "porcentaje_inseguro",
                    "backgroundColor": "white",
                    "borderColor": "white",
                    "borderWidth": 3,
                    "data": df_inseguros['porcentaje_inseguro'].tolist(),
                    "fill": True,
                    "maxBarThickness": 6
                }]
        }
    else:
        chart_dict = {
                "labels": df_seguros['IP'].tolist(),
                "datasets": [{
                    "label": "porcentaje_inseguro",
                    "backgroundColor": "white",
                    "borderColor": "white",
                    "borderWidth": 3,
                    "data": df_seguros['porcentaje_inseguro'].tolist(),
                    "fill": True,
                    "maxBarThickness": 6
                }]
        }

    # Convert the dictionary to JSON format
    chart_json = json.dumps(chart_dict)

    print(chart_json)

    return chart_json
