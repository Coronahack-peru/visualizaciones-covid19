import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


pathData = "C:/Users/ffalcon/Documents/GitHub/Datos-Abiertos-COVID-19" # pathData = "C:/Users/ffalcon/Dropbox/covid-cases"

print("CARGAR BASES DE DATOS")

reportePositivos = pd.read_csv(os.path.join(pathData, 'DATOSABIERTOS_SISCOVID.csv'), encoding='iso8859_2')
reportePositivos.columns = reportePositivos.columns.str.lower()
reportePositivos = (reportePositivos.sort_values(by=['uuid', 'd_pcr'], ascending=[True, False])
                .groupby(['uuid'])
                .first())

reporteFallecidos = pd.read_csv(os.path.join(pathData, 'fallecidos_minsa_covid19.csv'), encoding='iso8859_2')
reporteFallecidos.columns = reporteFallecidos.columns.str.lower()

# reporteAll = reportePositivos.merge(reporteFallecidos[['uuid','fecha_fallecimiento','departamento','provincia','distrito']], on='uuid', indicator=True)
# reporteAll.loc[reporteAll['_merge']=='both']


print("MODIFY TIMESTAMPS POSITIVOS")
reportePositivos = reportePositivos.dropna(subset=['fecha_prueba'])

reportePositivos['timestamp_prueba'] =  list(map(lambda x:
                                datetime.strptime(x, '%Y-%m-%d') if '-' in x else datetime.strptime(x, '%d/%m/%Y'),
                                reportePositivos['fecha_prueba']))

reportePositivos['timestamp_day'] = reportePositivos['timestamp_prueba']

reportePositivos = reportePositivos.loc[reportePositivos['timestamp_prueba']>datetime(2020, 1, 1),:]

reportePositivos['d_pcr'] = reportePositivos['tipo_prueba'] == 'PCR'


print("MODIFY TIMESTAMPS FALLECIDOS")
reporteFallecidos['timestamp_fecnac'] =  list(map(lambda x:
                                datetime.strptime(x, '%d/%m/%Y') if isinstance(x,str) else np.nan,
                                reporteFallecidos['fecha_nac']))

reporteFallecidos['timestamp_fecfallece'] =  list(map(lambda x:
                                datetime.strptime(x, '%d/%m/%Y') if isinstance(x,str) else np.nan,
                                reporteFallecidos['fecha_fallecimiento']))

reporteFallecidos['edad'] = (reporteFallecidos['timestamp_fecfallece'] - reporteFallecidos['timestamp_fecnac']).dt.days/365

reporteFallecidos['timestamp_day'] = reporteFallecidos['timestamp_fecfallece']


print("GET TOP 10 DISTRICTS WITH MORE POSITIVE CASES BY DPTO")
dptoName = 'LIMA'
provinciaName = 'LIMA'

# Numero de Casos Positivos
positiveCasesDistrito = reportePositivos.loc[(reportePositivos['departamento']==dptoName) & (reportePositivos['provincia']==provinciaName),'distrito'].value_counts().reset_index().rename(columns={'index':'distrito','distrito':'d_pcr'})

# Numero de Positivos via PCR
pcrCasesDistrito = reportePositivos.loc[(reportePositivos['departamento']==dptoName) & (reportePositivos['provincia']==provinciaName),['distrito','d_pcr']].groupby('distrito').sum().sort_values('d_pcr',ascending=False)

# Share de casos via PCR por distrito:
pcrShareDistrito = reportePositivos.loc[(reportePositivos['departamento']==dptoName) & (reportePositivos['provincia']==provinciaName),['distrito','d_pcr']].groupby('distrito').mean().sort_values('d_pcr',ascending=False)

# Numero de Fallecidos
fallecidosDistrito = reporteFallecidos.loc[(reporteFallecidos['departamento']==dptoName) & (reporteFallecidos['provincia']==provinciaName),'distrito'].value_counts().reset_index().rename(columns={'index':'distrito','distrito':'nFallecidos'})

# Merge aggregated statistics by districts
districtsLevelData = (positiveCasesDistrito
                    .merge(pcrCasesDistrito, on='distrito')
                    .merge(pcrShareDistrito, on='distrito')
                    .merge(fallecidosDistrito, on='distrito')
                    .rename(columns={'d_pcr_x':'nCases',
                                    'd_pcr_y':'nPositivesPCR',
                                    'd_pcr':'sharePositivesPCR'}))

districtsLevelData.sort_values('nFallecidos',ascending=False)
