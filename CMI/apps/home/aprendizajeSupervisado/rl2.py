import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import json

def cargar_datos_entrenamiento(archivo_json,X,y):
    with open(archivo_json, 'r') as f:
        datos = json.load(f)

    for dispositivo in datos:
        X.append([
            dispositivo['servicios'],
            dispositivo['servicios_inseguros'],
        ])
        y.append(dispositivo['peligroso'])


def predecir_datos(archivo_json,clf,Xp):
    with open(archivo_json, 'r') as f:
        datos = json.load(f)

    for dispositivo in datos:
        Xp.append([
            dispositivo['servicios'],
            dispositivo['servicios_inseguros']
        ])
    Yp = clf.predict(Xp)

    device_ids = []
    for device in datos:
        device_ids.append(device['id'])

    return Yp, device_ids


if __name__ == '__main__':
    Xt = []
    yt = []
    Xp = []
    Yp = []
    devices_id = []
    jsonTrain = 'dump/devices_IA_clases.json'
    jsonPred = 'dump/devices_IA_predecir_v2.json'


    # Load data
    cargar_datos_entrenamiento(jsonTrain, Xt, yt)
    regr = linear_model.LinearRegression()
    regr.fit(Xt, yt)

    # Make predictions
    Yp, devices_id = predecir_datos(jsonPred, regr, Xp)

    # Print results
    print(Yp)
    print(devices_id)

    # Plot outputs
    plt.scatter(Xt, yt, color='black')
    plt.plot(Xt, regr.predict(Xt), color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()
