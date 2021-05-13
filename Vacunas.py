#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import PercentFormatter


df = pd.read_csv('https://raw.githubusercontent.com/lscasso/covid/main/vacunasXDia.csv',sep=",")
df.replace({'Edad': {
        u" años": u"",
        "No Definido": 9999,
        "> 18 meses y <= 21 meses": 1,
        "4 meses": 0,
        "> 21 meses y <= 2": 2
    }}, regex=True, inplace=True)

df.Edad = pd.to_numeric(df.Edad,errors='coerce')
df = df[df.Edad >= 18]
bins= [18,50,60,71,80,120]
labels = ['18-49','50-59','60-70','71-79','80 o más']
df['GrupoEdad'] = pd.cut(df.Edad, bins= bins, labels=labels,right=False)


df['Fecha'] =  df['Fecha'].apply(lambda x: pd.to_datetime(x, format = '%Y-%m-%d') )
porEdad = df.groupby(['Fecha','GrupoEdad']).sum().reset_index()
pEdad = porEdad.pivot(index='Fecha', columns='GrupoEdad', values='Cantidad')
pAcum = pEdad.cumsum()


pAcum['18-49'] = pAcum['18-49'] / 1588867
pAcum['50-59'] = pAcum['50-59'] / 405194
pAcum['60-70'] = pAcum['60-70'] / 371120
pAcum['71-79'] = pAcum['71-79'] / 197490
pAcum['80 o más'] = pAcum['80 o más'] / 141654

fecha = pAcum.index.max()
pAcum = pAcum[datetime.datetime(2021,3,1):]
plt2 = pAcum.plot(xlabel="Fecha", title='Actos Vacunales acumulados respecto a población al ' +  fecha.strftime("%d/%m/%Y"), legend='reverse')

plt2.yaxis.set_major_formatter(PercentFormatter(1))
fig = plt2.get_figure()
fig.savefig("ovacunas.png", dpi=300, bbox_inches='tight')