# -*- coding: utf-8 -*-
"""
Created on Wed Dec 6 11:25:01 2023

@author: vanes
"""

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def addSeconds(df):
    lst_sec = []
    
    for line in df.itertuples():
        time = 0
        if type(line[2]) == str:
            dico_time = json.loads(line[2])
        time = dico_time['min'] * 60 + dico_time['sec'] + dico_time['mili'] * 1E-3
        lst_sec.append(time)
        
    df['sec'] = lst_sec

def pointToCoord(point):
     return [float(s) for s in point.strip("Point()").split(",")]

def latlngToCoord(latlng):
    return [float(s) for s in latlng.strip("LatLng()").split(",")]

def eventCoords(df, df_zoom):
    lst = []
    for i in range(df_zoom.shape[0]-1):

        if i%2 == 0:
            
            start = df_zoom.iloc[i, 7]
            end = df_zoom.iloc[i+1, 7]

            k = df[df['sec'] <= start].index.values[-1]
            l = df[df['sec'] <= end].index.values[-1]
            
            lst.append(df[k:l+1])

    return lst


NAME = 'iamvdo'

if __name__ == "__main__":
    
    df = pd.read_csv('data/mouseMoveEvents_'+NAME+'.csv', sep=';')
    
    del df['NOcorner']
    del df['center']
    del df['nivZoom']
    
    addSeconds(df)
    
    dfAllEvents = pd.read_csv('data/allEvents_'+NAME+'.csv', sep=';')
    addSeconds(dfAllEvents)
    
    ###################### dataframe toutes les coords mouseMove ##############
    
    df_latlong = df['posLatLon'].apply(latlngToCoord)
    df['xy'] = df['posPix'].apply(pointToCoord)
    
    df['x'] = df['xy'].apply(lambda x: x[0])
    df['y'] = df['xy'].apply(lambda x: x[1])
    
    df_n = df[['x', 'y']]
    
    ###################### dataframe events zoom #########################
    
    df_zoom = dfAllEvents[dfAllEvents["type"].isin(["zoomstart", "zoomend"])]
    zoomCoords = eventCoords(df, df_zoom)
    
    ###################### dataframe events dragstart #########################
    
    df_drag = dfAllEvents[dfAllEvents["type"].isin(["dragstart", "dragend"])]
    dragCoords = eventCoords(df, df_drag)

    
    # ###################### Graphiques #########################

    # ###################### Zoom #########################
    
    plt.figure()
    # sns.scatterplot(data=df, x="x", y="y")
    
    # for i in range(len(zoomCoords)):
    #     df_zoom1 = zoomCoords[i]
    #     sns.scatterplot(data=df_zoom1, x="x", y="y", color='red')
    
    # plt.savefig("output/tracePoint_mouse_"+NAME+".png")

    # ###################### drag #########################
    
    # plt.figure()

    for i in range(len(dragCoords)):
        df_drag1 = dragCoords[i]
        sns.scatterplot(data=df_drag1, x="x", y="y", color='green')
    


    # plt.figure()
    # plt.plot(df['x'], df['y'])
    
    # for i in range(len(k)):
    #     df_zoom1 = k[i]
    #     sns.scatterplot(data=df_zoom1, x="x", y="y", color='red')
    
    # plt.savefig("output/traceLine_mouse_"+NAME+".png")
    
    # for i in range(len(k)):
    #     plt.figure()
    #     df_zoom1 = k[i]
    #     sns.scatterplot(data=df_zoom1, x="x", y="y", color='red')
    
    # plt.figure()
    # plt.hist2d(df['x'], df['y'])
    # plt.colorbar()
    # plt.savefig("output/heatmap_mouse_"+NAME+".png")


    

