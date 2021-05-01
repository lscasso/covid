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


diasAGraficar = [7,14]
ySub = 9
ajusteSub = 1
for  dias in diasAGraficar:
    a = pEdad.rolling(window=dias).mean()
    a = a[datetime.datetime(2021,3,1):]
    
    plt2 = a.plot(legend='reverse',xlabel="Fecha", title='Evolución de fallecimientos por edad en relación al promedio diario de febrero\nPromedio ' + str(dias) + ' días al ' + fecha.strftime("%d/%m/%Y"))
    plt2.yaxis.set_major_formatter(PercentFormatter(1))
    plt2.axvline(x=datetime.datetime(2021,3,22),color=u'm',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,3,22-ajusteSub),y=ySub,s='Inicio vacunación\n80 o más',rotation=90,color=u'm',fontsize=6)
    
    plt2.axvline(x=datetime.datetime(2021,4,10),color=u'r',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,4,10-ajusteSub),y=ySub,s='Inicio vacunación\n71-79',rotation=90,color=u'r',fontsize=6)
    
    plt2.axvline(x=datetime.datetime(2021,3,15),color=u'g',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,3,15-ajusteSub),y=ySub,s='Inicio vacunación\n60-70',rotation=90,color='g',fontsize=6)
    
    plt2.axvline(x=datetime.datetime(2021,3,8),color=u'#ff7f0e',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,3,8-ajusteSub),y=ySub,s='Inicio vacunación\n50-59',rotation=90,color=u'#ff7f0e',fontsize=6)
    
    plt2.axvline(x=datetime.datetime(2021,3,29),color=u'b',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(x=datetime.datetime(2021,3,29-ajusteSub),y=ySub,s='Inicio vacunación\n18-49',rotation=90,color='b',fontsize=6)
    
    
    plt2.axhline(y=1,color=u'k',linestyle='--',alpha=0.5, linewidth=0.5)
    plt2.text(y=0.65,x=datetime.datetime(2021,3,27),s='Promedio fallecidos diarios\nfebrero 2021',color='k',fontsize=6)
    
    fig = plt2.get_figure()
    fig.savefig("promOutput" + str(dias) + ".png", dpi=300, bbox_inches='tight')