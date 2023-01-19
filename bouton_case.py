# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe BoutonCase. Une case peut contenir une mine
et être dans différents états de dévoilement.

Auteur: Pascal Germain, Kevin Jobin, Francois Dufour, Bruce Bouchard
"""
# Importation des modules
from tkinter import Button

class BoutonCase(Button):
    """
    Classe dérivée de Button qui instancie des objets de type BoutonCase,
    qui contient une case du jeu.

    Inheritance:
        Button (class)

    Attributes:
        self.rangee_x = Coordonnée en x de la case
        self.colonne_y = Coordonnée en y de la case
    """
    def __init__(self, parent, rangee_x, colonne_y):
        """
        Constructeur de la classe BoutonCase.

        Args:
            parent (objet): widget/object Tkinter qui contient le BoutonCase
            rangee_x (int): Position en x de la case
            colonne_y (int): Position en y de la case

        Returns:
            BoutonCase (object):  Une instance de la classe BoutonCase
        """
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        # Constructeur de la classe mère Button
        super().__init__(parent, text=' ', padx=1, pady=3, height=2, width=3, relief='sunken')


