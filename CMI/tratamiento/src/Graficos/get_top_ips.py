import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import json


def get_top_ips(num_ips):
    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')


    # Querys to "alerts" table
    query_alert = 'SELECT * FROM alerts'

    # Read the query into a df
    df_alerts = pd.read_sql_query(query_alert, conn)

    # Select priority 1
    df_p1 = df_alerts[df_alerts['prioridad'] == 1]  

    # Count the aparitions of the 'origen'IP column
    df_counts = df_p1.groupby('origen').size().reset_index(name='counts')

    # Select top 10
    df_top = df_counts.nlargest(num_ips, 'counts')

    print(df_top)

    # Create the dictionary for the chart data
    chart_dict = {
        "labels": df_top['origen'].tolist(),
        "datasets": [{
            "label": "Counts",
            "backgroundColor": "white",
            "borderColor": "white",
            "borderWidth": 3,
            "data": df_top['counts'].tolist(),
            "fill": True,
            "maxBarThickness": 6
        }]
    }

    # Convert the dictionary to JSON format
    chart_json = json.dumps(chart_dict)

    print(chart_json)

    return chart_json

get_top_ips(10)