#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: leandro
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


df = pd.read_csv('https://raw.githubusercontent.com/lscasso/covid/main/estadisticasUY_fallecimientos.csv',sep=",")
df['fecha'] =  df['fecha'].apply(lambda x: pd.to_datetime(x, format = '%d/%m/%Y') )

bins= [18,50,60,71,80,120]
labels = ['18-49','50-59','60-70','71-79','80 o más']

df['GrupoEdad'] = pd.cut(df.edad, bins= bins, labels=labels,right=False)
porEdad = df.groupby(['fecha','GrupoEdad']).size().reset_index(name='count')
pEdad = porEdad.pivot(index='fecha', columns='GrupoEdad', values='count')
fecha = pEdad.index.max()

diasAGraficar = [7,14]
for  dias in diasAGraficar:
    a = pEdad.rolling(window=dias).mean()
    a = a[datetime.datetime(2021,3,1):]
        
    plt2 = a.plot(legend='reverse',xlabel="Fecha", title='Promedio ' + str(dias) + ' días - Fallecimientos al ' + fecha.strftime("%d/%m/%Y"))
    
    plt2.axvline(x=datetime.datetime(2021,3,22),color='purple',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,3,21),y=15,s='Inicio vacunación\n80 o más',rotation=90,color='purple',fontsize=6)
    
    plt2.axvline(x=datetime.datetime(2021,4,10),color='red',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,4,9),y=15,s='Inicio vacunación\n71-79',rotation=90,color='red',fontsize=6)
    
    fig = plt2.get_figure()
    fig.savefig("output" + str(dias) + ".png", dpi=300, bbox_inches='tight')