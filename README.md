# Un robot solveur de sudoku

Ce projet permet de résoudre et remplir une grille de sudoku à l'aide d'un Raspberry Pi et d'une table traçante.

Le projet est décrit plus en détails dans [ce rapport](doc/Rapport_final.pdf), ainsi que dans cette[présentation](doc/Soutenance.pdf).

> Vidéo de démonstration :

> [![Watch the video](https://github.com/bonnetv/Sudoku-solver/blob/master/img/Capture.JPG)](https://drive.google.com/open?id=1vr8ph6N277OrLa1NCr08aWasJZEI5jlR)


## Spécifications techniques

* Système : **Raspberry 3B** avec une carte MicroSD de **16Go minimum**.
* Système d'exploitation : **Raspian Stretch**.
* Langage de programmation : **Python 3**.
* Table traçante : **Servogor 790**

La commande du traceur XY se fait par les PWM Hardware, ce qui nécessite une configuration particulière. Il faut suivre la procédure décrite ici :
[http://www.jumpnowtek.com/rpi/Using-the-Raspberry-Pi-Hardware-PWM-timers.html](http://www.jumpnowtek.com/rpi/Using-the-Raspberry-Pi-Hardware-PWM-timers.html)

L'utilisation des PWM nécessite une exécution en mode Super Utilisateur.

La bibliothèque OpenCV 3.4.1 a été installée en suivant le guide suivant (sans installer l'environnement virtuel) :
[https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi)

L'installation est très longue (plus de 4 heures). 
Bien passer la taille du swap à 1024 pour la compilation d'OpenCV
et la repasser en normal après.

La base de donnée d'apprentissage pour la reconnaissance des chiffres est extraite de la base [Chars74K](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/) (*de Campos* et al)


## Descriptif du répertoire ./src

- `dataset.zip`					  Répertoire contenant les images pour l'apprentissage de la reconnaissance de caractères
- `digit_learner.py`		  Programme d'apprentissage de la base de caractères générant des fichiers de données
- `main.py`					      Programme principal. Bien l'exécuter en mode super-utilisateur via "sudo python3 main.py"
- `alarm.py`				      Module de pilotage de la LED pour indiquer une erreur
- `ecriture.py`				    Module pour le tracé des chiffres
- `digit_recognizer.py`		Module pour la reconnaissance des chiffres
- `extract_grids.py`		  Module pour l'extraction des grilles et de leur contenu
- `pwm.py`					      Module de pilotage des sorties PWM
- `calibration.py`			  Module pour la calibration table traçante / caméra
- `impl_pwm.py`				    Programme de test de sorties PWM
- `solving.py`				    Module de résolution d'une grille de Sudoku
- `(digitresponses.data)`	Fichier base de données créé par digit_learner.py contenant les labels des digits
- `(digitsamples.data)`		Fichier base de données créé par digit_learner.py contenant les caractéristiques des digits
- `MCalibPWM.npy`			    Matrice de calibration créé par calibration.py et utilisé dans main.py


## Mode d'emploi

- Étape 0 : dans un terminal, se placer dans le dossier du code source et décompresser `dataset.zip`.

- Étape 1 : (si première exécution) exécuter `digit_learner.py` séparément afin de générer les fichiers de données .data nécessaires à l'apprentissage de l'algorithme des k plus proches voisins :

> ```
> python3 digit_learner.py
> ```

- Étape 2 : exécuter `main.py` EN MODE SUPER-UTILISATEUR :

> ```
> sudo python3 main.py
> ```

Lors de son exécution, l'algorithme génèrera des images dans le dossier du code qui permettent d'évaluer le fonctionnement ou non de l'algorithme.
