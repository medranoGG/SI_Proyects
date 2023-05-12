from matplotlib import pyplot as plt
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import plot_tree
import graphviz #https://graphviz.org/download/
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
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(Xt, yt)
    # Print plot
    dot_data = tree.export_graphviz(clf, out_file=None,
                          feature_names=['servicios', 'servicios_inseguros'],
                          class_names=['No peligroso', 'Peligroso'],
                         filled=True, rounded=True,
                        special_characters=True)
    graph = graphviz.Source(dot_data)
    #graph.view()

    Yp, devices_id = predecir_datos(jsonPred,clf,Xp)

    peligrosos = []
    for i in range(len(Yp)):
        if Yp[i] == 1:
            peligrosos.append(devices_id[i])

    print(Yp)
    print(peligrosos)


