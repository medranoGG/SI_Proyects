from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.tree import export_graphviz
from subprocess import call
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
    clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=5)
    clf.fit(Xt, yt)
    print(str(Xt[0]) + " " + str(yt[0]))
    print(clf.predict([Xt[0]]))

    for i in range(len(clf.estimators_)):
        print(i)
        estimator = clf.estimators_[i]
        export_graphviz(estimator,
                        out_file='tree.dot',
                        feature_names=['servicios', 'servicios_inseguros'],
                        class_names=['No peligroso', 'Peligroso'],
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        call(['dot', '-Tpng', 'tree.dot', '-o', 'tree'+str(i)+'.png', '-Gdpi=600'])