# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:39:28 2018

@author: Simon Spark
"""

import numpy as np
from math import*
#from pylab import*

#MOC otocoupleur, 4 pattes 2 masses pour entrée et sortie
#Ajouter l'agrandissement partout

calibre=0.1
#Référence la grille fait 9 cm 
#Ca nous permet de considérer que chaque case fait 1cm
# Donc agrandissement=taille/9
n=4000 #echantillonnage



def position (ligne,colonne,a,angle):   #Orientation et agrandissement ok
    # Permet de se positionner au centre de la case désirée
    # a=agrandissement
    u=(colonne*1.2+0.6)*calibre*a
    v=(10.8-ligne*1.2-0.6)*calibre*a
    x=u*cos(angle)-v*sin(angle)
    y=v*cos(angle)+u*sin(angle)
    return(x,y)      




def un (ligne, colonne, agrandissement,angle):
    # Renvoie la tesnion à chaque instant pour avoir le chiffre voulue
    # Au départ on se trouve au centre de la case
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    # Séquence 1
    haut=[1]
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(-0.2*t[i]*calibre)
        v.append(0)
        haut.append(1)
    # Séquence 2
    for i in range (1, n+1):
        haut.append(0)
        u.append(u[n]+0.2*t[i]*calibre)
        v.append(v[n]+0.4*t[i]*calibre)
        
    # Séquence 3
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[2*n])
        v.append(v[2*n]-0.8*t[i]*calibre)
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,3*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,3*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,3*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,3*n+1)]
    return (x,y,haut)

def deux (ligne, colonne, agrandissement, angle):
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    #Séquence 1
    haut=[1]
    for i in range(1,n+1):
        haut.append(1)
        u.append(-0.2*t[i]*calibre)
        v.append(+0.4*t[i]*calibre)
    #Séquence 2
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[n]+0.4*t[i]*calibre)
        v.append(v[n])
    #Séquence 3
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[2*n])
        v.append(v[2*n]-0.4*t[i]*calibre)
    #Séquence 4
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[3*n]-0.4*t[i]*calibre)
        v.append(v[3*n])
    #Séquence 5
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[4*n])
        v.append(v[4*n]-0.4*t[i]*calibre)
    #Séquence 6
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[5*n]+0.4*t[i]*calibre)
        v.append(v[5*n])
   #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,6*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,6*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,6*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,6*n+1)]
    return(x,y,haut)
 
def trois (ligne, colonne, agrandissement, angle):
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    #Séquence 1
    haut=[1]
    for i in range(1,n+1):
        haut.append(1)
        u.append(-0.3*t[i]*calibre)
        v.append(+0.4*t[i]*calibre)
    #Séquence 2
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[n]+0.6*t[i]*calibre)
        v.append(v[n])
    #Séquence 3
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[2*n])
        v.append(v[2*n]-0.8*t[i]*calibre)
    #Séquence 4
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[3*n]-0.6*t[i]*calibre)
        v.append(v[3*n])
    #Séquence 5
    for i in range(1,n+1):
        haut.append(1)
        u.append(u[4*n])
        v.append(v[4*n]+0.4*t[i]*calibre)
    #Séquence 6
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[5*n]+0.6*t[i]*calibre)
        v.append(v[5*n])
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,6*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,6*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,6*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,6*n+1)]
    return(x,y,haut)

    
def quatre (ligne, colonne, agrandissement,angle):
    # Renvoie le rapport cyclique à chaque instant pour avoir le chiffre voulue
    # Au départ on se trouve au centre de la case
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    # Séquence 1
    haut=[1]
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(+0.2*t[i]*calibre)
        v.append(0)
        haut.append(1)
    # Séquence 2
    for i in range (1, n+1): #Remplacer par la structure range
        haut.append(0)
        u.append(u[n]-0.6*t[i]*calibre)
        v.append(0)    
    # Séquence 3
    for i in range (1, n+1):
        haut.append(0)
        u.append(u[2*n]+0.4*t[i]*calibre)
        v.append(v[2*n]+0.4*t[i]*calibre)   
    # Séquence 4
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[3*n])
        v.append(v[3*n]-0.8*t[i]*calibre)
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,4*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,4*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,4*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,4*n+1)]
    return (x,y,haut)
    

def cinq (ligne, colonne, agrandissement, angle):
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    #Séquence 1
    haut=[1]
    for i in range(1,n+1):
        haut.append(1)
        u.append(+0.2*t[i]*calibre)
        v.append(+0.4*t[i]*calibre)
    #Séquence 2
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[n]-0.4*t[i]*calibre)
        v.append(v[n])
    #Séquence 3
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[2*n])
        v.append(v[2*n]-0.4*t[i]*calibre)
    #Séquence 4
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[3*n]+0.4*t[i]*calibre)
        v.append(v[3*n])
    #Séquence 5
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[4*n])
        v.append(v[4*n]-0.4*t[i]*calibre)
    #Séquence 6
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[5*n]-0.4*t[i]*calibre)
        v.append(v[5*n])
    print(len(u))
   #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,6*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,6*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,6*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,6*n+1)]
    return(x,y,haut)


def six (ligne, colonne, agrandissement, angle):
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    #Séquence 1
    haut=[1]
    for i in range(1,n+1):
        haut.append(1)
        u.append(+0.3*t[i]*calibre)
        v.append(+0.4*t[i]*calibre)
    #Séquence 2
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[n]-0.6*t[i]*calibre)
        v.append(v[n])
    #Séquence 3
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[2*n])
        v.append(v[2*n]-0.8*t[i]*calibre)
    #Séquence 4
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[3*n]+0.6*t[i]*calibre)
        v.append(v[3*n])
    #Séquence 5
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[4*n])
        v.append(v[4*n]+0.4*t[i]*calibre)
    #Séquence 6
    for i in range(1,n+1):
        haut.append(0)
        u.append(u[5*n]-0.6*t[i]*calibre)
        v.append(v[5*n])
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,6*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,6*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,6*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,6*n+1)]
    return(x,y,haut)

def sept (ligne, colonne, agrandissement,angle):
    # Renvoie le rapport cyclique à chaque instant pour avoir le chiffre voulue
    # Au départ on se trouve au centre de la case
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    # Séquence 1
    haut=[1]
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(-0.2*t[i]*calibre)
        v.append(+0.4*t[i]*calibre)
        haut.append(1)
    # Séquence 2
    for i in range (1, n+1):
        haut.append(0)
        u.append(u[n]+0.4*t[i]*calibre)
        v.append(v[n])
        
    # Séquence 3
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[2*n]-0.2*t[i]*calibre)
        v.append(v[2*n]-0.8*t[i]*calibre)
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,3*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,3*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,3*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,3*n+1)]
    return (x,y,haut)

def huit (ligne, colonne, agrandissement,angle):
    # Renvoie le rapport cyclique à chaque instant pour avoir le chiffre voulue
    # Au départ on se trouve au centre de la case
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    # Séquence 1
    haut=[1]
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(-0.2*t[i]*calibre)
        v.append(0)
        haut.append(1)
    # Séquence 2
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(u[n])
        v.append(+0.4*t[i]*calibre)
        haut.append(0)
    # Séquence 3
    for i in range (1, n+1): #Remplacer par la structure range
        haut.append(0)
        u.append(u[2*n]+0.4*t[i]*calibre)
        v.append(v[2*n])    
    # Séquence 4
    for i in range (1, n+1):
        haut.append(0)
        u.append(u[3*n])
        v.append(v[3*n]-0.8*t[i]*calibre)   
    # Séquence 5
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[4*n]-0.4*t[i]*calibre)
        v.append(v[4*n])
    # Séquence 6
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[5*n])
        v.append(v[5*n]+0.4*t[i]*calibre)
    # Séquence 7
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[6*n]+0.4*t[i]*calibre)
        v.append(v[6*n])
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,7*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,7*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,7*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,7*n+1)]
    return (x,y,haut)

def neuf (ligne, colonne, agrandissement,angle):
    # Renvoie le rapport cyclique à chaque instant pour avoir le chiffre voulue
    # Au départ on se trouve au centre de la case
    a=agrandissement
    t=np.linspace(0,1,n+1)
    u=[0]
    v=[0]
    # Séquence 1
    haut=[1]
    for i in range (1, n+1): #Remplacer par la structure range
        u.append(+0.2*t[i]*calibre)
        v.append(0)
        haut.append(1)
    # Séquence 2
    for i in range (1, n+1): #Remplacer par la structure range
        haut.append(0)
        u.append(u[n]-0.4*t[i]*calibre)
        v.append(0)    
    # Séquence 3
    for i in range (1, n+1):
        haut.append(0)
        u.append(u[2*n])
        v.append(0.4*t[i]*calibre)   
    # Séquence 4
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[3*n]+0.4*t[i]*calibre)
        v.append(v[3*n])
    # Séquence 5
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[4*n])
        v.append(v[4*n]-0.8*t[i]*calibre)
    # Séquence 5
    for i in range (1, n+1):
        haut.append(0)
        u.append (u[5*n]-0.4*t[i]*calibre)
        v.append(v[5*n])
    #Fin
    x=[u[i]*a*cos(angle)-v[i]*a*sin(angle)for i in range (0,6*n+1)]
    y=[v[i]*a*cos(angle)+u[i]*a*sin(angle)for i in range (0,6*n+1)]
    x=[x[i]+position(ligne,colonne,agrandissement,angle)[0]for i in range (0,6*n+1)]
    y=[y[i]+position(ligne,colonne,agrandissement,angle)[1]for i in range (0,6*n+1)]
    return (x,y,haut)


# Lignes de test des fonctions d'écriture
    
##print("La position renvoyé est", position (2,2,2,0) )
##
##seq_chiffre=neuf(2,2,2,0)
##x= seq_chiffre[0]
##y= seq_chiffre[1]
##
##
##plot(x,y)