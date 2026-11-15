"""
Point d'entree de la phase 3 du projet FitZone.

La phase 1 (main.py) nettoie les donnees, la phase 2 (phase2.py) explique la
resiliation et predit la frequentation. La phase 3 passe de l'explication a
la DECISION : quels abonnes appeler, et jusqu'ou elargir l'equipe d'appel.

  Q5 : chaque mois, 400 abonnes arrivent en fin d'engagement et on ne peut en
       appeler que 80. Lesquels ?
  Q6 : si on double l'equipe d'appel le mois prochain, recupere-t-on deux
       fois plus de monde ?

Les deux questions sont traitees en deux etages separes :
  - src/classification.py attribue un risque de resiliation a chaque abonne
    de la cohorte. Il ne decide rien.
  - src/evaluation.py transforme ces risques en ordre d'appels, en euros et
    en gain marginal. Il ne modelise rien.

Cette separation est voulue : le jour ou le modele de scoring change, la
partie economique n'a pas a etre rouverte, et inversement, le jour ou la
direction conteste le cout d'un appel, le modele n'a pas a etre reentraine.

Les deux hypotheses structurantes de la phase 3 sont ecrites en tete des
modules concernes, et non ici : la cohorte simulee de 400 abonnes dans
src/classification.py, les trois hypotheses economiques dans
src/evaluation.py. Aucun chiffre en euros de cette phase ne doit etre cite
sans elles.

Ce fichier ne fait aucun calcul lui-meme : il charge les donnees nettoyees
et enchaine les deux modules.
"""

from src.classification import scorer_risque
from src.evaluation import evaluer_priorisation

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
    afficher_titre("PHASE 3 - CHARGEMENT DES DONNEES NETTOYEES")
    abonnes = charger_donnees_nettoyees()

    afficher_titre("ETAPE 1 - SCORING DU RISQUE DE RESILIATION")
    cohorte = scorer_risque(abonnes)

    afficher_titre("ETAPE 2 - PRIORISATION DES APPELS (QUESTIONS 5 ET 6)")
    evaluer_priorisation(cohorte)

    afficher_titre("PHASE 3 TERMINEE")
    print("Liste des appels : outputs/results/q5_top80_a_appeler.csv")
    print("Figures          : outputs/figures/")


if __name__ == "__main__":
    main()
