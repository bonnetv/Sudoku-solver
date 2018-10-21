"""
@author     Valentin
@brief      Stuff to deal with the resolution of a numpy 9x9-sudoku

Helped from the steps mentionned in this document from Jules Svartz:
http://perso.numericable.fr/jules.svartz/prepa/IPT_spe/TP_sudoku.pdf
"""

import numpy as np
import time

AL = [
[1, 0, 0, 0, 0, 7, 0, 9, 0],
[0, 3, 0, 0, 2, 0, 0, 0, 8],
[0, 0, 9, 6, 0, 0, 5, 0, 0],
[0, 0, 5, 3, 0, 0, 9, 0, 0],
[0, 1, 0, 0, 8, 0, 0, 0, 2],
[6, 0, 0, 0, 0, 4, 0, 0, 0],
[3, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 4, 0, 0, 0, 0, 0, 0, 7],
[0, 0, 7, 0, 0, 0, 3, 0, 0],
]

L0 = [
[0, 9, 0, 0, 2, 0, 0, 0, 0],
[0, 0, 8, 1, 0, 0, 7, 0, 4],
[1, 0, 0, 0, 0, 0, 0, 5, 0],
[6, 0, 0, 0, 0, 0, 0, 0, 0],
[9, 0, 0, 0, 0, 0, 0, 0, 6],
[0, 1, 0, 5, 0, 0, 2, 0, 0],
[0, 0, 0, 0, 0, 6, 9, 0, 0],
[7, 0, 0, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 4, 6, 0, 2],
]


L1 = [
[0, 0, 0, 0, 7, 0, 0, 6, 0],
[3, 0, 4, 0, 0, 5, 1, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 0, 5],
[0, 0, 0, 0, 0, 0, 0, 0, 2],
[0, 0, 2, 0, 0, 0, 0, 0, 6],
[7, 0, 0, 0, 0, 8, 0, 5, 0],
[6, 0, 0, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 9, 0, 0, 3],
[2, 0, 7, 4, 0, 0, 0, 0, 0],
]


#Most difficult sudoku ever (starts by 9 8 7)
L2 =[
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 3, 0, 8, 5],
[0, 0, 1, 0, 2, 0, 0, 0, 0],
[0, 0, 0, 5, 0, 7, 0, 0, 0],
[0, 0, 4, 0, 0, 0, 1, 0, 0],
[0, 9, 0, 0, 0, 0, 0, 0, 0],
[5, 0, 0, 0, 0, 0, 0, 7, 3],
[0, 0, 2, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 4, 0, 0, 0, 9]
]


L3=[
[0, 9, 0, 2, 0, 0, 6, 0, 5], 
[3, 2, 0, 0, 0, 7, 0, 0, 0], 
[0, 7, 0, 9, 0, 5, 0, 0, 8], 
[0, 1, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 7, 0, 0, 0, 0, 9, 4], 
[6, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 8, 0, 0, 0, 0, 0, 7], 
[0, 3, 0, 4, 9, 1, 5, 0, 0], 
[0, 0, 0, 0, 0, 3, 0, 0, 0]
]


L4=[
[8, 9, 0, 2, 3, 4, 6, 7, 5], 
[3, 2, 5, 6, 8, 7, 4, 1, 9], 
[4, 7, 6, 9, 0, 5, 3, 2, 8], 
[9, 1, 4, 7, 5, 2, 8, 6, 0], 
[2, 5, 7, 3, 6, 8, 1, 9, 4], 
[6, 8, 3, 1, 4, 9, 7, 5, 0], 
[1, 4, 8, 5, 2, 6, 9, 3, 7], 
[7, 3, 2, 4, 9, 1, 5, 8, 6], 
[5, 6, 9, 8, 7, 3, 2, 4, 1]
]

"""bool isInTheLine[9][9];
bool isInTheColumn[9][9];
bool isInTheBlock[9][9];
"""

def chiffres_ligne(L, i, withzero):
    """
    @param      L   a sudoku grid
    @param      i   a line index of the sudoku
    @param      withzero    TODO: A RAJOUTER 
    @return     liste   a list with the digits belonging to a line
    @brief      Renvoie les digits d'une ligne
    """
    
    liste = []
    
    for digit in L[i]:
        if withzero:
            liste.append(digit)
        elif digit != 0:
            liste.append(digit)
    return(liste)
    
def chiffres_colonne(L, j, withzero):
    """
    @param      L   a sudoku grid
    @param      j   a column index of the sudoku 
    @return     liste   a list with the digits belonging to a column
    @brief      Renvoie les digits d'une colonne
    """
    
    liste=[]
    
    for i in range(0,9):
        if withzero:
            liste.append(L[i][j])
        elif L[i][j] != 0:
            liste.append(L[i][j])
    return(liste)
    
def chiffres_bloc(L, i, j, withzero):
    """
    @param      L   a sudoku grid
    @param      i   a line index of the sudoku
    @param      j   a column index of the sudoku 
    @return     liste   a digit list
    @brief      Renvoie les digits du bloc dans lequel est située la case [i][j]
    """
    
    liste=[]
    
    i_bloc = i-i%3      #ligne de début du bloc
    j_bloc = j-j%3      #colonne de début du bloc
    
    for k in range(i_bloc, i_bloc+3):
        for l in range(j_bloc, j_bloc+3):
            if withzero:
                liste.append(L[k][l])
            elif L[k][l]!=0:
                liste.append(L[k][l])
    return(liste)

def chiffres_conflit(L, i, j):
    """
    @param      L   a sudoku grid
    @param      i   a line index of the sudoku
    @param      j   a column index of the sudoku 
    @return     liste   a digit list
    @brief      Renvoie la liste des digits qui ne peuvent pas occuper la case [i][j]
    """
    
    liste=[]            #la liste finale à renvoyer
    
    liste_ligne = chiffres_ligne(L, i, False)
    liste_col = chiffres_colonne(L, j, False)
    liste_bloc = chiffres_bloc(L, i, j, False)

    
    for digit in range(1,10):
        if (digit in liste_ligne) | (digit in liste_col) | (digit in liste_bloc):
            liste.append(digit)
    return(liste)

#print(chiffres_conflit(L, 0, 0))
    
    

def case_suivante(L, nb_possible, i_min, j_min, ordre_sudoku):
    """
    @param      L               a sudoku grid
    @param      nb_possible     matrix containing the number of digits able to fill the (i,j) case
    @param      i_min           a line index of the sudoku
    @param      j_min           a column index of the sudoku
    @param      ordre_sudoku    the sudoku order (ex: 9x9 -> 9)
    @return     a couple of case index
    @brief      Renvoie la case suivante à traiter dans le sudoku.
    """
    
    liste = []; #Utile pour les cas où il n'y a qu'une seule possibilité de candidat
    
    #On cherche les indices des coefficients ayant un nombre de possibilités supérieur ou égal à celui du coefficient (i,j)


    #Etape 0 : vérification de la validité de la grille
    """Une grille non valide est caractérisée par une case (i,j) n'ayant aucun digit autorisé (nb_possible[i][]=0), ayant une valeur nulle L[i][j]=0 dans la grille"""

    for i in range(0,9):
        for j in range(0,9):
            if nb_possible[i][j]==0 and L[i][j]==0:
                return((i,j))
    
    #Etape 1 : remplir les cases avec une seule possibilité
    
    for i in range(0, ordre_sudoku):
        for j in range(0, ordre_sudoku):
            if nb_possible[i][j]==1:
                liste.append((i,j))
        
    if len(liste) != 0:
        return(liste)
        
    #Étape 2 : sinon, remplir la première case avec le moins de possibilités possibles
    
    for m in range(2,9):
        for i in range(0, ordre_sudoku):
            for j in range(0, ordre_sudoku):
                if nb_possible[i][j]==m :
                    return((i,j))
        
    return((9,0))
    
def ordre_backtracking(L, ordre_sudoku):
    """
    @param      L   a sudoku grid to solve
    @return     nb_possible  a matrix with same dimension as the sudoku grid, containing : 
    @brief      Permet de déterminer le nombre possibilités restantes pour chaque case (i,j)
    
    """
    nb_possible = np.zeros((9,9))  
    for i in range(0,9):
        for j in range(0,9):
            if L[i][j] != 0:
                nb_possible[i][j]=0;
            else:
                a=chiffres_ligne(L, i, False)
                b=chiffres_colonne(L, j, False)
                c=chiffres_bloc(L,i,j, False)
                nb_possible[i][j]= ordre_sudoku-len(set(a)|set(b)|set(c))

    return(nb_possible)
            

def solution_sudoku(L):
    """
    @param      L   a sudoku grid to solve
    @return     the sudoku grid solved
    @brief      Fonction de résolution du sudoku
    """
    
    def aux(Lij):
        """
        @param      i   a line index of the sudoku
        @param      j   a column index of the sudoku 
        @return     a boolean
        @brief      Fonction récursive qui essaie de remplir la grille par une méthode "brute force"
        
        Renvoie 'true' si l'indice rentré dans la case est "valide" en regard des règles du sudoku, sinon 'false'
        """
        #nb_possible = ordre_backtracking(L,9)
        #print("Bienvenue dans",i,j)
        
        if (len(Lij)==1 and Lij(1,1)==9 and Lij(1,2)==0) :
            #print("C'est bientôt fini")
            #Le sudoku a été résolu avec succès
            return(True)
            
        # elif L[i][j]!=0:
        #     #La case est déjà remplie
        #     #print("La case est déjà remplie !!")
        #     next = case_suivante(L, nb_possible,i,j,9)
        #     return(aux(next[0],next[1]))
        
        #Sinon, on essaie de la remplir
        
        for k,l in range(0,9):
            liste_conflit = chiffres_conflit(L, k, l)
            
            if len(liste_conflit) ==9 :
                L[k][l] = 0 
                #print("C'est faux !")
                return(False)
        
            for digit in range(1,10):
                if not (digit in liste_conflit):
                    L[k][l] = digit
                    
        nb_possible = ordre_backtracking(L,9)
        print(nb_possible)
        # print()
        afficher(L)
        # print()
        next = case_suivante(L, nb_possible,i,j,9)
        # print(next)
                
        if aux(next)==True:
            print("Fin")
            return(True)
        #La suite s'exécute dans le cas où aucun des digits essayé n'a permis la résolution du sudoku dans son intégralité
        
    #Corps de solution_sudoku : appel à la fonction récursive avec la première case du sudoku
    nb_possible = ordre_backtracking(L,9)
    #print(nb_possible)
    next = case_suivante(L, nb_possible,0,0,9)
    #print(next)
    aux(next)
    return(L)

def afficher(L):
    """
    @param      L   a sudoku grid
    @brief      Affiche une grille de sudoku
    """
    
    for i in range(0,9):
        print(L[i])
        
init = time.clock()
print(afficher(solution_sudoku(L3)))
fin = time.clock()
print((fin-init))
"""
"""        
#print(ordre_backtracking(L4, 9))