
# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe InterfacePartie. L'interface hérite de la classe d'objet Tk qui contient la 
fenêtre principale dans laquelle se déroule notre partie de Démineur.

Auteurs: Pascal Germain, Kevin Jobin, Bruce Bouchard, François Dufour
"""

# Importation des modules
from tkinter import *
from tkinter import messagebox, filedialog
from tableau import Tableau
from bouton_case import BoutonCase
import pygame

# Classe de l'interface
class InterfacePartie(Tk):
    """
    Classe dérivée de Tk qui instancie des objets de type InterfacePartie,
    qui contient la fenêtre principale du jeu.

    Inheritance:
        Tk (class)

    Attributes:

        # Fenêtre de jeu de l'interface
       self.title(str): Titre de la fenêtre de jeu. Par défaut: "Démineur"
       self.resizable(width, height): Redimensionnage de la fenêtre. Par défaut: (width=0, height=0)
       self.geometry("width x height"): Dimensions fixes de la fenêtre. Par défaut: (width=400px , height=400px)

        # Icône de l'interface
       self.iconphoto(Bool, image): Contient la photo de l'icône de l'application.

        # Chronomètre
       self.chrono (int): Nombre (en secondes) de temps de jeu d'une partie.
       self.label_chrono (Label): Étiquette qui contient le chronomèetre.

        # Compteur de tour
       self.compteur (int): Nombre de tours joués depuis le début de la partie.
       self.bouton_compteur (Button): Bouton qui contient le nombre de tour joués.

        # Score du joueur
       self.score (int): Score du joueur de la partie précédente. Par défaut, le score est initialisé à 0.
       self.score_label (Label): Étiquette qui contient le score de la partie précédente.

        # Tableau du jeu
       self.cadre (Frame): Cadre qui contient toutes les cases du jeu.
       self.tableau_mines (Tableau): Instance de la classe Tableau, c'est lui qui contient la logique du
                                     jeu de démineur. (voir docstring Tableau() )

       self.dictionnaire_boutons (Dict): Un dictionnaire qui contient les cases (qui sont instances de
                                         la classe BoutonCase). Chaque clé correspond aux coordonnées (x,y)
                                         de la case et est associée à une case (objet BoutonCase).

                                         Ex: { (1,1) : <objet BoutonCase> , ... (x,y) : <objet BoutonCase> }

    """

    def __init__(self):
        """
        Initialisation (constructeur) de l'objet InterfacePartie(Tk) avec des valeurs par défaut (aucun argument).
        """
        # On appele le constructeur de la classe mère Tk
        super().__init__()

        # Nom de la fenêtre.
        self.title("Démineur")

        # On empêche la redimension de la fenêtre principale
        self.geometry("400x400")
        self.resizable(0, 0)

        # Icone de l'application
        icon_top = PhotoImage(file="png/smile.png")
        self.iconphoto(True, icon_top)

        # Musique du jeu (fonctions du module pygame)
        pygame.mixer.init()
        pygame.mixer.music.load("super_lalonde.mp3")
        pygame.mixer.music.play(-1)

        # Cadre qui contient les boutons principaux du menu de la partie
        bouton_frame = Frame(self)
        bouton_frame.pack(padx=20, pady=20)

        # Bouton pour débuter une partie
        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.pack(side=LEFT)

        # Bouton pour afficher les instructions
        bouton_instructions = Button(bouton_frame, text="Instructions", command=self.instructions)
        bouton_instructions.pack(side=LEFT)

        # Bouton pour sauvegarder la partie encours
        bouton_sauvegarde = Button(bouton_frame, text="Sauvegarder", command=self.sauvegarde)
        bouton_sauvegarde.pack(side=LEFT)

        # Bouton pour ouvrir une partie préalablement sauvegardée
        bouton_chargement = Button(bouton_frame, text="Ouvrir", command=self.ouvrir)
        bouton_chargement.pack(side=LEFT)

        # Bouton pour quitter la partie en cours
        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter)
        bouton_quitter.pack(side=LEFT)

        # Cadre qui contient les boutons du compteur de tour et du chrono
        frame_compteurs = Frame(self)
        frame_compteurs.pack()

        # Chronomètre qui garde le temps
        self.chrono = 0

        # On part le chronomètre après une seconde
        self.after(1000, self.incremente)

        # Label (étiquette) du Chrono
        self.label_chrono = Button(frame_compteurs, text="Temps: " + str(self.chrono) + " secs", state='disabled')
        self.label_chrono.pack(side=LEFT)

        # Compteur de tour
        self.compteur = 0

        # Bouton du compteur de tour
        self.bouton_compteur = Button(frame_compteurs, text="Tour: " + str(self.compteur), state='disabled')
        self.bouton_compteur.pack(side=LEFT)

        # Initialisation du score de la partie
        self.score = 0

        # Étiquette du score
        self.score_label = Label(self, text='Score: ' + str(self.score))
        self.score_label.pack(side=BOTTOM, padx=10, pady=10)

        # Cadre qui contient les cases du jeu
        self.cadre = Frame(self, padx=20, pady=10)
        self.cadre.pack()

        # Dictionnaire dans lequel on retrouve toutes les cases du jeu
        self.dictionnaire_boutons = {}

        # Initialisation du tableau qui contient l'information des cases
        self.tableau_mines = Tableau()

        # pour chaque rangée de 0 à (nb. de rangée - 1)
        for i in range(self.tableau_mines.dimension_rangee):

            # pour chaque colonne de 0 à (nb. de colonne - 1)
            for j in range(self.tableau_mines.dimension_colonne):

                # On va placer une case qui sera une instance de BoutonCase (widget bouton)
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)

                # On 'bind' le clic gauche de la souris à la fonction qui dévoile la case
                bouton.bind('<Button-1>', self.devoiler_case)

                # On 'bind' le clic droit de la souris à la fonction qui met ou enlève un drapeau
                bouton.bind('<Button-2>', self.mettre_drapeau)
                bouton.bind('<Button-3>', self.mettre_drapeau)

                # On place la case/bouton dans le dictionnaire de bouton
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton

    def nouvelle_partie(self):
        """
        Méthode qui permet de lancer une nouvelle partie, en demandant d'abord à l'utilisateur de choisir
        les dimensions du jeu et le nombre de mines via une fenêtre secondaire.

        command: le clic du bouton_nouvelle_partie (Button) déclenche la méthode
        """

        # On initialise le compteur de tour à 0
        self.compteur = 0
        self.bouton_compteur['text'] = 'Tour: ' + str(self.compteur)
        self.bouton_compteur.pack(side=TOP)

        # On ouvre une fenêtre secondaire d'options de jeu
        self.fenetre_options = Toplevel(self)
        self.fenetre_options.title("Options de Jeu")
        self.fenetre_options.geometry("460x200")
        self.fenetre_options.resizable(0, 0)

        # Étiquette du choix des dimensions
        Label(self.fenetre_options, padx=10, pady=10,
              text="Choix des dimensions de la partie").grid()

        # Cadre contenant les sélections des dimensions du tableau et le nombre de mines
        cadre_selection = Frame(self.fenetre_options)
        cadre_selection.grid()

        # Déclaration des variables et leur valeurs par défaut
        rangee_var = IntVar(cadre_selection, value='5')
        colonne_var = IntVar(cadre_selection, value='5')
        mines_var = IntVar(cadre_selection, value='5')

        # Étiquette du choix du nombre de rangées
        label_rangee = Label(cadre_selection, padx=20, text=" Entrez le nombre de rangée: ")
        label_rangee.grid(row=1, column=0)
        entry_rangee = Entry(cadre_selection, bd=5, textvariable=rangee_var)
        entry_rangee.grid(row=1, column=1)

        # Étiquette du choix du nombre de colonnes
        label_colonne = Label(cadre_selection, padx=22, text="  Entrez le nombre de colonne: ")
        label_colonne.grid(row=2, column=0)
        entry_colonne = Entry(cadre_selection, bd=5, textvariable=colonne_var)
        entry_colonne.grid(row=2, column=1)

        # Étiquette du choix du nombre de mines
        label_mines = Label(cadre_selection, padx=22, text="Entrez le nombre de mines:  ")
        label_mines.grid(row=3, column=0)
        entry_mines = Entry(cadre_selection, bd=5, textvariable=mines_var)
        entry_mines.grid(row=3, column=1)

        # Cadre qui contient le bouton qui permet de commencer la partie
        cadre_commencer_partie = Frame(cadre_selection, padx=20, pady=20)
        cadre_commencer_partie.grid(row=4, column=1, sticky=NSEW)

        # Bouton qui permet de confirmer le choix des options et de commencer la partie
        bouton_commencer_partie = Button(cadre_commencer_partie, text='Commencer!',
                                         command=lambda: self.valider_dimensions(entry_rangee.get(),
                                                                                 entry_colonne.get(),
                                                                                 entry_mines.get()))
        bouton_commencer_partie.grid()

    def quitter(self):
        """
        Méthode qui ouvre une fenêtre permettant à l'utilisateur de quitter le programme (jeu). Il
        demande d'abord à l'utilisateur de confirmer son choix.

        command: le bouton_quitter (Button) contenu dans la fenêtre principale
        """
        # Création d'une fenêtre secondaire
        self.fenetre_quitter = Toplevel(self)
        self.fenetre_quitter.title("Quitter le jeu?")
        self.fenetre_quitter.resizable(0, 0)

        # Étiquette qui demande de confirmer le jeu
        label_quitter = Label(self.fenetre_quitter, padx=22, text="Voulez-vous vraiment quitter le jeu?  ")
        label_quitter.pack(side=TOP)

        # Cadre qui contient les boutons oui ou non
        bouton_frame = Frame(self.fenetre_quitter)
        bouton_frame.pack(side=TOP, padx=20, pady=20)

        # Bouton oui
        bouton_oui = Button(bouton_frame, text="Oui", padx=10, pady=10, command=self.quit)
        bouton_oui.pack(side=LEFT)

        # Bouton non
        bouton_non = Button(bouton_frame, text="Non", padx=10, pady=10, command=self.fenetre_quitter.destroy)
        bouton_non.pack(side=LEFT)

    def valider_dimensions(self, rangee, colonne, mines):
        """
        Fonction qui valide les coordonnées entrées par l'utilisateur et affiche un message d'erreur si ce
        ne sont pas des choix valides. Sinon, les entrées sont valides et on appele la fonction qui débute
        la partie.

        Args:
            rangee  (str): Entrée du nb de rangées choisies par le joueur (par défaut, 5)
            colonne (str): Entrée du nb de colonnes choisies par le joueur (par défaut, 5)
            mines   (str): Entrée du nombre de mines choisies par le joueur (par défaut, 5)

        """

        # Message d'erreur si les entrées sont invalides
        message_erreur = """S'il vous plait, entrez des dimensions valides de jeu:\n
        - Le nombre de rangée/colonne entre 3 et 20\n
        - Le nombre de mines ne doit pas être nul ou excédé le nombre de cases"""

        # Bloc de gestion de l'exception
        try:

            # On convertit les choix en nombre, si l'utilisateur a entré des chiffres. Sinon, on demander de recommencer.
            rangee, colonne, mines = int(rangee), int(colonne), int(mines)

            # On vérifie que les choix soient entre 3 et 20 et que le nombre de mines ne dépasse pas le nombre de cases.

            if rangee >= 20 or colonne >= 20 or (mines > rangee * colonne) or rangee < 3 or colonne < 3 or mines < 1:

                # si c'est le cas, les entrées ne sont pas valide et on doit recommencer
                messagebox.showerror("Erreur de dimensions", message_erreur)

                # On ferme l'ancienne fenêtre d'options de nouvelle partie
                self.fenetre_options.destroy()
                self.fenetre_options.update()

                # On en ouvre une nouvelle
                self.nouvelle_partie()

            else:

                # On ferme l'ancienne fenêtre d'options de nouvelle partie
                self.fenetre_options.destroy()
                self.fenetre_options.update()

                # Comme les entrées sont valides, on peut commencer la partie
                self.commencer_partie(rangee, colonne, mines)

        except:

            # Une exception s'est produit, on demande à l'utilisateur de recommencer
            messagebox.showerror("Erreur de dimensions", message_erreur)

            # On ferme l'ancienne fenêtre d'options de nouvelle partie
            self.fenetre_options.destroy()
            self.fenetre_options.update()

            # On en ouvre une nouvelle
            self.nouvelle_partie()

    def commencer_partie(self, rangee, colonne, mines):
        """
        Fonction qui débute la partie et affiche toutes les cases dans la fenêtre principale.

        Args:
            rangee  (int): Nombre de rangées choisies par le joueur (par défaut, 5)
            colonne (int): Nombre de colonnes choisies par le joueur (par défaut, 5)
            mines   (int): Nombre de mines choisies par le joueur (par défaut, 5)

        """

        # On ajuste la grosseur de la fenêtre en fonction du nombre de case
        grandeur_colonne = int(colonne) * 80
        grandeur_rangee = int(rangee) * 80
        grandeur = "{}x{}".format(grandeur_rangee, grandeur_colonne)
        self.geometry(grandeur)

        # On efface l'ancienne partie, puis on commencer la nouvelle
        if hasattr(self, 'tableau_mines'):
            for i in range(self.tableau_mines.dimension_rangee):
                for j in range(self.tableau_mines.dimension_colonne):
                    self.dictionnaire_boutons[(i + 1, j + 1)].grid_forget()
            del self.dictionnaire_boutons
            del self.tableau_mines
            self.cadre.grid_forget()

        # Initialisation du tableau de mines du jeu et du dictonnaire_boutons
        self.tableau_mines = Tableau(int(rangee), int(colonne), int(mines))
        self.dictionnaire_boutons = {}

        # pour chaque rangée de 0 à (nb. de rangée - 1)
        for i in range(self.tableau_mines.dimension_rangee):
            # pour chaque colonne de 0 à (nb. de colonne - 1)
            for j in range(self.tableau_mines.dimension_colonne):
                # On va placer une case qui sera un widget bouton
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton.bind('<Button-2>', self.mettre_drapeau)
                bouton.bind('<Button-3>', self.mettre_drapeau)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton

        # Si le chronomètre n'est pas déjà à 0, on le redémarre
        if self.chrono != 0:
            self.chrono = 0

    def retablir_sauvegarde(self, contenu_partie):

        """
        Méthode qui reçoit une sauvegarde de partie, quitte la partie en cours et charge la partie
        sauvegardée dans la fenêtre principale du jeu.

        Args:
                contenu_partie (dict): Un dictionnaire qui contient une sauvegarde de
                                      la partie.

        """

        # On rétablit les valeurs du compteur de tour et du chronomètre
        self.chrono, self.compteur = contenu_partie['chrono'],\
                                     contenu_partie['compteur']
        self.bouton_compteur['text'] = 'Tour: ' + str(self.compteur)
        self.bouton_compteur.pack(side=LEFT)

        # On convertit les valeurs des options de jeu en nombre (int)
        rangee, colonne, nombre_mines = int(contenu_partie['dimension_rangee']),\
                                        int(contenu_partie['dimension_colonne']),\
                                        int(contenu_partie['nombre_mines'])

        # On reconvertit le dictionnaire de case (str) en objet Dict
        dictionnaire_info_case = dict(contenu_partie['dictionnaire'])

        # On ajuste la grosseur de la fenêtre en fonction du nombre de case
        grandeur_colonne = int(colonne) * 80
        grandeur_rangee = int(rangee) * 80
        grandeur = "{}x{}".format(grandeur_rangee, grandeur_colonne)
        self.geometry(grandeur)

        # On efface l'ancienne partie, puis on commencer la nouvelle
        if hasattr(self, 'tableau_mines'):
            for i in range(self.tableau_mines.dimension_rangee):
                for j in range(self.tableau_mines.dimension_colonne):
                    self.dictionnaire_boutons[(i + 1, j + 1)].grid_forget()
            del self.dictionnaire_boutons
            del self.tableau_mines
            self.cadre.grid_forget()

        # Initialisation du tableau de mines du jeu et du dictonnaire_boutons
        self.tableau_mines = Tableau(rangee, colonne, nombre_mines)

        # On rétablit l'état de chacun des cases du jeu
        for case in dictionnaire_info_case:

            # On va chercher dans le tableau l'objet case correspondante aux coordonnées données par le dictionnaire
            objet_case = self.tableau_mines.dictionnaire_cases[case]

            # True si c'est une mine, False sinon
            objet_case.est_minee = dictionnaire_info_case[case][0]

            # True si la case est dévoilée, False sinon
            objet_case.est_devoilee = dictionnaire_info_case[case][1]

            # On rétablit la valeur du nombre de mines voisines
            objet_case.nombre_mines_voisines = dictionnaire_info_case[case][2]

        # On réinitialise le dictionnaire de bouton pour le remplir avec les cases sauvegardées
        self.dictionnaire_boutons = {}

        # pour chaque rangée de 0 à (nb. de rangée - 1)
        for i in range(self.tableau_mines.dimension_rangee):
            # pour chaque colonne de 0 à (nb. de colonne - 1)
            for j in range(self.tableau_mines.dimension_colonne):
                # On va placer une case qui sera un widget bouton
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<Button-1>', self.devoiler_case)
                bouton.bind('<Button-2>', self.mettre_drapeau)
                bouton.bind('<Button-3>', self.mettre_drapeau)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton

        # On dévoile chacun des cases qui étaient préalablement dévoilées
        for element in self.dictionnaire_boutons:

            bouton_a_devoiler = self.dictionnaire_boutons[element]
            case_a_verifie = self.tableau_mines.dictionnaire_cases[
                bouton_a_devoiler.rangee_x, bouton_a_devoiler.colonne_y]

            if case_a_verifie.est_devoilee:

                bouton_a_devoiler['text'] = str(case_a_verifie.nombre_mines_voisines)

                if case_a_verifie.nombre_mines_voisines == 0:
                    bouton_a_devoiler['text'] = '0'
                    bouton_a_devoiler['state'] = 'disabled'

                elif case_a_verifie.nombre_mines_voisines == 1:
                    bouton_a_devoiler['state'] = 'disabled'
                    bouton_a_devoiler['disabledforeground'] = 'blue'

                elif case_a_verifie.nombre_mines_voisines == 2:
                    bouton_a_devoiler['state'] = 'disabled'
                    bouton_a_devoiler['disabledforeground'] = 'green'

                elif case_a_verifie.nombre_mines_voisines == 3:
                    bouton_a_devoiler['state'] = 'disabled'
                    bouton_a_devoiler['disabledforeground'] = 'red'

                else:
                    bouton_a_devoiler['state'] = 'disabled'
                    bouton_a_devoiler['disabledforeground'] = '#0C3B87'

    def sauvegarde(self):
        """
        Méthode qui ouvre une fenêtre permettant à l'utilisateur de sauvegarder sa partie en cours. Il
        demande à l'utilsateur de choisir un nom et un emplacement pour le fichier et l'enregistre en
        fichier texte (.txt)

        command: le bouton_sauvegarde (Button) contenu dans la fenêtre principale
        """

        # Dictionnaire qui va contenir la sauvegarde des éléments de l'interface
        dictionnaire_partie = {}

        # Dictionnaire qui va contenir la sauvegarde de l'état des cases
        dictionnaire_info_case = {}

        # On sauvegarde chacune des cases et leur état et on l'associe a une coordonnée du tableau
        for case in self.tableau_mines.dictionnaire_cases:

            # Attributs de l'objet Case
            est_minee = self.tableau_mines.dictionnaire_cases[case].est_minee
            est_devoilee = self.tableau_mines.dictionnaire_cases[case].est_devoilee
            nombre_mines_voisines = self.tableau_mines.dictionnaire_cases[case].nombre_mines_voisines

            # On ajoute l'élément au dictionnaire { ... (x,y) : [Bool, Bool, Int], ... }
            dictionnaire_info_case[case] = [est_minee, est_devoilee, nombre_mines_voisines]

        # Sauvegarde du Tableau
        dictionnaire_partie['dimension_colonne'] = self.tableau_mines.dimension_colonne
        dictionnaire_partie['dimension_rangee'] = self.tableau_mines.dimension_rangee
        dictionnaire_partie['nombre_mines'] = self.tableau_mines.nombre_mines
        dictionnaire_partie['dictionnaire'] = dictionnaire_info_case

        # Sauvegarde du temps
        dictionnaire_partie['compteur'] = self.compteur
        dictionnaire_partie['chrono'] = self.chrono

        # Fenêtre de sauvegarde
        fenetre_sauvegarde = filedialog.asksaveasfile(mode="w")

        # On sauvegarde la partie sous forme de dictionnaire dans un fichier .txt
        try:
            fenetre_sauvegarde.write(str(dictionnaire_partie))
            fenetre_sauvegarde.close()

        # Gestion de l'exception si l'utilisateur cancel la sauvegarde
        except:

            return

    def ouvrir(self):
        """
        Méthode qui ouvre une fenêtre permettant à l'utilisateur de charger une partie sauvegardée. Il
        demande à l'utilsateur de choisir un nom et un emplacement de fichier et convertit le contenu en
        un dictionnaire de type string.

        command: le bouton_chargement (Button) contenu dans la fenêtre principale
        """


        # On se sert de filedialog pour ouvrir une fenêtre de sauvegarde de fichier .txt
        fenetre_sauvegarde = filedialog.askopenfile(mode="r")

        # Gestion de l'exception d'ouverture de fichier

        try:
            # On charge le contenu du fichier dans notre variable de sauvegarde
            contenu_partie = fenetre_sauvegarde.read()
            fenetre_sauvegarde.close()

            # On convertit le contenu de la partie (de type string) en dictionnaire
            contenu_partie = eval(contenu_partie)

            # On appelle la fonction qui charge la partie sauvegardée dans la fenêtre principale
            self.retablir_sauvegarde(contenu_partie)

        except:

            return

    def instructions(self):
        """
        Méthode qui ouvre une fenêtre affichant les instructions du jeu.

        command: le bouton_instructions (Button) contenu dans la fenêtre principale
        """

        # On ouvre une fenêtre secondaire qui contient les instructions
        self.fenetre_instructions = Toplevel(self)
        self.fenetre_instructions.title("Instructions du Jeu")
        self.fenetre_instructions.geometry("680x500")
        self.fenetre_instructions.resizable(0, 0)

        # Texte contenant les instructions du jeu
        instructions = """
    Le jeu se joue avec un tableau de cases dont le contenu est caché. Ces cases contiennent soit :

    • Une mine

    • Une case vide

    • Un nombre qui indique combien de mines la case a dans son voisinage 
      (les huit cases sur son pourtour)
    \n\n\
    Les mines sont placées aléatoirement dans le tableau. Les règles du jeu sont les suivantes :

    1. Si le joueur choisit une case où une mine est cachée, la mine explose! La partie est terminée.

    2. Si le joueur choisit une case avec un nombre caché, la case est dévoilée et le nombre devient visible.

    3. Si le joueur choisit une case vide (donc qui n’a ni mine ni nombre caché), il y a un effet en cascade
    qui fait le dévoilement de toutes les cases vides dans le voisinage jusqu’à ce que la limite du tableau 
    soit atteinte ou qu’une case avec un numéro caché soit atteinte. L’objectif du jeu est d’identifier, par 
    la logique, toutes les cases contenant des mines, sans en déclencher aucune.\n\n"""

        # Étiquette qui contient le titre
        Label(self.fenetre_instructions, padx=10, pady=10,
                text="Instructions de la partie").grid(row=0, column=0)

        # Étiquette qui contient le message
        Label(self.fenetre_instructions, padx=10, pady=10, text=instructions,
              anchor="e", justify=LEFT).grid(row=1, column=0)

    def mettre_drapeau(self, event):
        """
        Méthode qui affiche une image de drapeau sur une case lorsqu'un clique droit est exécuté sur
        le bouton correspondant de la case.

        Args:
             event (object): Un clique gauche de souris (<'Button-2'>) sur un bouton d'une case de jeu.

        command: le bouton (BoutonCase) contenu dans le cadre du jeu
        """

        # Widget associé à l'évènement (dans notre cas, un boutoncase)
        bouton = event.widget

        # Fichier contenant l'image du drapeau
        photo_drapeau = PhotoImage(file="png/flag_icon.gif").subsample(1, 1)

        # S'il n'y a pas d'image sur la case lorsqu'on clique droit, on l'ajoute
        if 'pyimage' not in bouton['image']:
            bouton['image'] = photo_drapeau
            bouton['compound'] = 'center'
            bouton.image = photo_drapeau

        # Sinon, on l'enlève
        else:
            bouton['image'] = ''

    def devoiler_case(self, event):
        """
        Méthode qui dévoile le contenu de la case lorsque le joueur clique sur un bouton du jeu.
        Si la case est une mine, on affiche la solution ainsi qu'un message de défaite. En cas de victoire,
        on affiche aussi la solution ainsi qu'un message de victoire.

        Args:
           event (object): Un clique droit de souris (<'Button-1'>) sur un bouton d'une case de jeu.
        """

        # Widget associé à l'évènement (dans notre cas, un widget de type BoutonCase)
        bouton = event.widget

        # On trouve la case qui y est associée dans le tableau de l'interface
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)

        # On vérifie d'abord si la case n'est pas minée
        if not case.est_minee and not case.est_devoilee:

            # On va incrémenter le compteur de tour de 1
            self.compteur += 1
            self.bouton_compteur['text'] = 'Tour: ' + str(self.compteur)
            self.bouton_compteur.pack(side=TOP)

            # On va aller dévoiler la case voulue
            self.tableau_mines.devoiler_case(bouton.rangee_x, bouton.colonne_y)

            # Musique de dévoilement de case
            devoilement_sound = pygame.mixer.Sound("sword_blade.wav")
            devoilement_sound.play()

            # On vérifie si la partie est terminée (si le joueur a gagné)
            if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:

                # On affiche la solution et le message de victoire
                victoire = True
                self.afficher_solution(victoire)

            # On va dévoiler la case et ses voisins en effet cascade, s'il y a lieu

            for element in self.dictionnaire_boutons:

                bouton_a_devoiler = self.dictionnaire_boutons[element]
                case_a_verifie = self.tableau_mines.dictionnaire_cases[bouton_a_devoiler.rangee_x, bouton_a_devoiler.colonne_y]

                # On va aussi afficher le chiffre correspond au nombre de mines sur la case

                if case_a_verifie.est_devoilee:
                    bouton_a_devoiler['text'] = str(case_a_verifie.nombre_mines_voisines)

                    if case_a_verifie.nombre_mines_voisines == 0:
                        bouton_a_devoiler['text'] = '0'
                        bouton_a_devoiler['state'] = 'disabled'

                    elif case_a_verifie.nombre_mines_voisines == 1:
                        bouton_a_devoiler['state'] = 'disabled'
                        bouton_a_devoiler['disabledforeground'] = 'blue'

                    elif case_a_verifie.nombre_mines_voisines == 2:
                        bouton_a_devoiler['state'] = 'disabled'
                        bouton_a_devoiler['disabledforeground'] = 'green'

                    elif case_a_verifie.nombre_mines_voisines == 3:
                        bouton_a_devoiler['state'] = 'disabled'
                        bouton_a_devoiler['disabledforeground'] = 'red'

                    else:
                        bouton_a_devoiler['state'] = 'disabled'
                        bouton_a_devoiler['disabledforeground'] = '#0C3B87'

        # si c'est une mine, on finit le tour et on va dévoilé la mine et la solution
        elif case.est_minee:

            # on incrémente le compteur de tour quand même
            self.compteur += 1
            self.bouton_compteur['text'] = 'Tour: ' + str(self.compteur)
            self.bouton_compteur.pack(side=TOP)

            # On affiche l'image de la mine sur le bouton
            photo_mine = PhotoImage(file="png/mine.gif").subsample(1, 1)
            bouton['image'] = photo_mine
            bouton['compound'] = 'center'
            bouton.image = photo_mine

            # on affiche la solution et le message de défaite
            victoire = False
            self.afficher_solution(victoire)

    def afficher_solution(self, victoire):
        """
        Méthode qui dévoile toutes les cases lorsque le joueur clique sur une mine ou lorsqu'il ne reste
        plus de cases à dévoiler qui ne sont pas des mines. Alors on affiche un message de défaite ou un
        message de victoire tout dépendant.

        Args:
           victoire (Bool): True si le joueur remporte la partie, False sinon.
        """

        # On affiche la solution en dévoilant tous les boutons
        for element in self.dictionnaire_boutons:

            bouton = self.dictionnaire_boutons[element]
            case = self.tableau_mines.dictionnaire_cases[element]

            if case.est_minee:
                photo1 = PhotoImage(file="png/mine.gif")
                bouton['image'] = photo1
                bouton['compound'] = 'center'
                bouton.image = photo1

            else:

                bouton['text'] = str(case.nombre_mines_voisines)

                if case.nombre_mines_voisines == 0:
                    bouton['text'] = '0'
                    bouton['state'] = 'disabled'

                elif case.nombre_mines_voisines == 1:
                    bouton['state'] = 'disabled'
                    bouton['disabledforeground'] = 'blue'

                elif case.nombre_mines_voisines == 2:
                    bouton['state'] = 'disabled'
                    bouton['disabledforeground'] = 'green'

                elif case.nombre_mines_voisines == 3:
                    bouton['state'] = 'disabled'
                    bouton['disabledforeground'] = 'red'

                else:
                    bouton['state'] = 'disabled'
                    bouton['disabledforeground'] = '#0C3B87'

        # On affiche le message de victoire si la variable est True
        if victoire:
            victory_sound = pygame.mixer.Sound('victory-trumpets.wav')
            victory_sound.play()
            self.message_victoire = messagebox.showinfo(title='Victoire',
                                                           message='Félicitation, vous avez remporté la partie! :)')

            # On affiche le score qui est égal au temps écoulé depuis le début de la partie
            self.score = self.chrono
            self.score_label['text'] = 'Score précédent: ' + str(self.chrono)
            self.score_label.pack(side=BOTTOM, padx=10, pady=10)

        # Sinon, on affiche le message de défaite
        else:
            defeat_sound = pygame.mixer.Sound('explosion.wav')
            defeat_sound.play()
            self.message_defaite = messagebox.showwarning(title='Défaite',
                                                message='Oh non... vous avez touché une mine! Recommencez :(')
            # On met le score à 0 car on a perdu
            self.score = 0
            self.score_label['text'] = 'Score précédent: ' + str(self.score)
            self.score_label.pack(side=BOTTOM, padx=10, pady=10)

    def incremente(self):
        """
        Une méthode récursive qui incrémente le compteur à chaque seconde (1000ms) dès qu'une partie débute.
        """

        # On incrémente le chrono de 1
        self.chrono += 1

        # Étiquette qui affiche le chronomètre dans la fenêtre principale
        self.label_chrono['text'] = "Temps: " + str(self.chrono) + " secs"
        self.label_chrono.pack(side=LEFT)

        # On appelle la méthode after de manière récursive à toutes les secondes (1000ms)
        self.after(1000, self.incremente)
