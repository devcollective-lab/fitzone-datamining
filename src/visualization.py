import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error


# Visualiser les taux de résiliation par formule
def visualiser_resiliations_formule(abonnes):
    taux = []

    for formule in abonnes["formule"].unique():
        groupe = abonnes[abonnes["formule"] == formule]
        nb_resilies = (groupe["a_resilie"] == "oui").sum()
        pourcentage = nb_resilies / len(groupe) * 100

        taux.append({
            "formule": formule,
            "taux_resiliation": pourcentage
        })

    resultats = pd.DataFrame(taux)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=resultats,
        x="formule",
        y="taux_resiliation",
        color="steelblue"
    )

    plt.title("Taux de résiliation par formule")
    plt.xlabel("Formule")
    plt.ylabel("Taux de résiliation (%)")
    plt.ylim(0, 45)

    plt.tight_layout()
    plt.savefig("outputs/figures/resiliations_formule.png")
    plt.close()

    print("Graphique enregistré : outputs/figures/resiliations_formule.png")


# Visualiser les taux de résiliation par créneau
def visualiser_resiliations_creneau(abonnes):
    taux = []

    for creneau in abonnes["creneau_habituel"].unique():
        groupe = abonnes[abonnes["creneau_habituel"] == creneau]
        nb_resilies = (groupe["a_resilie"] == "oui").sum()
        pourcentage = nb_resilies / len(groupe) * 100

        taux.append({
            "creneau": creneau,
            "taux_resiliation": pourcentage
        })

    resultats = pd.DataFrame(taux)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=resultats,
        x="creneau",
        y="taux_resiliation",
        color="steelblue"
    )

    plt.title("Taux de résiliation par créneau habituel")
    plt.xlabel("Créneau habituel")
    plt.ylabel("Taux de résiliation (%)")
    plt.ylim(0, 40)

    plt.tight_layout()
    plt.savefig("outputs/figures/resiliations_creneau.png")
    plt.close()

    print("Graphique enregistré : outputs/figures/resiliations_creneau.png")


# Visualiser les taux de résiliation selon la distance
def visualiser_resiliations_distance(abonnes):
    tranches = [
        (0, 2000, "0 à 2 km"),
        (2000, 5000, "2 à 5 km"),
        (5000, 10000, "5 à 10 km"),
        (10000, float("inf"), "10 km et plus")
    ]

    taux = []

    for minimum, maximum, distance in tranches:
        groupe = abonnes[
            (abonnes["distance_domicile_m"] >= minimum) &
            (abonnes["distance_domicile_m"] < maximum)
        ]

        if len(groupe) > 0:
            nb_resilies = (groupe["a_resilie"] == "oui").sum()
            pourcentage = nb_resilies / len(groupe) * 100

            taux.append({
                "distance": distance,
                "taux_resiliation": pourcentage
            })

    resultats = pd.DataFrame(taux)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=resultats,
        x="distance",
        y="taux_resiliation",
        color="steelblue"
    )

    plt.title("Taux de résiliation selon la distance")
    plt.xlabel("Distance domicile-salle")
    plt.ylabel("Taux de résiliation (%)")
    plt.ylim(0, 45)

    plt.tight_layout()
    plt.savefig("outputs/figures/resiliations_distance.png")
    plt.close()

    print("Graphique enregistré : outputs/figures/resiliations_distance.png")


# Comparer les visites réelles et prédites
def visualiser_predictions(y_test, predictions):
    plt.figure(figsize=(8, 5))

    sns.scatterplot(
        x=y_test,
        y=predictions,
        color="steelblue"
    )

    minimum = min(y_test.min(), predictions.min())
    maximum = max(y_test.max(), predictions.max())

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
        color="red",
        linestyle="--"
    )

    plt.title("Visites réelles et prédites")
    plt.xlabel("Visites réelles par mois")
    plt.ylabel("Visites prédites par mois")

    plt.tight_layout()
    plt.savefig("outputs/figures/predictions_regression.png")
    plt.close()

    print("Graphique enregistré : outputs/figures/predictions_regression.png")


# Comparer les erreurs des modèles de régression
def visualiser_comparaison_modeles(y_test, predictions_reference,
                                  predictions_lineaire, predictions_rf):

    modeles = [
        "Référence",
        "Régression linéaire",
        "Random Forest"
    ]

    erreurs = [
        mean_absolute_error(y_test, predictions_reference),
        mean_absolute_error(y_test, predictions_lineaire),
        mean_absolute_error(y_test, predictions_rf)
    ]

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=modeles,
        y=erreurs,
        color="steelblue"
    )

    plt.title("Comparaison des erreurs des modèles")
    plt.xlabel("Modèle")
    plt.ylabel("MAE (visites par mois)")
    plt.ylim(0, 4)

    plt.tight_layout()
    plt.savefig("outputs/figures/comparaison_modeles.png")
    plt.close()

    print("Graphique enregistré : outputs/figures/comparaison_modeles.png")
