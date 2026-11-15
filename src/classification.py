"""
Scoring du risque de resiliation pour la cohorte de fin d'engagement (phase 3).

Ce module attribue a chaque abonne de la cohorte mensuelle une probabilite de
resiliation. Il ne decide pas qui appeler : c'est le role de src/evaluation.py,
qui exploite ces probabilites pour construire l'ordre des appels (question 5)
et mesurer le rendement de l'elargissement de l'equipe (question 6).

HYPOTHESE SUR LA COHORTE - A LIRE AVANT TOUTE INTERPRETATION
-----------------------------------------------------------
La direction decrit 400 abonnes qui arrivent chaque mois en fin
d'engagement. Le fichier nettoye NE CONTIENT AUCUNE DATE de fin
d'engagement : il est donc impossible de reconstituer la vraie cohorte du
mois. On la SIMULE par le jeu de test de train_test_split avec
test_size=400, ce qui est une hypothese de travail et non une donnee.

Cette simulation suppose que la cohorte d'un mois donne est un echantillon
representatif de l'ensemble des abonnes. C'est defendable (rien n'indique
que les fins d'engagement se concentrent sur un profil particulier) mais
cela reste a verifier le jour ou une date d'engagement sera disponible. Si
les fins d'engagement etaient saisonnieres, ou concentrees sur les abonnes
entres en promotion, les resultats de la phase 3 seraient optimistes.

On utilise stratify=y pour que la cohorte simulee ait le meme taux de
resiliation que la population totale : sans cela, le tirage pourrait donner
une cohorte anormalement saine ou anormalement a risque, et toute la
rentabilite calculee en phase 3 dependrait de ce hasard.

JUSTIFICATION DU MODELE : REGRESSION LOGISTIQUE
----------------------------------------------
On choisit la regression logistique plutot qu'un arbre de decision ou une
foret aleatoire, pour trois raisons liees a l'usage reel :

1) On a besoin d'un CLASSEMENT, pas d'une decision binaire. La question
   n'est pas "cet abonne va-t-il resilier ?" mais "parmi 400 abonnes,
   lesquels sont les 80 plus a risque ?". Il faut donc une probabilite
   continue, qui se trie. Un arbre de decision range les abonnes dans un
   petit nombre de feuilles et donne la meme probabilite a tous les abonnes
   d'une meme feuille : impossible de departager 400 abonnes proprement, on
   obtiendrait des paquets d'ex aequo qu'il faudrait trancher au hasard.

2) La probabilite doit etre CALIBREE, c'est-a-dire utilisable comme un
   vrai pourcentage, parce qu'on la multiplie ensuite par un chiffre
   d'affaires pour calculer une valeur esperee (voir src/evaluation.py).
   La regression logistique optimise directement la vraisemblance, ce qui
   produit des probabilites proches des frequences observees. Une foret
   aleatoire, qui moyenne des votes d'arbres, a tendance a tasser ses
   probabilites vers le centre : le classement resterait correct mais les
   euros calcules dessus seraient faux.

3) Le modele doit etre EXPLICABLE au comite de direction. Chaque
   coefficient se lit comme un effet, et la phase 2 a deja montre lesquels
   pesent. Il faut pouvoir dire a un responsable de salle pourquoi tel
   abonne est dans la liste des 80. Une foret de centaines d'arbres ne se
   raconte pas.

Enfin, avec 797 lignes et 12 variables, un modele a forte variance comme une
foret aleatoire n'apporterait de toute facon pas grand-chose : le gain de
performance serait dans le bruit du decoupage.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Variables explicatives numeriques du score de risque
VARIABLES_NUMERIQUES = [
    "anciennete_mois",
    "prix_mensuel_eur",
    "distance_domicile_m",
    "visites_par_mois",
    "seances_coaching",
    "reclamations",
]

# Variables qualitatives, transformees en indicatrices
VARIABLES_QUALITATIVES = ["formule", "creneau_habituel"]

# Taille de la cohorte mensuelle de fin d'engagement (hypothese, cf. docstring)
TAILLE_COHORTE = 400

# Graine fixe : la liste des 80 abonnes a appeler doit etre reproductible,
# sinon deux executions designeraient deux listes differentes
GRAINE = 42


def construire_cible(abonnes):
    """Transforme a_resilie (oui/non) en cible binaire 1/0.

    1 = a resilie, pour que la probabilite predite se lise directement
    comme un risque de depart.
    """
    return (abonnes["a_resilie"] == "oui").astype(int)


def preparer_variables(abonnes):
    """Construit la matrice des variables explicatives.

    drop_first=True : une modalite sert de reference, sinon les indicatrices
    d'une meme variable sont colineaires entre elles.
    astype(float) : get_dummies produit des colonnes booleennes, que
    StandardScaler n'est pas cense recevoir. On convertit tout en float pour
    avoir une matrice homogene et eviter tout avertissement de version.
    """
    colonnes = VARIABLES_NUMERIQUES + VARIABLES_QUALITATIVES
    return pd.get_dummies(abonnes[colonnes], drop_first=True).astype(float)


def scorer_cohorte(abonnes):
    """Entraine le modele et score la cohorte simulee de fin d'engagement.

    Retourne (cohorte, auc, taux_resiliation_base) ou cohorte est le
    sous-ensemble des abonnes de test, enrichi des colonnes churn et
    probabilite_resiliation.
    """
    explicatives = preparer_variables(abonnes)
    cible = construire_cible(abonnes)

    # test_size=400 : le jeu de test EST la cohorte mensuelle simulee.
    # stratify=cible : meme taux de resiliation dans la cohorte que dans la
    # population totale (cf. docstring).
    entrainement_x, cohorte_x, entrainement_y, cohorte_y = train_test_split(
        explicatives, cible,
        test_size=TAILLE_COHORTE,
        random_state=GRAINE,
        stratify=cible,
    )

    # Le StandardScaler est ajuste UNIQUEMENT sur le jeu d'entrainement.
    # L'ajuster sur l'ensemble des donnees ferait fuiter dans l'entrainement
    # les moyennes et ecarts-types de la cohorte, donc une information que
    # l'on n'a pas le jour ou l'on score de vrais abonnes a venir. Le score
    # mesure ici serait alors meilleur que celui obtenu en situation reelle.
    echelle = StandardScaler()
    echelle.fit(entrainement_x)

    # max_iter=2000 : marge confortable pour la convergence de lbfgs
    modele = LogisticRegression(max_iter=2000)
    modele.fit(echelle.transform(entrainement_x), entrainement_y)

    # predict_proba renvoie deux colonnes (ne resilie pas, resilie) :
    # on garde la seconde, qui est le risque de depart
    probabilites = modele.predict_proba(echelle.transform(cohorte_x))[:, 1]

    # On revient aux lignes d'origine pour recuperer abonne_id, salle et prix,
    # dont evaluation.py a besoin et qui ne sont pas dans la matrice scalee
    cohorte = abonnes.loc[cohorte_x.index].copy()
    cohorte["churn"] = cohorte_y.values
    cohorte["probabilite_resiliation"] = probabilites

    auc = roc_auc_score(cohorte_y, probabilites)
    taux_base = cohorte_y.mean()

    return cohorte, auc, taux_base


def scorer_risque(abonnes):
    """Affiche la qualite du scoring et retourne la cohorte scoree."""
    cohorte, auc, taux_base = scorer_cohorte(abonnes)

    print("Abonnes disponibles        :", len(abonnes))
    print("Abonnes d'entrainement     :", len(abonnes) - len(cohorte))
    print("Cohorte de fin d'engagement :", len(cohorte), "(simulee, cf. docstring du module)")

    print("\n--- Qualite du scoring sur la cohorte ---")
    print("AUC sur la cohorte                  : {:.3f}".format(auc))
    print("Taux de resiliation de base          : {:.4f}".format(taux_base))
    print("Resiliants dans la cohorte           : {}".format(int(cohorte["churn"].sum())))
    print("\nLecture : une AUC de {:.3f} signifie que si l'on tire au hasard un".format(auc))
    print("abonne qui va resilier et un abonne qui va rester, le modele donne")
    print("un risque plus eleve au premier dans {:.0f} % des cas. C'est loin de".format(auc * 100))
    print("la perfection, mais tres au-dessus du hasard (0.500) : suffisant")
    print("pour classer une file d'appels, insuffisant pour decider seul.")

    print("\n--- Distribution du risque predit sur la cohorte ---")
    description = cohorte["probabilite_resiliation"].describe()
    print("minimum : {:.3f}   median : {:.3f}   maximum : {:.3f}".format(
        description["min"], description["50%"], description["max"]))
    print("Le risque s'etale largement : c'est ce qui rend un classement utile.")
    print("Si tous les abonnes avaient le meme risque, aucune priorisation")
    print("ne serait possible et l'equipe d'appel vaudrait un tirage au sort.")

    return cohorte
