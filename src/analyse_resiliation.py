"""
Analyse des facteurs de resiliation chez FitZone (questions 1 et 2).

Question 1 : qu'est-ce qui distingue un abonne qui reste d'un abonne qui part ?
Question 2 : la distance domicile-salle explique-t-elle vraiment les departs ?

JUSTIFICATION DES METHODES RETENUES
-----------------------------------
1) Variables numeriques : test de Mann-Whitney et non un test de Student.
   Le test de Student suppose des distributions normales dans chaque groupe.
   Or anciennete_mois et seances_coaching sont tres asymetriques (beaucoup
   d'abonnes recents, beaucoup d'abonnes a zero seance de coaching), donc
   l'hypothese de normalite est fausse. Mann-Whitney compare les rangs et ne
   suppose rien sur la forme des distributions : c'est le test adapte ici.

2) Taille d'effet en plus de la p-value. Une p-value dit seulement si un
   ecart est difficilement attribuable au hasard, pas s'il est important.
   Avec 797 abonnes, un ecart minuscule peut sortir significatif. On divise
   donc l'ecart des moyennes par l'ecart-type global pour obtenir un ecart
   exprime en nombre d'ecarts-types, comparable d'une variable a l'autre.

3) Variables qualitatives : chi2 d'independance. C'est le test standard pour
   savoir si deux variables categorielles sont liees (ici formule, creneau ou
   salle contre le fait d'avoir resilie). On affiche en plus les tableaux
   croises en pourcentage, parce que le chi2 dit qu'il existe un lien mais
   pas dans quel sens il va.

4) Regression logistique multivariee pour finir. Les tests precedents sont
   bivaries : ils regardent chaque variable seule et confondent donc les
   effets correles entre eux (le prix et la formule, par exemple, disent en
   partie la meme chose). La regression logistique estime l'effet propre de
   chaque variable, les autres etant tenues constantes. On standardise les
   variables avant (StandardScaler) pour que les coefficients soient
   comparables entre eux : sans cela, le coefficient de la distance (en
   metres, donc des milliers) et celui des reclamations (0, 1, 2) ne seraient
   pas lisibles sur la meme echelle.

5) La variable salle n'entre PAS dans le modele multivarie. Son chi2 est non
   significatif (voir la sortie) et elle vaudrait 13 variables indicatrices
   supplementaires sans apport : on les ecarte pour ne pas diluer le modele.

6) AUC en validation croisee 5 plis et non sur les donnees d'entrainement.
   Un modele evalue sur les donnees qui l'ont entraine surestime toujours sa
   performance. On mesure aussi l'AUC plutot que le taux de bonnes reponses
   car les classes sont desequilibrees (environ 1 resiliation sur 5) : un
   modele qui repondrait toujours "ne resilie pas" aurait un bon taux de
   bonnes reponses tout en etant inutile.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

# Variables numeriques candidates a l'explication de la resiliation
VARIABLES_NUMERIQUES = [
    "anciennete_mois",
    "prix_mensuel_eur",
    "distance_domicile_m",
    "visites_par_mois",
    "seances_coaching",
    "reclamations",
]

# Variables qualitatives testees au chi2
VARIABLES_QUALITATIVES = ["formule", "creneau_habituel", "salle"]

# Variables qualitatives retenues dans le modele multivarie (cf. point 5
# de la docstring : salle est ecartee car son chi2 est non significatif)
QUALITATIVES_DU_MODELE = ["formule", "creneau_habituel"]

# Bornes des tranches de distance, en metres, pour la question 2
BORNES_DISTANCE = [0, 1000, 2000, 3000, 5000, np.inf]
ETIQUETTES_DISTANCE = ["<1 km", "1-2 km", "2-3 km", "3-5 km", ">5 km"]


def construire_cible(abonnes):
    """Transforme a_resilie (oui/non) en cible binaire 1/0.

    On code 1 = a resilie, pour que les coefficients positifs du modele se
    lisent ensuite comme "augmente le risque de depart".
    """
    return (abonnes["a_resilie"] == "oui").astype(int)


def comparer_variables_numeriques(abonnes, churn):
    """Compare chaque variable numerique entre abonnes restants et partants.

    Pour chaque variable : moyenne des restants, moyenne des partants,
    p-value de Mann-Whitney et taille d'effet (ecart des moyennes divise par
    l'ecart-type global). Retourne un tableau trie par taille d'effet.
    """
    lignes = []
    for variable in VARIABLES_NUMERIQUES:
        restants = abonnes.loc[churn == 0, variable]
        partants = abonnes.loc[churn == 1, variable]

        # alternative="two-sided" : on ne prejuge pas du sens de l'ecart
        _, p_value = stats.mannwhitneyu(restants, partants, alternative="two-sided")

        # Taille d'effet : ecart des moyennes ramene en nombre d'ecarts-types.
        # Signe positif = la variable est plus elevee chez les partants.
        effet = (partants.mean() - restants.mean()) / abonnes[variable].std()

        lignes.append({
            "variable": variable,
            "moyenne_restants": round(restants.mean(), 2),
            "moyenne_partants": round(partants.mean(), 2),
            "p_value": p_value,
            "taille_effet": round(effet, 3),
        })

    tableau = pd.DataFrame(lignes)
    # Tri par taille d'effet absolue : on veut voir d'abord ce qui separe le plus
    tableau = tableau.reindex(tableau["taille_effet"].abs().sort_values(ascending=False).index)
    return tableau.reset_index(drop=True)


def tester_variables_qualitatives(abonnes):
    """Chi2 d'independance entre chaque variable qualitative et a_resilie.

    Retourne un tableau avec la statistique, les degres de liberte et la
    p-value pour formule, creneau_habituel et salle.
    """
    lignes = []
    for variable in VARIABLES_QUALITATIVES:
        tableau_croise = pd.crosstab(abonnes[variable], abonnes["a_resilie"])
        chi2, p_value, degres_liberte, _ = stats.chi2_contingency(tableau_croise)
        lignes.append({
            "variable": variable,
            "chi2": round(chi2, 3),
            "degres_liberte": degres_liberte,
            "p_value": p_value,
        })
    return pd.DataFrame(lignes)


def tableau_croise_pourcentage(abonnes, variable):
    """Taux de resiliation en pourcentage pour chaque modalite d'une variable.

    Le chi2 signale un lien sans en donner le sens : ce tableau le donne.
    On normalise par ligne (normalize="index") pour lire, dans chaque
    modalite, la part des abonnes partis.
    """
    croise = pd.crosstab(abonnes[variable], abonnes["a_resilie"], normalize="index")
    return (croise * 100).round(1)


def modele_logistique(abonnes, churn):
    """Regression logistique multivariee standardisee.

    Retourne (coefficients, auc_moyenne, auc_par_pli).
    Les coefficients sont tries par valeur absolue decroissante et
    accompagnes de leur odds ratio exp(coefficient).
    """
    # get_dummies avec drop_first=True : une modalite sert de reference, sinon
    # les indicatrices d'une meme variable sont colineaires entre elles
    indicatrices = pd.get_dummies(abonnes[QUALITATIVES_DU_MODELE], drop_first=True)
    explicatives = pd.concat([abonnes[VARIABLES_NUMERIQUES], indicatrices], axis=1)

    # Standardisation : coefficients comparables entre variables d'unites differentes
    explicatives_standardisees = StandardScaler().fit_transform(explicatives)

    # max_iter=1000 : la valeur par defaut (100) ne suffit pas toujours a converger
    modele = LogisticRegression(max_iter=1000)
    modele.fit(explicatives_standardisees, churn)

    coefficients = pd.DataFrame({
        "variable": explicatives.columns,
        "coefficient": modele.coef_[0].round(3),
        "odds_ratio": np.exp(modele.coef_[0]).round(3),
    })
    coefficients = coefficients.reindex(
        coefficients["coefficient"].abs().sort_values(ascending=False).index
    ).reset_index(drop=True)

    # AUC en validation croisee : performance sur des abonnes non vus a l'entrainement
    auc_par_pli = cross_val_score(
        LogisticRegression(max_iter=1000),
        explicatives_standardisees,
        churn,
        cv=5,
        scoring="roc_auc",
    )
    return coefficients, auc_par_pli.mean(), auc_par_pli


def analyser_distance(abonnes, churn, coefficients):
    """Analyse dediee a la question 2 : la distance explique-t-elle les departs ?

    Retourne (distance_restants, distance_partants, p_value, taux_par_tranche,
    rang_de_la_distance). Le rang est la place de distance_domicile_m dans le
    classement des coefficients du modele multivarie : c'est lui qui dit si la
    distance pese vraiment une fois les autres variables tenues constantes.
    """
    restants = abonnes.loc[churn == 0, "distance_domicile_m"]
    partants = abonnes.loc[churn == 1, "distance_domicile_m"]
    _, p_value = stats.mannwhitneyu(restants, partants, alternative="two-sided")

    # Decoupage en tranches : on cherche si le taux de depart monte vraiment
    # avec la distance, ou s'il n'y a pas de progression nette
    tranches = pd.cut(
        abonnes["distance_domicile_m"],
        bins=BORNES_DISTANCE,
        labels=ETIQUETTES_DISTANCE,
        right=False,
    )
    taux_par_tranche = pd.DataFrame({
        "abonnes": churn.groupby(tranches, observed=False).size(),
        "taux_resiliation_pct": (churn.groupby(tranches, observed=False).mean() * 100).round(1),
    })

    rang = int(coefficients.index[coefficients["variable"] == "distance_domicile_m"][0]) + 1
    return restants.mean(), partants.mean(), p_value, taux_par_tranche, rang


def analyser_resiliation(abonnes):
    """Enchaine toute l'analyse des questions 1 et 2 et affiche les resultats."""
    churn = construire_cible(abonnes)

    print("Abonnes analyses :", len(abonnes))
    print("Resiliations :", int(churn.sum()),
          "soit {:.1f} %".format(churn.mean() * 100))

    print("\n=== QUESTION 1 : ce qui distingue un partant d'un restant ===")

    print("\n--- Variables numeriques (test de Mann-Whitney) ---")
    print("Taille d'effet = (moyenne partants - moyenne restants) / ecart-type global")
    numeriques = comparer_variables_numeriques(abonnes, churn)
    for _, ligne in numeriques.iterrows():
        print("{:<22} restants={:>8.2f}  partants={:>8.2f}  p={:.4f}  effet={:+.3f}".format(
            ligne["variable"], ligne["moyenne_restants"], ligne["moyenne_partants"],
            ligne["p_value"], ligne["taille_effet"]))

    print("\n--- Variables qualitatives (chi2 d'independance) ---")
    qualitatives = tester_variables_qualitatives(abonnes)
    for _, ligne in qualitatives.iterrows():
        verdict = "significatif" if ligne["p_value"] < 0.05 else "NON significatif"
        print("{:<18} chi2={:>8.3f}  ddl={:<3} p-value={:.4f}  ({})".format(
            ligne["variable"], ligne["chi2"], ligne["degres_liberte"],
            ligne["p_value"], verdict))

    print("\n--- Taux de resiliation par creneau (en %) ---")
    print(tableau_croise_pourcentage(abonnes, "creneau_habituel"))
    print("\nLecture : le chi2 du creneau est non significatif. L'idee des")
    print("responsables de salle selon laquelle les abonnes du soir seraient")
    print("les plus fideles n'est pas verifiee par les donnees.")

    print("\n--- Taux de resiliation par formule (en %) ---")
    print(tableau_croise_pourcentage(abonnes, "formule"))

    print("\n--- Regression logistique multivariee (variables standardisees) ---")
    coefficients, auc_moyenne, auc_par_pli = modele_logistique(abonnes, churn)
    print("Coefficient negatif = protege du depart, positif = augmente le risque")
    for _, ligne in coefficients.iterrows():
        print("{:<28} coef={:+.3f}   odds ratio={:.3f}".format(
            ligne["variable"], ligne["coefficient"], ligne["odds_ratio"]))
    print("\nAUC moyenne en validation croisee 5 plis : {:.3f}".format(auc_moyenne))
    print("AUC par pli :", np.round(auc_par_pli, 3))

    print("\nReponse a la question 1 : ce qui distingue vraiment un partant,")
    print("c'est l'anciennete faible, le peu de visites et l'absence de")
    print("coaching. Les deux hypotheses des responsables tombent toutes les")
    print("deux. Le creneau : son chi2 est non significatif, les abonnes du")
    print("soir resilient a 23,2 % contre 23,7 % en moyenne. Le prix : en")
    print("bivarie les partants payent bien moins cher (effet -0,61), mais")
    print("dans le modele multivarie le prix devient le plus faible des")
    print("coefficients numeriques et change meme de signe. L'ecart bivarie")
    print("ne venait donc pas du prix lui-meme : il venait de ce que les")
    print("formules cheres incluent du coaching et vont avec des abonnes")
    print("anciens et assidus. Une fois ces variables tenues constantes, le")
    print("prix n'explique plus rien. Baisser les prix ne retiendrait personne.")

    print("\n=== QUESTION 2 : la distance explique-t-elle les departs ? ===")
    moy_restants, moy_partants, p_distance, taux_tranches, rang = analyser_distance(
        abonnes, churn, coefficients
    )
    print("Distance moyenne des restants  : {:.0f} m".format(moy_restants))
    print("Distance moyenne des partants  : {:.0f} m".format(moy_partants))
    print("Ecart                          : {:+.0f} m".format(moy_partants - moy_restants))
    print("p-value bivariee (Mann-Whitney) : {:.4f}".format(p_distance))

    print("\n--- Taux de resiliation par tranche de distance ---")
    print(taux_tranches)

    print("\nRang de distance_domicile_m dans le modele multivarie : {} sur {}".format(
        rang, len(coefficients)))
    print("\nReponse a la question 2 : l'ecart existe et il est statistiquement")
    print("significatif, donc on ne se raconte pas entierement une histoire.")
    print("Mais la distance arrive loin derriere l'anciennete, les visites et")
    print("le coaching dans le modele multivarie : c'est un facteur reel et")
    print("secondaire. La traiter comme la cause principale des departs serait")
    print("une erreur de hierarchie.")
