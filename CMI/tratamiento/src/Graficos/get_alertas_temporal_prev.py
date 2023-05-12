import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from io import BytesIO


def get_alertas_temporal_prev(date):


    #date_obj = datetime.strptime(date, "%Y-%m-%d")
    #prev_day_obj = date_obj - datetime.timedelta(days=1)
    #date_prev = prev_day_obj.strftime("%Y-%m-%d")

    # Connect to the SQLite3 database file
    conn = sqlite3.connect('/tratamiento/database/base.db')

    # Querys to "alerts" table
    query_alert = "SELECT * FROM alerts WHERE DATE(timestamp) = ? "

    
    # Read the query into a df
    df_alerts = pd.read_sql_query(query_alert, conn, params=[date])

    # Change dates to date time
    df_alerts['timestamp'] = pd.to_datetime(df_alerts['timestamp'])

    # Set the index as the timestamp
    df_alerts = df_alerts.set_index('timestamp')

    # Group x day and count
    alerts_per_day = df_alerts['prioridad'].resample('D').count()

    print(alerts_per_day)

    chart_dict = {
        "labels": alerts_per_day.index.strftime('%Y-%m-%d').tolist(),
        "datasets": [{
            "label": "Numero de alertas",
            "backgroundColor": "white",
            "borderColor": "white",
            "borderWidth": 3,
            "data": alerts_per_day.tolist(),
            "fill": True,
            "maxBarThickness": 6
        }]
    }

    # Convert the dictionary to JSON format
    chart_json = json.dumps(chart_dict)

    print(chart_json)

    return chart_json
