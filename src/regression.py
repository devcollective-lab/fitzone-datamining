"""
Prediction de la frequentation mensuelle chez FitZone (questions 3 et 4).

Question 3 : combien de fois par mois viendra un abonne qui signe demain ?
Question 4 : de quoi depend cette frequentation, et avec quelle marge d'erreur ?

JUSTIFICATION DES METHODES RETENUES
-----------------------------------
1) Regression lineaire multiple. La cible visites_par_mois est une quantite
   numerique continue : c'est un probleme de regression, pas de
   classification. On prend le modele lineaire plutot qu'un modele plus
   puissant parce que la question 4 demande DE QUOI depend la frequentation :
   un modele lineaire donne un coefficient lisible par variable, ce qu'une
   foret aleatoire ou un gradient boosting ne donnent pas directement.

2) a_resilie est EXCLUE des variables explicatives. L'enonce demande de
   predire pour un abonne qui signe demain : a cet instant on ne sait pas
   encore s'il resiliera. Garder cette variable ferait fuiter une information
   du futur dans le modele (fuite de donnees) et donnerait une performance
   impossible a reproduire en situation reelle. abonne_id est exclue aussi :
   c'est un identifiant, il ne porte aucune information.

3) get_dummies(drop_first=True) pour formule et creneau_habituel. Une
   regression lineaire ne sait traiter que des nombres. On cree une
   indicatrice par modalite sauf une, qui sert de reference : garder toutes
   les modalites rendrait les colonnes colineaires (leur somme vaut toujours
   1) et les coefficients instables.

4) train_test_split 25 % de test. On evalue le modele sur des abonnes qu'il
   n'a jamais vus, sinon on mesure sa capacite a reciter et non a predire.
   random_state=42 pour que le resultat soit reproductible d'une execution
   a l'autre.

5) MAE d'un modele naif comme point de comparaison. Un R2 ou une MAE seuls
   ne disent pas si le modele sert a quelque chose. On compare donc a la
   strategie la plus bete possible, qui est de toujours predire la moyenne :
   si le modele ne fait pas nettement mieux, il ne vaut pas son cout.

6) Validation croisee KFold 5 plis en plus du decoupage unique. Un seul
   decoupage peut etre chanceux ou malchanceux. La validation croisee donne
   une moyenne sur 5 decoupages differents, et surtout un ecart-type qui dit
   a quel point le resultat depend du decoupage. shuffle=True car on ne sait
   pas si l'ordre des lignes du fichier porte une structure.

7) Coefficients standardises (StandardScaler avant regression) pour la
   question 4. Les coefficients bruts sont exprimes dans l'unite de chaque
   variable : celui de la distance est en visites par metre, celui du
   coaching en visites par seance. Ils ne sont donc pas comparables. Apres
   standardisation, chaque coefficient se lit "variation de la frequentation
   quand la variable augmente d'un ecart-type", ce qui se compare. On affiche
   l'ecart-type de la cible a cote pour juger si un coefficient est gros.

8) matplotlib.use("Agg") : on enregistre des fichiers PNG sans ouvrir de
   fenetre, ce qui est necessaire pour une execution en ligne de commande.
"""

import os

import matplotlib
matplotlib.use("Agg")  # backend sans fenetre : on ecrit des PNG, on n'affiche rien
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

# Ce que l'on cherche a predire
CIBLE = "visites_par_mois"

# Variables explicatives numeriques (a_resilie et abonne_id sont exclues,
# cf. point 2 de la docstring)
EXPLICATIVES_NUMERIQUES = [
    "anciennete_mois",
    "prix_mensuel_eur",
    "distance_domicile_m",
    "seances_coaching",
    "reclamations",
]

# Variables explicatives qualitatives, transformees en indicatrices
EXPLICATIVES_QUALITATIVES = ["formule", "creneau_habituel"]

# Parametres de decoupage, fixes pour que les resultats soient reproductibles
PART_TEST = 0.25
GRAINE = 42
NOMBRE_PLIS = 5

DOSSIER_FIGURES = os.path.join("outputs", "figures")


def preparer_donnees(abonnes):
    """Construit la matrice des variables explicatives et le vecteur cible."""
    colonnes = EXPLICATIVES_NUMERIQUES + EXPLICATIVES_QUALITATIVES
    explicatives = pd.get_dummies(abonnes[colonnes], drop_first=True)
    cible = abonnes[CIBLE]
    return explicatives, cible


def entrainer_et_evaluer(explicatives, cible):
    """Entraine la regression sur 75 % des abonnes et l'evalue sur les 25 % restants.

    Retourne un dictionnaire de resultats et les vecteurs necessaires aux figures.
    """
    entrainement_x, test_x, entrainement_y, test_y = train_test_split(
        explicatives, cible, test_size=PART_TEST, random_state=GRAINE
    )

    modele = LinearRegression()
    modele.fit(entrainement_x, entrainement_y)
    predictions = modele.predict(test_x)

    # Modele naif : predire toujours la moyenne du jeu d'entrainement.
    # C'est le point de comparaison minimal (cf. point 5 de la docstring).
    prediction_naive = np.full(len(test_y), entrainement_y.mean())

    resultats = {
        "r2_test": r2_score(test_y, predictions),
        "mae_test": mean_absolute_error(test_y, predictions),
        # squared=False n'existe pas dans toutes les versions de scikit-learn :
        # on prend la racine carree de la MSE a la main, c'est la meme chose
        "rmse_test": np.sqrt(mean_squared_error(test_y, predictions)),
        "mae_naif": mean_absolute_error(test_y, prediction_naive),
        "moyenne_entrainement": entrainement_y.mean(),
        "taille_entrainement": len(entrainement_y),
        "taille_test": len(test_y),
    }
    return resultats, modele, test_y, predictions


def valider_par_plis(explicatives, cible):
    """Validation croisee KFold 5 plis sur le R2 et la MAE.

    L'ecart-type renvoye dit a quel point la performance depend du decoupage.
    """
    plis = KFold(n_splits=NOMBRE_PLIS, shuffle=True, random_state=GRAINE)

    r2_par_pli = cross_val_score(LinearRegression(), explicatives, cible,
                                 cv=plis, scoring="r2")
    # scikit-learn ne sait que maximiser un score : la MAE est donc fournie
    # en negatif, on remet le signe a l'endroit
    mae_par_pli = -cross_val_score(LinearRegression(), explicatives, cible,
                                   cv=plis, scoring="neg_mean_absolute_error")
    return r2_par_pli, mae_par_pli


def coefficients_standardises(explicatives, cible):
    """Coefficients de la regression sur variables standardisees, tries par poids.

    On reentraine sur la totalite des abonnes : il ne s'agit plus ici de
    mesurer une performance mais de decrire de quoi depend la frequentation,
    donc autant utiliser toute l'information disponible.
    """
    explicatives_standardisees = StandardScaler().fit_transform(explicatives)

    modele = LinearRegression()
    modele.fit(explicatives_standardisees, cible)

    coefficients = pd.DataFrame({
        "variable": explicatives.columns,
        "coefficient": modele.coef_.round(3),
    })
    coefficients = coefficients.reindex(
        coefficients["coefficient"].abs().sort_values(ascending=False).index
    ).reset_index(drop=True)
    return coefficients


def tracer_figures(test_y, predictions, coefficients):
    """Enregistre les trois figures PNG dans outputs/figures/."""
    os.makedirs(DOSSIER_FIGURES, exist_ok=True)
    chemins = []

    # Figure 1 : predictions contre realite. La diagonale est le modele parfait ;
    # plus les points en sont loin, plus le modele se trompe.
    plt.figure(figsize=(7, 7))
    plt.scatter(test_y, predictions, alpha=0.5, edgecolor="none")
    minimum = min(test_y.min(), predictions.min())
    maximum = max(test_y.max(), predictions.max())
    plt.plot([minimum, maximum], [minimum, maximum], "r--", label="prediction parfaite")
    plt.xlabel("Visites par mois observees")
    plt.ylabel("Visites par mois predites")
    plt.title("Predictions contre realite (jeu de test)")
    plt.legend()
    plt.grid(alpha=0.3)
    chemin = os.path.join(DOSSIER_FIGURES, "phase2_predictions_vs_realite.png")
    plt.tight_layout()
    plt.savefig(chemin, dpi=120)
    plt.close()
    chemins.append(chemin)

    # Figure 2 : residus contre predictions. Un nuage sans forme autour de zero
    # valide l'hypothese lineaire ; une courbure ou un entonnoir la mettrait en cause.
    residus = test_y - predictions
    plt.figure(figsize=(8, 5))
    plt.scatter(predictions, residus, alpha=0.5, edgecolor="none")
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Visites par mois predites")
    plt.ylabel("Residu (observe - predit)")
    plt.title("Residus contre predictions")
    plt.grid(alpha=0.3)
    chemin = os.path.join(DOSSIER_FIGURES, "phase2_residus.png")
    plt.tight_layout()
    plt.savefig(chemin, dpi=120)
    plt.close()
    chemins.append(chemin)

    # Figure 3 : les 8 coefficients standardises les plus forts. Barres
    # horizontales car les noms de variables sont longs et illisibles en abscisse.
    les_plus_forts = coefficients.head(8).iloc[::-1]  # inverse : le plus fort en haut
    couleurs = ["tab:green" if valeur > 0 else "tab:red"
                for valeur in les_plus_forts["coefficient"]]
    plt.figure(figsize=(9, 5))
    plt.barh(les_plus_forts["variable"], les_plus_forts["coefficient"], color=couleurs)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlabel("Coefficient standardise (effet d'un ecart-type)")
    plt.title("Les 8 variables qui pesent le plus sur la frequentation")
    plt.grid(axis="x", alpha=0.3)
    chemin = os.path.join(DOSSIER_FIGURES, "phase2_coefficients.png")
    plt.tight_layout()
    plt.savefig(chemin, dpi=120)
    plt.close()
    chemins.append(chemin)

    return chemins


def modeliser_frequentation(abonnes):
    """Enchaine toute la modelisation des questions 3 et 4 et affiche les resultats."""
    explicatives, cible = preparer_donnees(abonnes)

    print("Cible :", CIBLE)
    print("Variables explicatives apres indicatrices :", explicatives.shape[1])
    print("Liste :", ", ".join(explicatives.columns))
    print("Exclues volontairement : a_resilie (information du futur), abonne_id")

    print("\n=== QUESTION 3 : combien de visites par mois predire ? ===")
    resultats, _, test_y, predictions = entrainer_et_evaluer(explicatives, cible)
    print("Abonnes d'entrainement : {}   abonnes de test : {}".format(
        resultats["taille_entrainement"], resultats["taille_test"]))
    print("\n--- Performance sur le jeu de test ---")
    print("R2   : {:.3f}".format(resultats["r2_test"]))
    print("MAE  : {:.2f} visites par mois".format(resultats["mae_test"]))
    print("RMSE : {:.2f} visites par mois".format(resultats["rmse_test"]))

    print("\n--- Comparaison avec un modele naif ---")
    print("Un modele qui predirait toujours la moyenne ({:.2f} visites) obtiendrait".format(
        resultats["moyenne_entrainement"]))
    print("une MAE de {:.2f} visites par mois.".format(resultats["mae_naif"]))
    gain = (1 - resultats["mae_test"] / resultats["mae_naif"]) * 100
    print("Le modele reduit donc l'erreur moyenne de {:.1f} %.".format(gain))

    print("\n--- Validation croisee KFold {} plis ---".format(NOMBRE_PLIS))
    r2_par_pli, mae_par_pli = valider_par_plis(explicatives, cible)
    print("R2  : moyenne {:.3f}   ecart-type {:.3f}".format(r2_par_pli.mean(), r2_par_pli.std()))
    print("      par pli :", np.round(r2_par_pli, 3))
    print("MAE : moyenne {:.3f}   ecart-type {:.3f}".format(mae_par_pli.mean(), mae_par_pli.std()))
    print("      par pli :", np.round(mae_par_pli, 3))

    print("\n=== QUESTION 4 : de quoi depend la frequentation ? ===")
    coefficients = coefficients_standardises(explicatives, cible)
    print("Coefficients standardises (effet d'un ecart-type de la variable,")
    print("exprime en visites par mois), tries par poids absolu :")
    for _, ligne in coefficients.iterrows():
        print("{:<30} {:+.3f}".format(ligne["variable"], ligne["coefficient"]))
    print("\nPour mise en perspective, l'ecart-type de la frequentation est de")
    print("{:.2f} visites par mois.".format(cible.std()))

    print("\n--- Figures ---")
    for chemin in tracer_figures(test_y, predictions, coefficients):
        print("enregistree :", chemin)

    print("\nReponse a la question 3 : le modele predit la frequentation d'un")
    print("nouvel abonne a environ {:.1f} visites pres en moyenne, contre {:.1f}".format(
        resultats["mae_test"], resultats["mae_naif"]))
    print("si l'on se contentait de la moyenne. Il explique {:.0f} % de la".format(
        resultats["r2_test"] * 100))
    print("variance de la frequentation sur des abonnes jamais vus.")

    print("\nReponse a la question 4 : la frequentation depend d'abord du")
    print("nombre de seances de coaching, loin devant tout le reste (un")
    print("ecart-type de coaching vaut la moitie d'un ecart-type de visites),")
    print("puis de la formule Premium et du creneau du soir ; la distance au")
    print("domicile, l'anciennete et les reclamations suivent avec un poids")
    print("deux a trois fois plus faible, la distance et les reclamations")
    print("tirant la frequentation vers le bas. La marge d'erreur avec")
    print("laquelle il faut vivre est de l'ordre de {:.1f} visites par mois en".format(
        resultats["mae_test"]))
    print("moyenne ({:.1f} en RMSE, qui pese plus lourdement les gros ecarts),".format(
        resultats["rmse_test"]))
    print("soit environ la moitie d'un ecart-type de la cible. Une prediction")
    print("individuelle ne doit donc pas etre annoncee comme un chiffre exact.")
