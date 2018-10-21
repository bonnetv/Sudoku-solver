from pwm import PWM
import numpy as np
import time
import picamera

import RPi.GPIO as GPIO




from ecriture import un
from ecriture import deux
from ecriture import trois
from ecriture import quatre
from ecriture import cinq
from ecriture import six
from ecriture import sept
from ecriture import huit
from ecriture import neuf

from ecriture import position
from math import *
 

# Avant d'excecuter le code il est necessaire de creer des repertoires dans l'arborescence systeme du Rasberry Pi
# pour cela voir le lien http://www.jumpnowtek.com/rpi/Using-the-Raspberry-Pi-Hardware-PWM-timers.html


def lever_stylo (a, b) :
    if (a!=b) :
        if (a == 1):
            GPIO.output(35, GPIO.LOW) # Sortie au niveau logique bas
            print("On lève le stylo : Low")
        else :
            GPIO.output(35, GPIO.HIGH) # Sortie au niveau logique haut
            print("On baisse le stylo :High")
    return (1)



def stylo_haut () :
    GPIO.output(35, GPIO.LOW)
    print("Stylo en haut : LOW")
    return (1)

def choix(chiffre, ligne, colonne, agrandissement, angle):
    a=agrandissement;
    if (chiffre==1):
        return un(ligne, colonne, a, angle)
    if (chiffre==2):
        return deux(ligne, colonne, a, angle)
    if (chiffre==3):
        return trois(ligne, colonne, a, angle)
    if (chiffre==4):
        return quatre(ligne, colonne, a, angle)
    if (chiffre==5):
        return cinq(ligne, colonne, a, angle)
    if (chiffre==6):
        return six(ligne, colonne, a, angle)
    if (chiffre==7):
        return sept(ligne, colonne, a, angle)
    if (chiffre==8):
        return huit(ligne, colonne, a, angle)
    if (chiffre==9):
        return neuf(ligne, colonne, a, angle)
    else :
        print("La fonction choix ne reçoit pas un chiffre entre 1 et 9" )
        

def calibrage ():
    GPIO.setmode(GPIO.BOARD) # On lit les pattes dans l'ordre classique en électronique
    GPIO.setup(35, GPIO.OUT) # La broche 35 est configurée en sortie
    pwm_X = PWM(0)
    pwm_Y = PWM(1) # il n'existe que 2 canaux pour implementer les PWMs (0 et 1)
    pwm_X.export()
    pwm_Y.export()
    pwm_X.period = 100000 # les unites sont en nanosecondes, ainsi dans cet exemple la periode vaut 100000*1ns = 100 us
    pwm_Y.period = 100000
    GPIO.output(35, GPIO.HIGH)
    for i in range (0,int(pwm_Y.period/5)):
        pwm_Y.duty_cycle=5*i
        pwm_Y.enable = True
        
    for i in range (0,int(pwm_X.period/5)):
        
        pwm_X.duty_cycle=5*i
        pwm_X.enable = True
    
    for i in range (0,int(pwm_Y.period/5)):
        pwm_Y.duty_cycle=pwm_Y.period-5*i
        pwm_Y.enable = True
    
    for i in range (0,int(pwm_X.period/5)):
        pwm_X.duty_cycle=pwm_X.period-5*i
        pwm_X.enable = True
    
    pwm_X.enable = False
    pwm_Y.enable = False
    stylo_haut()
    time.sleep(1)
    pwm_X.duty_cycle=int(pwm_X.period/2)
    pwm_X.enable = True
    time.sleep(1)
    
    camera = picamera.PiCamera()
    camera.capture('calibrage.jpg')
    time.sleep(1)
    pwm_X.enable = False
    
    pwm_X.unexport()
    pwm_Y.unexport()
    GPIO.cleanup()
    return 1
                
def tracer_grille(grille, agrandissement, angle,origine):
    n=4000
    calibre=0.1
    pwm_X = PWM(0)
    pwm_Y = PWM(1) # il n'existe que 2 canaux pour implementer les PWMs (0 et 1)
    pwm_X.export()
    pwm_Y.export()
    pwm_X.period = 100000 # les unites sont en nanosecondes, ainsi dans cet exemple la periode vaut 100000*1ns = 100 us
    pwm_Y.period = 100000

    GPIO.setmode(GPIO.BOARD) # On lit les pattes dans l'ordre classique en électronique
    GPIO.setup(35, GPIO.OUT) # La broche 35 est configurée en sortie

##La fréquence max du lever/baisser de stylo et 4Hz. Donc 250ms.

###    Ecriture de la grille
       
    for i in range (0, len(grille)):
        for j in range(0, len(grille[0])):
               
            if (grille[i][j]!=0):
                
                seq_chiffre=choix(grille[i][j], i, j, agrandissement, angle  )
             
                x=seq_chiffre[0]
                y=seq_chiffre[1]
                haut=seq_chiffre[2]
                for k in range(0, len(x)):
                    x[k]+=origine[0]*calibre
                    y[k]+=origine[1]*calibre
           
        
                stylo_haut();
           
            
                for k in range(0,len(x)):
                    if(k!=0):
                        lever_stylo (haut[k], haut[k-1])
                
                    pwm_X.duty_cycle=int(x[k]*pwm_X.period/3.3)
                    pwm_Y.duty_cycle=int(y[k]*pwm_Y.period/3.3)
                    pwm_X.enable = True 
                    pwm_Y.enable = True
                stylo_haut()
              
   
#Lorsque l'on a termine avec la table tracante
    pwm_X.enable = False # On desactive la PWM
    pwm_Y.enable = False
    pwm_X.unexport()
    pwm_Y.unexport()
    GPIO.cleanup() # A la fin du programme on remet à 0 les broches du Rasberry PI
    return(0)

#Test de ce fichier

#calibrage()
##grille=[[1, 2, 0], [ 4, 0, 6], [7, 8, 9,]] #Grille obtenue par l'algo de résolution
##grille=[[ 8,  3, 9,  4,  6,  5,  7,  0,  0],
##        [ 1,  4,  6,  7,  8,  2,  9,  5,  0],
##        [ 7,  5,  0,  0,  9,  1,  0,  8,  6],
##        [ 3,  9,  0,  0,  2,  4,  6,  7,  0],
##        [ 5,  0,  4,  1,  0,  3,  0,  2,  9],
##        [ 2,  8,  7,  6,  5,  0,  3,  4,  1],
##        [ 6,  2,  0,  0,  3,  7,  1,  9,  4],
##        [ 0,  1,  3,  2,  0,  8,  0,  6,  7],
##        [0, 0,  5,  9,  1,  0,  2,  3,  8]] 
##
##agrandissement = 1
##angle=0
##origine=[6.6,4.4]
##tracer_grille(grille,agrandissement,angle,origine)

