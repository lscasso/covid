#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import PercentFormatter


df = pd.read_csv('https://raw.githubusercontent.com/lscasso/covid/main/estadisticasUY_fallecimientos.csv',sep=",")
df['fecha'] =  df['fecha'].apply(lambda x: pd.to_datetime(x, format = '%d/%m/%Y') )

bins= [18,50,60,71,80,120]
labels = ['18-49','50-59','60-70','71-79','80 o más']

df['GrupoEdad'] = pd.cut(df.edad, bins= bins, labels=labels,right=False)

porEdad = df.groupby(['fecha','GrupoEdad']).size().reset_index(name='count')

pEdad = porEdad.pivot_table(index='fecha', columns='GrupoEdad', values='count')
fecha = pEdad.index.max()
febrero = pEdad.copy()
febrero = pEdad[datetime.datetime(2021,2,1):datetime.datetime(2021,2,28)]

diasMes = 28
pEdad['18-49'] = pEdad['18-49'] / (febrero['18-49'].sum()/diasMes)
pEdad['50-59'] = pEdad['50-59'] / (febrero['50-59'].sum()/diasMes)
pEdad['60-70'] = pEdad['60-70'] / (febrero['60-70'].sum()/diasMes)
pEdad['71-79'] = pEdad['71-79'] / (febrero['71-79'].sum()/diasMes)
pEdad['80 o más'] = pEdad['80 o más'] / (febrero['80 o más'].sum()/diasMes)







dfV = pd.read_csv('https://raw.githubusercontent.com/lscasso/covid/main/vacunasXDia.csv',sep=",")
dfV.replace({'Edad': {
        u" años": u"",
        "No Definido": 9999,
        "> 18 meses y <= 21 meses": 1,
        "4 meses": 0,
        "> 21 meses y <= 2": 2
    }}, regex=True, inplace=True)

dfV.Edad = pd.to_numeric(dfV.Edad,errors='coerce')
dfV = dfV[dfV.Edad >= 18]
bins= [18,50,60,71,80,120]
labels = ['18-49','50-59','60-70','71-79','80 o más']
dfV['GrupoEdad'] = pd.cut(dfV.Edad, bins= bins, labels=labels,right=False)


dfV['Fecha'] =  dfV['Fecha'].apply(lambda x: pd.to_datetime(x, format = '%Y-%m-%d') )
porEdadV = dfV.groupby(['Fecha','GrupoEdad']).sum().reset_index()
pEdadV = porEdadV.pivot(index='Fecha', columns='GrupoEdad', values='Cantidad')
pAcum = pEdadV.cumsum()


pAcum['18-49'] = pAcum['18-49'] / 1588867
pAcum['50-59'] = pAcum['50-59'] / 405194
pAcum['60-70'] = pAcum['60-70'] / 371120
pAcum['71-79'] = pAcum['71-79'] / 197490
pAcum['80 o más'] = pAcum['80 o más'] / 141654

fecha = pAcum.index.max()
pAcum = pAcum[datetime.datetime(2021,3,1):]






diasAGraficar = [7,14]
for  dias in diasAGraficar:
    a = pEdad.rolling(window=dias).mean()
    a = a[datetime.datetime(2021,3,1):]
    
    promedioYVacunas = pd.merge (pAcum,a,left_index=True,right_index=True)
    promedioYVacunas.rename(columns={'80 o más_y':'80 o más', '71-79_y':'71-79','60-70_y':'60-70', '50-59_y':'50-59','18-49_y':'18-49'},inplace = True)
    plt2 = promedioYVacunas.plot(x='18-49_x', y='18-49', ylabel='Fallecidos respecto promedio febrero', title='Fallecimientos respecto al promedio febrero y\nporcentaje actos vacunales por franja etaria\nPromedio ' + str(dias) + ' días al ' + fecha.strftime("%d/%m/%Y"))
    plt2.yaxis.set_major_formatter(PercentFormatter(1))
    plt2.xaxis.set_major_formatter(PercentFormatter(1))
    promedioYVacunas.plot(x='50-59_x', y='50-59', ax=plt2)
    promedioYVacunas.plot(x='60-70_x', y='60-70', ax=plt2)
    promedioYVacunas.plot(x='71-79_x', y='71-79', ax=plt2)
    promedioYVacunas.plot(x='80 o más_x', y='80 o más', ax=plt2)
    plt2.set_xlabel("Actos Vacunales")
    fig = plt2.get_figure()
    fig.savefig("promOutput" + str(dias) + ".png", dpi=300, bbox_inches='tight')