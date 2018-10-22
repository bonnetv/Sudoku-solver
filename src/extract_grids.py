import numpy as np
import cv2
from math import atan2
from alarm import alarm

#Nombre de cases du Sudoku
nbCases=9*9

ratioAireGrilleCases=1.50
ratioAireChiffreCase=48.0

# Ordre de rangement des informations de hierarchie des contours
SUIVANT=0
PRECEDENT=1
ENFANT=2
PARENT=3

BLANC=(255, 255, 255)
GRIS=(127,127,127)
NOIR=(0,0,0)
EPAISSEUR=1+2*1
REMPLIR=-1

def Polygone(contour,nbCotes):
	
	"""
	Cette fonction renvoie le contour à nbCotes cotés le plus proche du contour en entrée
	@param      contour         Contour initial que l'on cherche à approximer
	@param      nbCotes         Entier désignant le nombre de cotés que doit avoir l'approximation du contour en entrée
	@return     poly         	Contour approximé   
	"""

	approx=1 # Erreur maximale tolérée entre le contour initial et celui approximé (en pourcentage)
	poly=cv2.approxPolyDP(contour,approx,True)
	while len(poly)>nbCotes:
		approx += 1
		poly=cv2.approxPolyDP(contour,approx,True)
	return poly	

def OrderQuadri(cellule):
	# Modification de la persepective
	# L'ordre des points est très important
	quadri=np.reshape(np.copy(cellule),(1,-1,2))
	centre=np.float32([quadri[0,:,0].mean(),quadri[0,:,1].mean()])
	liste_points=[]
	for i in range(len(quadri[0])):
		liste_points.append([quadri[0][i][0], quadri[0][i][1], atan2(quadri[0,i,1]-centre[1],quadri[0,i,0]-centre[0])])
	liste_points.sort(key=lambda point: point[2])
	for i in range(len(quadri[0])):
		quadri[0][i][0]=liste_points[i][0]
		quadri[0][i][1]=liste_points[i][1]
	return quadri
	
def Unwarp(img, quadri, taille):
	
	"""
	Cette fonction permet, à partir d'une image et d'un contour et récupérer une nouvelle image comprenant uniquement ce contour (ici nommé quadri)
	@param      img         Image avec erreur de perspective
	@param      quadri      Contour (dans le cadre de notre traitement il s'agira du contour d'une grille)
	@param		taille		Entier correspondant à la taille de l'image finale
	@return     dst         Image de la grille uniquement   
	@return     M			Matrice de transformation pour passer de l'image originale à l'image finale
	"""
	# Modification de la persepective
	# L'ordre des points est très important
	cellule=np.reshape(np.copy(quadri),(1,-1,2))
	pts1 = np.float32(OrderQuadri(cellule).reshape(-1,2))
	pts2 = np.float32([[0,0],[taille,0],[taille,taille],[0,taille]])
	# point_XMIN = quadri[0][0]
	# point_XMAX = quadri[0][0]
	# point_YMIN = quadri[0][0]
	# point_YMAX = quadri[0][0]
	# 
	# indice_X_MIN = 0
	# indice_X_MAX = 0
	# indice_Y_MIN = 0
	# indice_Y_MAX = 0
	# 
	# liste_X = []
	# liste_Y = []
	# 
	# for i in range(len(quadri)) :
	# 	liste_X.append([quadri[i][0][0],i])   
	# 	liste_Y.append([quadri[i][0][1],i]) 

##  	point_XMIN = quadri[min(liste_X)[1]][0]
	# point_XMAX = quadri[max(liste_X)[1]][0]
	# point_YMIN = quadri[min(liste_Y)[1]][0]
	# point_YMAX = quadri[max(liste_Y)[1]][0]
	# 
	# # Modification de perspective, pts1 correspond aux points que l'on veut modifier
	# pts1 = np.float32([point_YMIN,point_XMAX,point_XMIN,point_YMAX]) # [[.,YMIN],[XMAX,.],[XMIN,.],[.,YMAX]]
	# pts2 correspond aux coordonnées de fin, M la matrice de transformation et dst l'image finale
	# pts2 = np.float32([[0,0],[taille,0],[0,taille],[taille,taille]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(taille,taille))
	
	# https://docs.opencv.org/3.0-beta/modules/imgproc/doc/geometric_transformations.html#warpperspective
	# https://docs.opencv.org/3.0-beta/modules/core/doc/operations_on_arrays.html#perspectivetransform
	# http://answers.opencv.org/question/252/cv2perspectivetransform-with-python/
	# print(cv2.perspectiveTransform(np.array([pts1]),M))
	# print(cv2.perspectiveTransform(np.array([pts2]),np.linalg.inv(M)))
	return dst, M

def TracePolygone(img, poly, couleur, epaisseur):
	
	"""
	Cette fonction permet de tracer sur une image un contour
	@param      img         Image initiale
	@param      poly      	Contour que l'on souhaite tracer
	@param		couleur		Entier correspondant à la couleur du tracé
	@param		epaisseur	Entier correspondant à l'épaisseur du tracé
	"""
	if len(poly) > 1:
		for k in range(len(poly)-1):
			cv2.line(img, (poly[k][0][0],poly[k][0][1]), (poly[k+1][0][0],poly[k+1][0][1]), couleur, epaisseur)
		cv2.line(img, (poly[len(poly)-1][0][0],poly[len(poly)-1][0][1]), (poly[0][0][0],poly[0][0][1]), couleur, epaisseur)
			
def FindGridsAndUnwarp(img, taille):
	if max(img.shape) > (3280//2):
		imgs = cv2.resize(img, (img.shape[1]//2,img.shape[0]//2))
	else:
		imgs = img
	thr=cv2.adaptiveThreshold(np.copy(imgs),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,45,3)
	if __debug__ or True:  # Image de contrôle pour comprendre ce qui se passe
		cv2.imwrite('threshold.png',thr)
	thr1 = np.copy(thr)
	im2, contours, hierarchy = cv2.findContours(thr1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# On va compter le nombre d'enfants hiérarchiques de chaque contour identifié
	# pouvant correspondre à la surface d'une case par rapport à celle de la grille
	nbEnfantsAssezGrands=[0]*len(contours)
	surfacePlusGrandEnfant=[0.0]*len(contours)
	for k in range(len(hierarchy[0])):
		monParent = hierarchy[0][k][PARENT]
		if (monParent >= 0):
			monAireParent = cv2.contourArea(contours[monParent])
			monAire = cv2.contourArea(contours[k])
			if monAire > surfacePlusGrandEnfant[monParent]:
				surfacePlusGrandEnfant[monParent] = monAire
			if (ratioAireGrilleCases*nbCases*monAire > monAireParent):
				nbEnfantsAssezGrands[monParent] += 1
	
	listeGrilles = []
	listeQuadris = []
	listeCells = []
	listeMOCR= []
	Compteur = 0
	for grille in range(len(contours)):
		if nbEnfantsAssezGrands[grille]==nbCases:
			masque = np.zeros(thr.shape,np.uint8)
			Compteur = Compteur + 1
			cadre = np.zeros(thr.shape,np.uint8)
			lignesCasesRemplies = []
			quadri = Polygone(contours[grille],4)
			TracePolygone(cadre,quadri,GRIS,1)
			aireGrille = cv2.contourArea(contours[grille])
			for case in range(len(contours)):
				monParent=hierarchy[0][case][PARENT]
				if monParent==grille:
					monAire = cv2.contourArea(contours[case])
					if (ratioAireGrilleCases*nbCases*monAire > aireGrille) and \
					(ratioAireChiffreCase*surfacePlusGrandEnfant[case] > monAire):
						# On garde les vraies cases contenant un chiffre
						cv2.drawContours(masque,contours,case,BLANC,REMPLIR)
						
						carre = Polygone(contours[case],4)
						if len(carre)==4:
							lignesCasesRemplies.append(carre)
							TracePolygone(cadre,carre,GRIS,1)	
						
						# On va aussi effacer les taches dans les
						# cases contenant un chiffre
						for forme in range(len(contours)):
							parentForme=hierarchy[0][forme][PARENT]
							if (parentForme==case) and \
							(cv2.contourArea(contours[forme])<surfacePlusGrandEnfant[case]):
								cv2.drawContours(masque,contours,forme,NOIR,REMPLIR)
								cv2.drawContours(masque,contours,forme,NOIR,EPAISSEUR)
					elif (ratioAireGrilleCases*nbCases*monAire > aireGrille):
						carre = Polygone(contours[case],4)
						if len(carre)==4:
							lignesCasesRemplies.append(carre)	
					# On érode le contour du masque de la case	
					cv2.drawContours(masque,contours,case,NOIR,EPAISSEUR)
			# on efface la grille externe			
			cv2.drawContours(masque,contours,grille,NOIR,EPAISSEUR)
			
			# On ne garde que le contenu du masque
			thrm=cv2.bitwise_and(masque,thr)
			# On corrige la perspective et on met à la taille voulue
			img_uwrp, M = Unwarp(thrm, quadri, taille)
			# Et on stocke les résultats
			listeGrilles.append(img_uwrp)
			listeQuadris.append(quadri)
			listeCells.append(lignesCasesRemplies)
			listeMOCR.append(M)
			
			if __debug__ or True : # Images de contrôle pour comprendre ce qui se passe
				cv2.imwrite('masque'+str(len(listeGrilles))+'.png',masque)
				cv2.imwrite('nombres'+str(len(listeGrilles))+'.png',cv2.bitwise_or(cadre,thrm))
				cv2.imwrite('unwarped'+str(len(listeGrilles))+'.png',img_uwrp)
				print('Grille '+str(len(listeGrilles))+', il y a '+str(len(lignesCasesRemplies))+' cases remplies')
##	try:
##            assert Compteur != 0, "erreur :"
##        except:
##            print("coucou")
##            print("Grille non détectée")
##        except:
##            print("Grille non détectée")
##            alarm()
	return listeGrilles, listeQuadris, listeCells, listeMOCR
