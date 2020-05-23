import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt


pathData = "C:/Users/ffalcon/Documents/GitHub/Datos-Abiertos-COVID-19" # pathData = "C:/Users/ffalcon/Dropbox/covid-cases"
pathVisualizaciones = "C:/Users/ffalcon/Documents/GitHub/visualizaciones-covid19" # pathData = "C:/Users/ffalcon/Dropbox/covid-cases"


print("1. CARGAR BASES DE DATOS")

reportePositivos = pd.read_csv(os.path.join(pathData, 'DATOSABIERTOS_SISCOVID.csv'), encoding='iso8859_2')
reportePositivos.columns = reportePositivos.columns.str.lower()
reportePositivos = reportePositivos.dropna(subset=['fecha_nacimiento','departamento','provincia','distrito'])

reporteFallecidos = pd.read_csv(os.path.join(pathData, 'fallecidos_minsa_covid19.csv'), encoding='iso8859_2')
reporteFallecidos.columns = reporteFallecidos.columns.str.lower()
reporteFallecidos.shape
reporteFallecidos = reporteFallecidos.dropna(subset=['fecha_nacimiento','departamento','provincia','distrito'])

dataDistritos = pd.read_excel(os.path.join(pathData,'..','Datos-Complementarios-COVID19','Información de Distritos 2020.xlsx'),sheet_name="Nivel Distrital")
dataDistritos = dataDistritos.iloc[:1873,:]

def replaceCharacters(nameOld):

    nameOld=nameOld.replace('Á', 'A')
    nameOld=nameOld.replace('É', 'E')
    nameOld=nameOld.replace('Í', 'I')
    nameOld=nameOld.replace('Ó', 'O')
    nameOld=nameOld.replace('Ú', 'U')
    nameOld=nameOld.replace('Ñ', 'N')

    nameOld=nameOld.replace(' DE ', '')
    nameOld=nameOld.replace(' DEL ', '')
    nameOld=nameOld.replace(' LA ', '')
    nameOld=nameOld.replace(' LAS ', '')

    nameNew = nameOld

    return nameNew

print("2. CLEAN DISTRICT DATA A LITTLE BIT")

dataDistritos['grupo_etario1'] = (dataDistritos['De 0  a 4 años\n2017'] + dataDistritos['De 5  a 9 años\n2017'] +
                                    dataDistritos['De 10 a 14 años\n2017'] + dataDistritos['De 15 a 19 años\n2017'])
dataDistritos['grupo_etario2'] = (dataDistritos['De 20 a 24 años\n2017'] + dataDistritos['De 25 a 29 años\n2017'] +
                                    dataDistritos['De 30 a 34 años\n2017'] + dataDistritos['De 35 a 39 años\n2017'] + dataDistritos['De 40 a 44 años\n2017'])
dataDistritos['grupo_etario3'] = (dataDistritos['De 45 a 49 años\n2017'] + dataDistritos['De 50 a 54 años\n2017'] +
                                    dataDistritos['De 55 a 59 años\n2017'] + dataDistritos['De 60 a 64 años\n2017'])
dataDistritos['grupo_etario4'] = (dataDistritos['De 65 a 69 años\n2017'] + dataDistritos['De 70 a 74 años\n2017'])

dataDistritos['grupo_etario5'] = (dataDistritos['De 75 a 79 años\n2017'] + dataDistritos['De 80 a 84 años\n2017'] +
                                    dataDistritos['De 85 a 89 años\n2017'] + dataDistritos['De 90 a 94 años\n2017'] + dataDistritos['De 95 a más\n2017'])

dataDistritos = dataDistritos[['UBIGEO','Departamento','Provincia','Distrito','grupo_etario1','grupo_etario2','grupo_etario3','grupo_etario4','grupo_etario5']]
dataDistritos.columns = dataDistritos.columns.str.lower()
dataDistritos['departamento'] = dataDistritos['departamento'].str.upper()
dataDistritos['provincia'] = dataDistritos['provincia'].str.upper()
dataDistritos['distrito'] = dataDistritos['distrito'].str.upper()

dataDistritos['departamento'] = list(map(lambda x: replaceCharacters(x), dataDistritos['departamento']))
dataDistritos['provincia'] = list(map(lambda x: replaceCharacters(x), dataDistritos['provincia']))
dataDistritos['distrito'] = list(map(lambda x: replaceCharacters(x), dataDistritos['distrito']))

dataDistritos = pd.wide_to_long(dataDistritos, stubnames="grupo_etario", i=['ubigeo','departamento','provincia','distrito'], j="agecat").reset_index().rename(columns={'grupo_etario':'nHabitantes','agecat':'grupo_etario'})

print("3. MODIFY TIMESTAMPS POSITIVOS")

reportePositivos = reportePositivos.dropna(subset=['fecha_prueba'])

reportePositivos['timestamp_fecnac'] =  list(map(lambda x:
                                datetime.strptime(x, '%Y-%m-%d') if '-' in x else datetime.strptime(x, '%d/%m/%Y'),
                                reportePositivos['fecha_nacimiento']))

reportePositivos['timestamp_prueba'] =  list(map(lambda x:
                                datetime.strptime(x, '%Y-%m-%d') if '-' in x else datetime.strptime(x, '%d/%m/%Y'),
                                reportePositivos['fecha_prueba']))

reportePositivos['edad'] = (reportePositivos['timestamp_prueba'] - reportePositivos['timestamp_fecnac']).dt.days/365

reportePositivos = reportePositivos.loc[reportePositivos['timestamp_prueba']>datetime(2020, 1, 1),:]

reportePositivos['timestamp_day'] = reportePositivos['timestamp_prueba']

reportePositivos['d_pcr'] = reportePositivos['tipo_prueba'] == 'PCR'

reportePositivos['count'] = 1

#Armar categoria por grupo etario
reportePositivos['grupo_etario'] = np.nan
reportePositivos.loc[(reportePositivos['edad']>=-1) & (reportePositivos['edad']<=19),'grupo_etario']   = 1
reportePositivos.loc[(reportePositivos['edad']>19) & (reportePositivos['edad']<=44),'grupo_etario']  = 2
reportePositivos.loc[(reportePositivos['edad']>44) & (reportePositivos['edad']<=64),'grupo_etario']  = 3
reportePositivos.loc[(reportePositivos['edad']>64) & (reportePositivos['edad']<=74),'grupo_etario']  = 4
reportePositivos.loc[reportePositivos['edad']>=74 ,'grupo_etario'] = 5

#Replace Tildes and Nhes
reportePositivos['departamento'] = list(map(lambda x: replaceCharacters(x), reportePositivos['departamento']))
reportePositivos['provincia'] = list(map(lambda x: replaceCharacters(x), reportePositivos['provincia']))
reportePositivos['distrito'] = list(map(lambda x: replaceCharacters(x), reportePositivos['distrito']))


print("4. MODIFY TIMESTAMPS FALLECIDOS")
reporteFallecidos['timestamp_fecnac'] =  list(map(lambda x:
                                datetime.strptime(x, '%d/%m/%Y') if isinstance(x,str) else np.nan,
                                reporteFallecidos['fecha_nacimiento']))

reporteFallecidos['timestamp_fecfallece'] =  list(map(lambda x:
                                datetime.strptime(x, '%d/%m/%Y') if isinstance(x,str) else np.nan,
                                reporteFallecidos['fecha_fallecimiento']))

reporteFallecidos['edad'] = (reporteFallecidos['timestamp_fecfallece'] - reporteFallecidos['timestamp_fecnac']).dt.days/365

reporteFallecidos['timestamp_day'] = reporteFallecidos['timestamp_fecfallece']

reporteFallecidos['count'] = 1

#Armar categoria por grupo etario
reporteFallecidos['grupo_etario'] = np.nan
reporteFallecidos.loc[(reporteFallecidos['edad']>=-1) & (reporteFallecidos['edad']<=19),'grupo_etario']   = 1
reporteFallecidos.loc[(reporteFallecidos['edad']>20) & (reporteFallecidos['edad']<=44),'grupo_etario']  = 2
reporteFallecidos.loc[(reporteFallecidos['edad']>44) & (reporteFallecidos['edad']<=64),'grupo_etario']  = 3
reporteFallecidos.loc[(reporteFallecidos['edad']>64) & (reporteFallecidos['edad']<=74),'grupo_etario']  = 4
reporteFallecidos.loc[reporteFallecidos['edad']>=74 ,'grupo_etario'] = 5

#Replace Tildes and Nhes
reporteFallecidos['departamento'] = list(map(lambda x: replaceCharacters(x), reporteFallecidos['departamento']))
reporteFallecidos['provincia'] = list(map(lambda x: replaceCharacters(x), reporteFallecidos['provincia']))
reporteFallecidos['distrito'] = list(map(lambda x: replaceCharacters(x), reporteFallecidos['distrito']))


print("5. GET TOP 10 DISTRICTS WITH MORE POSITIVE CASES BY DPTO")

# Numero de Casos Positivos
positiveCasesDistrito = (reportePositivos.loc[:,['departamento','provincia','distrito','grupo_etario','count']]
                        .groupby(['departamento','provincia','distrito','grupo_etario'])
                        .sum()
                        .reset_index()
                        .rename(columns={'count':'nPositivos'}))

# Numero de Fallecidos
fallecidosDistrito = (reporteFallecidos.loc[:,['departamento','provincia','distrito','grupo_etario','count']]
                        .groupby(['departamento','provincia','distrito','grupo_etario'])
                        .sum()
                        .reset_index()
                        .rename(columns={'count':'nFallecidos'}))

# Merge aggregated statistics by districts
districtsLevelData = (positiveCasesDistrito
                        .merge(fallecidosDistrito, on=['departamento','provincia','distrito','grupo_etario'], how='left', indicator=True).rename(columns={'_merge':'_mergeFallecidos'})
                        .merge(dataDistritos, on=['departamento','provincia','distrito','grupo_etario'], how='left', indicator=True).rename(columns={'_merge':'_mergeHabitantes'}))

districtsLevelData = districtsLevelData.loc[districtsLevelData['_mergeHabitantes']=='both',:].drop(['_mergeFallecidos', '_mergeHabitantes'], axis=1)


districtsLevelData = districtsLevelData.sort_values('nFallecidos',ascending=False)
districtsLevelData['infectadosPCP'] = (districtsLevelData['nPositivos']/districtsLevelData['nHabitantes'])*1000
districtsLevelData['muertesPCP'] = (districtsLevelData['nFallecidos']/districtsLevelData['nHabitantes'])*1000
districtsLevelData['tasa_fatalidad'] = (districtsLevelData['nFallecidos']/districtsLevelData['nPositivos'])*100
districtsLevelData.loc[districtsLevelData['nPositivos']<=30,'tasa_fatalidad'] = np.nan

districtsLevelData.sort_values('muertesPCP',ascending=False).head(10)

districtsLevelData = districtsLevelData[['ubigeo', 'departamento', 'provincia', 'distrito', 'grupo_etario', 'nPositivos', 'nFallecidos','nHabitantes', 'infectadosPCP', 'muertesPCP', 'tasa_fatalidad']]
districtsLevelData['ubigeo'] = districtsLevelData['ubigeo'].astype(int)

districtsLevelData.to_csv(os.path.join(pathVisualizaciones,'data','contagios_fallecidos_distritos.csv'), index=False)


list(districtsLevelData)
#Plot Fatality Rate
varName= 'infectadosPCP'
a_plot = sns.kdeplot(districtsLevelData.loc[districtsLevelData['grupo_etario']==2, varName],color='blue',label='[18 44]')
a_plot = sns.kdeplot(districtsLevelData.loc[districtsLevelData['grupo_etario']==3, varName],color='orange',label='[45 64]')
a_plot = sns.kdeplot(districtsLevelData.loc[districtsLevelData['grupo_etario']==4, varName],color='green',label='[65 74]')
a_plot = sns.kdeplot(districtsLevelData.loc[districtsLevelData['grupo_etario']==5, varName],color='black',label='[75 100]')
a_plot.set(xlim=(0, 30))




# Agregar UBIGEO
#
