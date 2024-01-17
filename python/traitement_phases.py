import os
import pandas as pd
import json
import math
import warnings

warnings.simplefilter('ignore')



#--------------------------new dataframe conversion-------------------------------


def df_conversion(allevents_csv): 
    allevents=pd.DataFrame(allevents_csv)
    seconds(allevents)
    to_xy(allevents,'trans','xyTrans')
    #to_xy(allevents,'NOcorner','xyNO')
    new = allevents[['type', 'temps','sec','xyTrans']].copy()
    return new


#-----------------------------df distances--------------------------------------


def df_dist(df_converti):
    new = df_converti[['type', 'temps','sec','xyTrans']].copy().assign(dist_DA=None,dist_cumul=None)
    
    '''on crée une liste des indexs pour chaque type'''
    imovestart = new.index[new['type'] == 'movestart'].tolist()
    imoveend = new.index[new['type'] == 'moveend'].tolist()
    idragstart = new.index[new['type'] == 'dragstart'].tolist()
    idragend = new.index[new['type'] == 'dragend'].tolist()
    last = new.last_valid_index()
    #dist_DA
    for k, indexe in enumerate(idragend):
        indexs = idragstart[k]
        new['dist_DA'][indexe]=dist(new['xyTrans'][indexe],new['xyTrans'][indexs])
    #dist_cumul
    for k, indexe in enumerate(imoveend):
        indexs = imovestart[k]
        sub_df = new.iloc[indexs:indexe]
        #initialisation de l'itération avec exception pour le premier movestart du csv
        if indexs == 0 : new['dist_cumul'][indexs] = dist((0,0),new['xyTrans'][indexs])
        else : new['dist_cumul'][indexs] = 0
        for index, row in sub_df.iterrows():
            if index != last :
                new['dist_cumul'][index+1] = new['dist_cumul'][index] + dist(new['xyTrans'][index],new['xyTrans'][index+1])
    return new






#-------------------------------phases------------------------------------------
'''
Phases (de movestart à moveend, ou zoomstart à zoomend):    #zoomstart = movestart , zoomend = moveend = zoom
    0 : click
    1 : petit pan
    2 : gros pan
    3 : petit pan + élan (simple élan)
    4 : gros pan + élan
    5 : petit zoom
    6 : gros zoom (succession rapide de petits zoom)
    7 : petit pan long (on parcourt la map et on revient près du point de départ)
    8 : gros pan long (on parcourt la map et on va assez loin du point de départ)
'''



def phases(allevents_csv,seuil_gros_pan):
    df = df_dist(df_conversion(allevents_csv))[['type', 'temps','sec','xyTrans','dist_DA','dist_cumul']].copy().assign(phase=None)
    
    '''on crée une liste des indexs pour chaque type'''
    iclicks = df.index[df['type'] == 'click'].tolist()
    #imovestart = df.index[df['type'] == 'movestart'].tolist()
    imoveend = df.index[df['type'] == 'moveend'].tolist()
    idragstart = df.index[df['type'] == 'dragstart'].tolist()
    idragend = df.index[df['type'] == 'dragend'].tolist()
    izoomstart = df.index[df['type'] == 'zoomstart'].tolist()
    izoomend = df.index[df['type'] == 'zoomend'].tolist()
    for index in iclicks :
        #click
        df['phase'][index] = 0
    for k, indexs in enumerate(idragstart) :
        indexe = idragend[k]
        if df['dist_DA'][indexe]<seuil_gros_pan:
            if df['type'][indexe+1]!='moveend' : #si pan sans élan, df['type'][indexe+1]='move'
                #petit pan + élan
                indexm = next_moveend(imoveend,indexs)
                df['phase'][indexs-1] = 3
                df['phase'][indexm] = 3
            else : 
                if df['dist_cumul'][indexe]<2*df['dist_DA'][indexe]:
                    #petit pan
                    df['phase'][indexs-1] = 1
                    df['phase'][indexe+1] = 1
                else :
                    #petit pan long
                    df['phase'][indexs-1] = 7
                    df['phase'][indexe+1] = 7
        else :
            if df['type'][indexe+1]!='moveend' : #si pan sans élan, df['type'][indexe+1]='move'
                #gros pan + élan
                indexm = next_moveend(imoveend,indexs)
                df['phase'][indexs-1] = 4
                df['phase'][indexm] = 4
            else : 
                if df['dist_cumul'][indexe]<2*df['dist_DA'][indexe]:
                    #gros pan
                    df['phase'][indexs-1] = 2
                    df['phase'][indexe+1] = 2
                else :
                    #gros pan long
                    df['phase'][indexs-1] = 8
                    df['phase'][indexe+1] = 8
    
    
    df['phase'].iloc[izoomstart] = 5 #un zoom est petit tant qu'il n'a pas été prouvé qu'il est grand
    for k in range(len(izoomstart)-1):
        indexs = izoomstart[k]
        indexe = izoomend[k]
        indexs_suiv = izoomstart[k+1]
        indexe_suiv = izoomend[k+1]
        df['phase'][indexe+1] = 5 #un zoom est petit tant qu'il n'a pas été prouvé qu'il est grand
        if df['sec'][indexe]==df['sec'][indexs_suiv] :
            df['phase'][indexe+1] = None # +1 pour que la phase apparaisse à côté du moveend et non du zoomend
            df['phase'][indexs_suiv] = None
            df['phase'][indexe_suiv+1] = 6
            if df['phase'][indexs-1] == None:
                df['phase'][indexs] = None
            else :
                df['phase'][indexs] = 6
                
    return df
     
    

            
#----------------------------fonctions annexes---------------------------------

def to_xy(df,old_colonne,new_colonne):
    lst_xy = []
    for index, row in df.iterrows():
        s = row[old_colonne]
        (x,y)=(0,0)
        if type(row[old_colonne]) == str:
            #strip 'Point()' split ','
            for i in range(len(s)):
                if s[i]=='(': a=i+1
                if s[i]==',': b=i
                if s[i]==' ': c=i+1
                if s[i]==')': d=i
            x = float(s[a:b]) #lat
            y = float(s[c:d]) #lon
        lst_xy.append((x,y))
    df[new_colonne] = lst_xy
        



def seconds(df):
    lst_sec = []
    
    for line in df.itertuples():
        time = 0
        if type(line[2]) == str:
            dico_time = json.loads(line[2])
            time = dico_time['min'] * 60 + dico_time['sec'] + dico_time['mili'] * 1E-3
        lst_sec.append(time)
    df['sec'] = lst_sec



def dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2)


def next_moveend(imoveend,indexs):
    for val in imoveend :
        if val>indexs : return val


#-----------------------------------main---------------------------------------


if __name__ == '__main__':
    allevents_csv = pd.read_csv("data\\allEvents.csv",delimiter=';')
    
    
    #df_conversion(allevents_csv).to_csv(r"C:\Users\lilia\Documents\Work ENSG\ING2\PIR\tests_v3b\test2\df_converti.csv",sep=';',index=False)
    #df_dist(df_conversion(allevents_csv)).to_csv(r"C:\Users\lilia\Documents\Work ENSG\ING2\PIR\tests_v3b\test2\df_dist.csv",sep=';',index=False)
    
    seuil_gros_pan = 300 #en px, distance à partir de laquelle on considère le pan comme "gros"
    test = phases(allevents_csv,seuil_gros_pan)

    test.to_csv("output//testphases_seuil_gros_pan300.csv",sep=';',index=False)

    filtered_move = test.loc[test['type'] != 'move']
    filtered_move.to_csv("output//testphases_seuil_gros_pan300_filtered.csv",sep=';',index=False)
    
    
    