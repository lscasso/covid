#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 17:45:14 2021

@author: leandro
"""

import pandas as pd
import bar_chart_race as bcr

df = pd.read_csv('https://raw.githubusercontent.com/3dgiordano/covid-19-uy-vacc-data/main/data/Subnational.csv',sep=",")
df['date'] =  df['date'].apply(lambda x: pd.to_datetime(x, format = '%Y-%m-%d') )
df['region'].replace({"UY-MA":"Maldonado"},inplace=True)
df = df.groupby(['date','region']).sum().reset_index()
dfPivot = df.pivot(index='date', columns='region', values='people_vaccinated')

dfPivotProm = dfPivot.copy()
dfPivotProm['Artigas']  =  dfPivot['Artigas'] / 74570*100
dfPivotProm['Canelones']  =  dfPivot['Canelones'] / 588959*100
dfPivotProm['Cerro Largo']  =  dfPivot['Cerro Largo'] / 89587*100
dfPivotProm['Colonia']  =  dfPivot['Colonia'] / 130444*100
dfPivotProm['Durazno']  =  dfPivot['Durazno'] / 58990*100
dfPivotProm['Florida']  =  dfPivot['Florida'] / 69318*100
dfPivotProm['Flores']  =  dfPivot['Flores'] / 26500*100
dfPivotProm['Lavalleja']  =  dfPivot['Lavalleja'] / 59002*100
dfPivotProm['Maldonado']  =  dfPivot['Maldonado'] / 190078*100
dfPivotProm['Montevideo']  =  dfPivot['Montevideo'] / 1381946*100
dfPivotProm['Paysandu']  =  dfPivot['Paysandu'] / 119373*100
dfPivotProm['Rio Negro']  =  dfPivot['Rio Negro'] / 57874*100
dfPivotProm['Rocha']  =  dfPivot['Rocha'] / 74079*100
dfPivotProm['Rivera']  =  dfPivot['Rivera'] / 108569*100
dfPivotProm['Salto']  =  dfPivot['Salto'] / 132788*100
dfPivotProm['San Jose']  =  dfPivot['San Jose'] / 116479*100
dfPivotProm['Soriano']  =  dfPivot['Soriano'] / 83930*100
dfPivotProm['Tacuarembo']  =  dfPivot['Tacuarembo'] / 92993*100
dfPivotProm['Treinta y Tres']  =  dfPivot['Treinta y Tres'] / 50504*100

bcr.bar_chart_race(
    df=dfPivotProm,
    filename='vacunacion2.mp4',
    orientation='h',
    sort='desc',
    n_bars=19,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
     
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%d/%m/%Y',
    period_summary_func=lambda v, r: {'x': .99, 'y': .12,
                                      's': f'Personas vacunadas\npromedio país: {v.mean():.0f}%',
                                      'ha': 'right', 'size': 8, 'family': 'Courier New'},

    period_length=500,
    figsize=(5, 3),
    dpi=144,
    cmap='dark12',
    title='Personas vacunadas por departamento\nPorcentaje de la población',
    title_size='',
    bar_label_size=7,
    tick_label_size=7,
    shared_fontdict={'family' : 'Helvetica', 'color' : '.1'},
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)  