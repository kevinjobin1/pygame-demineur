# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.

Auteurs: Bruce Bouchard, Kevin Jobin, François Dufour
"""

from case import Case
from random import randint
from sys import setrecursionlimit

# on change la limite de récursion pour pouvoir afficher un tableau de 39x39, par exemple
setrecursionlimit(10**6)

class Tableau():
    """
    Tableau du jeu de démineur, implémenté avec un dictionnaire de cases.
    
    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau complet
        dimension_colonne (int): Nombre de colonnes du tableau complet
        nombre_mines (int): Nombre de mines cachées dans le tableau complet

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y), 
                x étant le numéro de la rangée, y étant le numéro de la colonne.
            Les valeurs sont des objets de la classe Case.

             { (1,1) : case1 ,
              (1,2) : case2 ,
              ... }
    """
    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=3):
        """ Initialisation d'un objet tableau.
        
        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau (valeur par défaut: 5)
            nombre_cases (int): Nombre de cases total du tableau (valeur par défaut: 25)
            nombre_mines (int): Nombre de mines cachées dans le tableau (valeur par défaut: 5)
            dictionnaire_cases (dict): Dictionnaire contenant comme clés des coordonnées (x,y)
                                        associée à un object Case comme élément. (Vide par défaut)

        """ 

        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        # nombre de cases total du tableau (incluant les mines)
        self.nombre_cases = self.dimension_rangee * self.dimension_colonne

        # nombre de cases à dévoiler (en excluant les mines)
        self.nombre_cases_sans_mine_a_devoiler = self.nombre_cases - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """
        # la rangée est valide, c'est-à-dire à l'intérieur du tableau (entre 1 et le nombre de rangée)
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        # de même pour la colonne
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne

        if rangee_valide and colonne_valide:
            return True

        return False
    
    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne
        
        Args:
            rangee_x (int) : Numéro de la rangée de la cas
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les coordonnées ne sont pas valides)
        """
        # retourne None si les coordonnées ne sont pas valides
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None

        # sinon, les coordonnées sont bonnes et on retourne l'objet case relié
        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines de la case dont les coordonnées
            sont reçues en argument
        """

        # coordonnées des cases voisines relatives aux coordonnées données en argument
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0),  (1, 1))

        # liste contenant les coordonnées des cases voisines
        liste_coordonnees_cases_voisines = []

        # pour chaque tuple contenu dans voisinage, on calcule la case voisine associée
        for case in voisinage:

            # coordonnées de la case voisine en fonction des coordonnées données en argument
            case_voisine = ((rangee_x + case[0]), (colonne_y + case[1]))

            # si la case voisine existe dans le tableau, on l'ajoute à la liste
            if self.valider_coordonnees(case_voisine[0], case_voisine[1]):

                liste_coordonnees_cases_voisines.append(case_voisine)

        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau (cette étape est programmée pour vous).
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard
                (attention de ne pas choisir deux fois la même case!).
                - À chaque fois qu'on ajoute une mine dans une case, on obtient la liste de 
                  ses voisins (pour se faire, utilisez la méthode obtenir_voisins)
                - Pour chaque voisin, on appelle la méthode ajouter_une_mine_voisine de la case correspondante.
        """

        # On remplit les cases du tableau
        for rangee_x in range(1, self.dimension_rangee+1):
            for colonne_y in range(1, self.dimension_colonne+1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()

        compteur_mines = 0

        liste_coordonnes_mines = []

        while compteur_mines < self.nombre_mines:

                coordonnees_mine = (randint(1, self.dimension_rangee), randint(1, self.dimension_colonne))

                if coordonnees_mine not in liste_coordonnes_mines:

                    liste_coordonnes_mines.append(coordonnees_mine)
                    self.dictionnaire_cases[coordonnees_mine].ajouter_mine()
                    compteur_mines += 1

                    # on trouve toutes les cases voisines de la mine
                    liste_voisins = self.obtenir_voisins(coordonnees_mine[0], coordonnees_mine[1])

                    # On itère sur chaque case voisine
                    for voisin in liste_voisins:
                        # Pour chaque case près d'une mine ,on incrémente son nombre de 1
                        self.dictionnaire_cases[voisin].ajouter_une_mine_voisine()

    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):
        """
        Valide que les coordonnées reçues en argument sont celles d'une case que l'on peut dévoiler 
        (donc que les coordonnées sont valides et que la case correspondante n'a pas encore été dévoilée).
        
        Args:
            rangee_x  (int): Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns
            bool: True si la case à ces coordonnées (x, y) peut être dévoilée, False autrement (donc si la
                  case a déjà été dévoilée ou que les coordonnées ne dont pas valides).
        """

        # on valide si les coordonnées données sont dans le tableau
        coordonnees_valide = self.valider_coordonnees(rangee_x, colonne_y)

        if coordonnees_valide:
            # on vérifie si la case choisie n'a pas été dévoilée, on retourne True
            if self.dictionnaire_cases[(rangee_x, colonne_y)].est_devoilee == False:

                return True

        else:
            # sinon, on retourne false
            return False
        
    def afficher_solution(self):
        """
        Méthode qui affiche le tableau de la solution à l'écran. La solution montre les 
        mines pour les cases qui en contiennent et la valeur du nombre de mines voisines 
        pour les autres cases.
        
        Important: Vous n'avez pas à modifier cette méthode, mais vous pouvez vous
        en inspirer pour écrire la méthode afficher_tableau().
        """
        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |' 
                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y%10}' 
                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|' 
                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)  
                    if case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)
                
                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne) 
         
    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu des cases dévoilées 
        (mine ou nombre de mines voisines) ou un point pour les cases non dévoilées.
        """

        print() # Retour de ligne
        
        for rangee_x in range(0, self.dimension_rangee+1):
            
            # Affichage d'une ligne, caractère par caractère
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0: 
                    # Premiers caractères de l'en-tête (coin supérieur gauche)
                    car = '  |'

                elif rangee_x == 0:
                    # En-tête: numéro de la colonne 
                    # (si y > 10, on affiche seulement l'unité pour éviter les décalages)
                    car = f'{colonne_y%10}'

                elif colonne_y == 0:
                    # Début de ligne: numéro de la ligne sur deux caractères,
                    # suivi d'une ligne verticale.
                    car = f'{rangee_x:<2}|'

                else:
                    # Contenu d'une case
                    case_xy = self.obtenir_case(rangee_x, colonne_y)

                    if case_xy.est_devoilee:
                        if case_xy.est_minee:
                            car = 'M'
                        else:
                            car = str(case_xy.nombre_mines_voisines)
                    else:
                        car = '.'
                
                # Afficher le caractère suivit d'un espace (sans retour de ligne)
                print(car, end=" ")
            
            # À la fin de chaque ligne
            print() # Retour de ligne
            if rangee_x == 0: # Ligne horizontale de l'en-tête
                print('--+-' + '--'*self.dimension_colonne) 

    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler.
        
        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """

        # on vérifie s'il reste des cases à dévoiler (excluant les mines)
        if self.nombre_cases_sans_mine_a_devoiler > 0:
            return True

        # sinon, c'est qu'il ne reste que les mines, on retourne False
        return False

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument. Si la case ne
        contient pas de mine, on décrémente l'attribut qui représente le nombre de cases sans mine à dévoiler. 
        Aussi, si cette case n'est voisine d'aucune mine, on dévoile ses voisins. 
       
        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler
        """

        # on vérifie d'abord si la case n'est pas minée
        if not self.contient_mine(rangee_x, colonne_y):

            # on trouve ensuite les coordonnées de la case grâce aux arguments donnés
            coordonnees_case = (rangee_x, colonne_y)

            # on trouve l'objet Case associé aux coordonnées données
            case = self.dictionnaire_cases[coordonnees_case]

            # on dévoile la case et on décrémente l'attribut du nombre de cases sans mines à dévoiler
            case.est_devoilee = True
            self.nombre_cases_sans_mine_a_devoiler -= 1

            # si la case n'est voisine d'aucune mine (valeur de 0) on dévoile ses voisins
            if case.nombre_mines_voisines == 0:
                liste_voisins = self.obtenir_voisins(rangee_x, colonne_y)

                for voisin in liste_voisins:
                    case_voisine = self.dictionnaire_cases[voisin]

                # pour chaque case voisine qui n'a pas encore été dévoilée, on la dévoile
                    if not case_voisine.est_devoilee:

                        # effet cascade via la récursion
                        self.devoiler_case(voisin[0], voisin[1])

    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine
        
        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """

        # on trouve les coordonnées grâce aux arguments donnés (on suppose qu'ils sont valides)
        coordonnees_case = (rangee_x, colonne_y)

        # on trouve l'objet Case avec les coordonnées correspondantes
        case = self.dictionnaire_cases[coordonnees_case]

        # on vérifie si cette case est minée
        if case.est_minee:

            # si c'est le cas, on retourne True
            return True

        # sinon, on retourne False
        return False


#### Tests unitaires (à compléter) ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
        tableau_test.dimension_rangee - tableau_test.nombre_mines

def test_valider_coordonnees():

    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x+1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y+1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)
    
def test_obtenir_voisins():

    tableau_test = Tableau()
    assert (tableau_test.obtenir_voisins(1, 1)) == [(1, 2), (2, 1), (2, 2)]
    assert (tableau_test.obtenir_voisins(3, 3)) == [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]
    assert (tableau_test.obtenir_voisins(1, 3)) == [(1, 2), (1, 4), (2, 2), (2, 3), (2, 4)]
    
def test_valider_coordonnees_a_devoiler():

    tableau_test = Tableau()
    assert tableau_test.valider_coordonnees_a_devoiler(1, 1) == True
    assert tableau_test.valider_coordonnees_a_devoiler(5, 5) == True
    assert tableau_test.valider_coordonnees_a_devoiler(0, 0) == False
    assert tableau_test.valider_coordonnees_a_devoiler(6, 6) == False
    assert tableau_test.valider_coordonnees_a_devoiler(-1, -1) == False
    
def test_devoiler_case():

    tableau_test = Tableau()

    tableau_test.devoiler_case(1, 1)
    assert tableau_test.dictionnaire_cases[(1, 1)].est_devoilee == True

    tableau_test = Tableau()

    tableau_test.devoiler_case(3, 3)
    assert tableau_test.dictionnaire_cases[(3, 3)].est_devoilee == True

    tableau_test = Tableau()

    tableau_test.devoiler_case(4, 4)
    assert tableau_test.dictionnaire_cases[(4, 4)].est_devoilee == True

    
def test_case_contient_mine():

    tableau_test = Tableau()

    tableau_test.dictionnaire_cases[(1, 1)].est_minee = True
    assert tableau_test.contient_mine(1, 1) == True

    tableau_test = Tableau()

    tableau_test.dictionnaire_cases[(1, 1)].est_minee = False
    assert tableau_test.contient_mine(1, 1) == False

    tableau_test = Tableau()

    tableau_test.dictionnaire_cases[(3, 4)].est_minee = True
    assert tableau_test.contient_mine(3, 4) == True


if __name__ == '__main__':

    # Les cinq prochaines lignes de code sont là pour vous aider à tester votre
    # première tentative d'implémentation des méthodes initialiser_tableau et afficher_tableau.
    
    tableau_test = Tableau()
    print('\nTABLEAU:')
    tableau_test.afficher_tableau()
    print('\nSOLUTION:')
    tableau_test.afficher_solution()

    print('\nTests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_valider_coordonnees_a_devoiler()
    test_devoiler_case()
    test_case_contient_mine()
    print('Tests réussis!')
