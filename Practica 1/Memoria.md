# MEMORIA PRÁCTICA 1: Recopilación, estructuración y análisis de datos

## AUTORES
- Pablo Pastor López
- Pablo Redondo Castro
- Gabriel Medrano Sánchez

## REQUIREMENTS
Se ha proporcionado un script de instalación de las librerias necesarias para la realización de la práctica

## CREACIÓN Y VOLCADO EN LA BASE DE DATOS

Para la creación y el volcado en la base de datos, hemos creado un archivo en python llamado [files_to_db.py](./database/files_to_db.py).
En este, mediante los imports de *sqlite3*, *pandas* y *json* hemos volcado la información de los archivos dentro de nuestra base de datos "base.db"

## DATAFRAMES

Para la creación de los dataframes hemos utilizado la lib **pandas**. 
Todos los dataframes se pueden encontrar en [Dataframes](./src/Dataframes/).

### FUNCIONES RELEVANTES UTILIZADAS

Hemos necesitado utilizad diversas funciones, algunas de las más relevantes son:
- *pd.read_sql_query()*
- *Dataframe.shape[]*
- *Dataframe.apply(lambda x: eval(x) if x != None else [])* Porque uno de los valores "None" no se cuenta como entero
- *.mean()*
- *.std()*
- *Dataframe.drop()*
- *Dataframe.rename()*
- *Dataframe.fillna()*
- *pd.merge()*

Entre otras

## AGRUPACIONES

Para realizar las agrupaciones hemos utilizado de nuevo la lib **pandas**
Todas las agrupaciones se pueden encontrar en [Agrupaciones](./src/Agrupaciones/)

Las agrupaciones han sido más sencillas puesto que se podía hacer la selección desde las propias consultas SQL

## ANALISIS VULNERABILIDADES

Se propone realizar ciertos cálculos sobre la variable análisis.
Para ello, hemos creado una nueva carpeta llamada [Analisis vulnerabilidades](./src/Analisis%20vulnerabilidades/)

En el archivo [vulnerabilidades.py](./src/Analisis%20vulnerabilidades/vulnerabilidades.py) hemos creado un *Dataframe* con todos los campos de 
nuestra tabla "análisis".
Indexando a través de la columna *vulnerabilidades* hemos extraido los datos de la misma y realizado las operaciones pertinentes.

## GRAFICOS

Para la creación de los gráficos, hemos utilizado la librería **matplotlib**
Todos los archivos de creación de gráficos se pueden encontrar [Graficos](./src/Graficos/)

Para la creación de estos gráficos, hemos creado *dataframes* por cada problema.
Mediante la librería **matplotlib** accedemos a los diferentes campos del gráfico para personalizarlo
    - Título
    - Descripción
    - Color
    - etc