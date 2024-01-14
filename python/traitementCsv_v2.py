# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:47:01 2023

@author: vanes
"""

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def drawHistoNivZoom(df_zoom):
    plt.clf()
    
    maxNiv = int(df_zoom['nivZoom'].max())
    minNiv = int(df_zoom['nivZoom'].min())
    maxNb = max(df_zoom['nivZoom'].value_counts())
    
    sns.histplot(data=df_zoom, x='nivZoom', discrete=True, binrange=(minNiv,maxNiv))
    plt.xticks(range(minNiv, maxNiv+1, 1))
    plt.yticks(range(0, maxNb+1, 1))
    plt.xlabel("Niveau de zoom")
    plt.ylabel("Occurence")

    plt.savefig("output/occNivZoom_"+NAME+".png")
    plt.show()


def addSeconds(df):
    lst_sec = []
    
    for line in df.itertuples():
        time = 0
        if type(line[2]) == str:
            dico_time = json.loads(line[2])
            time = dico_time['min'] * 60 + dico_time['sec'] + dico_time['mili'] * 1E-3
        lst_sec.append(time)
        
    df['sec'] = lst_sec
    
def calculateDurationZoom(df):

    nbRow = df.shape[0]
    lst = [0]*nbRow
    
    for i in range(nbRow-2):

        typ = df.iloc[i, 0]

        if typ == 'zoomstart':
            startTime = df.iloc[i, 7]
            
            endTime = df.iloc[i+2, 7]
            lst[i] = endTime-startTime

    df["zoomDuration"] = lst


def drawGraphNivZoomTime(df_zoom):
    plt.clf()
    
    maxNiv = int(df_zoom['nivZoom'].max())
    minNiv = int(df_zoom['nivZoom'].min())
    maxSec = int(df_zoom['sec'].max())
    minSec = int(df_zoom['sec'].min())
    
    sns.lineplot(data=df_zoom, x="sec", y="nivZoom")
    sns.scatterplot(data=df_zoom, x="sec", y="nivZoom")   
    plt.yticks(range(minNiv, maxNiv+1, 1))
    plt.xlabel("Temps en sec")
    plt.ylabel("Niveau de zoom")

    plt.savefig("output/timeNivZoom_"+NAME+".png")
    plt.show()
    
    
def drawGraphNivZoomDuration(df_zoom):
    plt.clf()
    
    maxNiv = int(df_zoom['nivZoom'].max())
    minNiv = int(df_zoom['nivZoom'].min())
    # maxNb = max(df_zoom['nivZoom'].value_counts())
    
    sns.histplot(data=df_zoom, x='nivZoom', weights='zoomDuration', discrete=True, hue='zoomDuration', legend=False, binrange=(minNiv,maxNiv))
    plt.xticks(range(minNiv, maxNiv+1, 1))

    plt.xlabel("Niveau de zoom")
    plt.ylabel("temps de zoom")

    plt.savefig("output/durationNivZoom_"+NAME+".png")
    plt.show()


def drawGraphTypeEvents(df):
    plt.clf()
    
    sns.histplot(data=df, y='type', multiple='dodge', legend=False)
    plt.xlabel("Occurence")
    plt.ylabel("type")

    plt.savefig("output/typeEvents_"+NAME+".png")
    plt.show()


NAME = 'collegueJbeilin'
    
if __name__ == "__main__":

    df = pd.read_csv('data/allEvents_'+NAME+'.csv', sep=';')
    addSeconds(df)

    # df_click = df[df["type"].isin(["click"])]
    
    df_zoom = df[df["type"].isin(["zoomstart", "zoomend"])]
    calculateDurationZoom(df_zoom)
    
    # df_drag = df[df["type"].isin(["dragstart", "dragend"])]
    
    df_type = df[df["type"].isin(["dragstart", "zoom", "click"])]
    
    df_occNivZoom = df.loc[df.type=="zoomstart"]
    df_occNivZoom.loc[len(df_occNivZoom)] = df_zoom.iloc[-1]

    drawGraphTypeEvents(df_type)
    drawHistoNivZoom(df_occNivZoom)
    drawGraphNivZoomTime(df_occNivZoom)
    drawGraphNivZoomDuration(df_zoom)

    

    
    
    
    
    
    
