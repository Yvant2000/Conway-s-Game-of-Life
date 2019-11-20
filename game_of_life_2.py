"""Chargement du programme"""
import pygame, os              #importations de modules
pygame.init()

screenSize = 1080,720           #Ouverture de la fenêtre
window = pygame.display.set_mode (screenSize)
screen = pygame.Surface (screenSize)
pygame.display.set_caption('Game of Life')
pygame.display.flip ()

if os.path.isfile('Game_of_life.txt') == False :      #Creation du fichier edition de la vie.
    f = open("Game_of_life.txt", "w")
    f.write ("#draw before this line your game of life")
    f.close()
    
squareSize = 5  #Définition de la taille des carrés
delay = 0       #Définition du temps d'attente entre chaques générations

xobject = 0     #Définition des variables et listes utiles au code
yobject = 0
livesList = []
bornList = []
almostDeadList = []
workOnList = []

with open('Game_of_life.txt', "r") as fichier :       #Ouverture du fichier edition de la vie.
    a = 1
    for letter in fichier.read() : #Interprétation du fichier pour affichage à l'écran.

        if letter == '#' :  #La lecture s'arrête si il lit "#".
            break

        if letter == '\n' : #Passage à la ligne du dessous.
            xobject = 0
            yobject += squareSize
            a = 0

        else :              #Si le character n'est pas un espace, il devient une cellule vivante.
            if not letter == ' ' : livesList.append (str(xobject) + "," + str(yobject))
            xobject += squareSize

"""Fonctions"""
def get_neighbour (home) :  #optention des coordonnées des "voisins".
    neighbourList = []
    
    coordones = home.split (",") #Toutes les cellules aux coordonnées relatives à la cellule "home" sont stockés dans une liste
    
    neighbourList.append (str(int(coordones[0])-squareSize) + "," + str(int(coordones[1])-squareSize)) #up left
    neighbourList.append (str(int(coordones[0])) + "," + str(int(coordones[1])-squareSize))            #up middle
    neighbourList.append (str(int(coordones[0])+squareSize) + "," + str(int(coordones[1])-squareSize)) #up right

    neighbourList.append (str(int(coordones[0])-squareSize) + "," + str(int(coordones[1])))            #middle left
    neighbourList.append (str(int(coordones[0])+squareSize) + "," + str(int(coordones[1])))            #middle right

    neighbourList.append (str(int(coordones[0])-squareSize) + "," + str(int(coordones[1])+squareSize)) #down left
    neighbourList.append (str(int(coordones[0])) + "," + str(int(coordones[1])+squareSize))            #down middle
    neighbourList.append (str(int(coordones[0])+squareSize) + "," + str(int(coordones[1])+squareSize)) #down right

    return neighbourList

def count_neighbour (neighbour) : #comptage des "voisins" en vie.
    global livesList
    a = 0
    for element in neighbour :
        if element in livesList : a+=1
    return a      #Le contenu de la fonction est le résultat du comptage.

def expend_workOnList (middle) : #On agrandi la liste des cellules sur lesquelles on travailles avec les cellules adjacentes.
    global workOnList, squareSize

    nList = get_neighbour (middle)
    
    for element in nList :      
        if not element in workOnList : workOnList[element] = count_neighbour (get_neighbour(element)) #Toutes les cellules voisines à une cellules vivante (element) est ajoutée aux cellules de travail.
    if not middle in workOnList : workOnList[middle] = count_neighbour (get_neighbour(middle))        #Les cellules vivantes (middle) aussi sont ajoutés aux cellules de travail.
    
"""Main_Loop"""
running = True
while running :     

    pygame.draw.rect(screen,(0,0,0),(0, 0, screenSize[0], screenSize[1])) #On nettoie l'écran.

    for square in livesList :       #Affichage des zone vivantes.
        coordones = square.split (",")
        if 0 < int(coordones[0]) < screenSize[0] and 0 < int(coordones[1]) < screenSize[1] : pygame.draw.rect(screen,(255,255,255),(int(coordones[0]), int(coordones[1]), squareSize, squareSize))

    workOnList = {}              #Remise a zéro des listes et dictionnaires temporaires.
    bornList = []
    almostDeadList = []

    for square in livesList :    #Définition de notre espace de travail.
        expend_workOnList (square)

    for square in workOnList :    #Application des règles du "Jeu de la vie".
        if workOnList[square] == 3 and not str(square) in livesList : bornList.append (str(square))  #Une cellules morte avec 3 voisins vivants nait.
        if workOnList[square] < 2 and str(square) in livesList : almostDeadList.append (str(square)) #Une cellule à l'écart meure.
        if workOnList[square] > 3 and str(square) in livesList : almostDeadList.append (str(square)) #Une cellule étouffée meure aussi.

    for square in almostDeadList  : #Cellules qui meurent
        livesList.remove (square)
    
    for square in bornList :        #Cellules qui naissent
        if not square in livesList : livesList.append (square)

    window.blit (screen,(0,0))
    pygame.display.update () #On rafraichi l'écran
    pygame.time.delay (delay)

    for event in pygame.event.get() : #Evenement de fermeture du programme.
        if event.type == pygame.QUIT :
            running = False
            
pygame.quit () #Fermeture du programme
