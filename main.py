#from angle_detect import angle_detec
#from warpping import unwarp
#from lines_deletion import lines_deletion
#from thresh import Prelem_Process
#from PIL.Image import *

from extract_grids import FindGridsAndUnwarp, OrderQuadri
from digit_recognizer import recognition
from solving import solution_sudoku, afficher
from calibration import calibration

import cv2
import numpy as np
import time
import math
import picamera
from impl_pwm import*

TAILLE_IMAGE_GRILLE=9*64

# Generation d'une matrice temporaire tant que calibration support pas effectuée
# MCalibPWM = np.float32([[1,0,0],[0,1,0],[0,0,1]])
# np.save('MCalibPWM.npy',MCalibPWM)
calibration()
MCalibPWM = np.load('MCalibPWM.npy')


camera = picamera.PiCamera()
camera.capture('1_initiale.jpg')
im = cv2.imread('1_initiale.jpg',0)


img = cv2.warpPerspective(im,MCalibPWM,(1000,665))

#img = cv2.imread('sudoku90.png',0)
listeGrilles, listeQuadris, listeCells, listeMOCR = FindGridsAndUnwarp(img, TAILLE_IMAGE_GRILLE)

for g in range(len(listeGrilles)):
	print('Traitement de la grille '+str(g))
	cv2.imshow('grille',listeGrilles[g])
	cv2.waitKey(1000)
	grilleNonResolue, angle = recognition(listeGrilles[g])
	
	print("La grille a resoudre est :")
	afficher(grilleNonResolue)
	
	grilleResolue = solution_sudoku(np.copy(grilleNonResolue))
	
	print("\nLa grille resolue est :")
	afficher(grilleResolue)

	cellules = []
	MROT=cv2.getRotationMatrix2D((TAILLE_IMAGE_GRILLE/2,TAILLE_IMAGE_GRILLE/2),-angle,1)
	for cell in listeCells[0]:
		cellule = np.float32([np.reshape(cell,(-1,2))])
		cellule = cv2.perspectiveTransform(cellule,listeMOCR[g])
		cellule = cv2.transform(cellule,MROT)
		cellule = OrderQuadri(cellule)
		cellules.append(cellule)
	
	list.sort(cellules, key=lambda cellule: cellule[0,0,1])
	for ligne in range(9):
		lignecellule=cellules[9*ligne:9*(ligne+1)]	
		list.sort(lignecellule, key=lambda cellule: cellule[0,0,0])
		cellules[9*ligne:9*(ligne+1)]=lignecellule[0:9]	
	
	MROTINV=cv2.getRotationMatrix2D((TAILLE_IMAGE_GRILLE/2,TAILLE_IMAGE_GRILLE/2),angle,1)
	MPINV=np.linalg.inv(listeMOCR[g])
	positions = []
	for cellule in cellules:
		cellule = cv2.transform(cellule,MROTINV)
		cellule = cv2.perspectiveTransform(cellule,MPINV)
		positions.append(cellule)
		
	grilleNonResolue=grilleNonResolue.reshape((-1))
	grilleResolue=np.int32(grilleResolue.reshape((-1)))
	#for CaseNR, CaseR, position in zip(grilleNonResolue, grilleResolue, positions):
		#if CaseNR == 0:
			# Remplacer le print suivant par l'appel à la fonction de tracé avec matrice de calibration PWM/caméra
			# print((CaseR,position.reshape((-1,2))))
			

	origine_grille = positions[72][0][3]
	grilleAEcrire= np.reshape(grilleResolue-grilleNonResolue,[-1,9])
	taille_grille = int(math.sqrt((positions[80][0][2][0]-positions[72][0][3][0])**2 + (positions[80][0][2][1]-positions[72][0][3][1])**2))
	
	vecteur_grille = [positions[80][0][2][0]-positions[72][0][3][0],positions[80][0][2][1]-positions[72][0][3][1]]
	angle_vecteur_grille = -math.atan2(vecteur_grille[1],vecteur_grille[0])
	
	origine_grille_cm=[27.5*origine_grille[0]/1000-0.2,18.3-18.3*origine_grille[1]/665-0.1]
	
	taille_grille_cm=27.5*taille_grille/1000
	
	
	print("La grille à écrire est :\n",grilleAEcrire , "\n")
	print("origine_grille=", origine_grille_cm, "\n")
	print("angle_vecteur_grille=", angle_vecteur_grille, "\n")
	print("taille_grille=", taille_grille_cm, "\n")
	 
	 

	tracer_grille(grilleAEcrire,taille_grille_cm/10.8,angle_vecteur_grille,origine_grille_cm)
	
	# vect2 = [positions[80][0][3][0]-positions[72][0][coeff_coin][0],0]
	# angle_grille = math.acos(((vect1[0]*vect2[0])+(vect1[1]*vect2[1]))/(math.sqrt(vect1[0]**2+vect1[1]**2)*math.sqrt(vect2[0]**2+vect2[1]**2)))-angle*math.pi/180