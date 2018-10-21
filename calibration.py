import numpy as np
import cv2

def calibration():

    # Ectriture de la zone maximale de la table traçante
    #pts1 = np.float32([[771,208],[804,676],[104,229],[83,688]]) # [[.,YMIN],[XMAX,.],[XMIN,.],[.,YMAX]]
    pts1 = pts1 = np.float32([[87,236],[723,227],[62,700],[756,682]]) # [[.,YMIN],[XMAX,.],[XMIN,.],[.,YMAX]]
    
    # Capture d'une image
    # camera = picamera.PiCamera()
    
    # Détection de la zone d'écriture et recadagre sur cette zone
    # pts1 = np.float32([point_YMIN,point_XMAX,point_XMIN,point_YMAX]) # [[.,YMIN],[XMAX,.],[XMIN,.],[.,YMAX]]
    # pts2 correspond aux coordonnées de fin, M la matrice de transformation et dst l'image finale
    pts2 = np.float32([[0,0],[1000,0],[0,665],[1000,665]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    #dst = cv2.warpPerspective(img,M,(taille,taille))
    
    np.save('MCalibPWM',M)
    
    
        
    