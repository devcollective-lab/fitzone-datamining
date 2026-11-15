"""
Point d'entree de la phase 2 du projet FitZone.

La phase 1 (main.py) nettoie les donnees brutes et ecrit
data/processed/FitZone_abonnes_clean.csv. La phase 2 part de ce fichier et
repond aux quatre questions de la direction :

  Q1 : qu'est-ce qui distingue un abonne qui reste d'un abonne qui part ?
  Q2 : la distance domicile-salle explique-t-elle vraiment les departs ?
  Q3 : combien de fois par mois viendra un abonne qui signe demain ?
  Q4 : de quoi depend cette frequentation, et avec quelle marge d'erreur ?

Les deux premieres questions sont traitees dans src/analyse_resiliation.py
(tests statistiques et regression logistique), les deux suivantes dans
src/regression.py (regression lineaire multiple). On garde les deux etages
separes parce qu'ils n'ont pas la meme cible : la resiliation d'un cote, la
frequentation de l'autre.

Ce fichier ne fait aucun calcul lui-meme : il charge les donnees nettoyees
et appelle les deux modules. Les donnees ne sont pas remodifiees ici, la
phase 1 reste la seule etape de nettoyage.
"""

from src.analyse_resiliation import analyser_resiliation
from src.regression import modeliser_frequentation

import pandas as pd

CHEMIN_DONNEES_NETTOYEES = "data/processed/FitZone_abonnes_clean.csv"


def charger_donnees_nettoyees():
    """Charge le fichier produit par la phase 1."""
    abonnes = pd.read_csv(CHEMIN_DONNEES_NETTOYEES)
    print("Fichier charge :", CHEMIN_DONNEES_NETTOYEES)
    print("Dimensions :", abonnes.shape)
    return abonnes


def afficher_titre(texte):
    """Affiche un titre de section bien visible dans la sortie console."""
    print("\n" + "=" * 70)
    print(texte)
    print("=" * 70)


def main():
    afficher_titre("PHASE 2 - CHARGEMENT DES DONNEES NETTOYEES")
    abonnes = charger_donnees_nettoyees()

    afficher_titre("PARTIE A - FACTEURS DE RESILIATION (QUESTIONS 1 ET 2)")
    analyser_resiliation(abonnes)

    afficher_titre("PARTIE B - PREDICTION DE LA FREQUENTATION (QUESTIONS 3 ET 4)")
    modeliser_frequentation(abonnes)

    afficher_titre("PHASE 2 TERMINEE")
    print("Figures enregistrees dans outputs/figures/")


if __name__ == "__main__":
    main()
