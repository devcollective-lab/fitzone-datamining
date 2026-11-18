import pandas as pd
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_predict

def preparer_donnees_classification(df, colonnes):
    """Prépare les données pour la classification en encodant les variables catégorielles et en séparant les variables
    indépendantes (X) de la variable dépendante (y)."""
    df_encode = pd.get_dummies(df, columns=colonnes, drop_first=True, dtype=int)
    y = df_encode["a_resilie"]
    X = df_encode.drop(columns=["abonne_id", "a_resilie", "tranche_distance", "reclamations_groupe"],
    errors="ignore")

    return X, y

def entrainer_regression_logistique(X_train, y_train):
    """ Crée et entraîne une régression logistique, puis renvoie le modèle entraîné. """
    modele = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    modele.fit(X_train, y_train)

    return modele

def tableau_gains(X, y):
    """Estime le risque de résiliation de chaque abonné par validation croisée,
    puis affiche, pour différentes tailles de campagne d'appels, le nombre de
    résiliés atteints, le rappel et la précision. Renvoie les abonnés triés par risque."""
    decoupage = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    modele = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

    probas = cross_val_predict(modele, X, y, cv=decoupage, method="predict_proba")[:, 1]

    resultats = pd.DataFrame({"risque": probas, "a_resilie": y.values})
    resultats = resultats.sort_values("risque", ascending=False)

    total_resilies = resultats["a_resilie"].sum()
    for part in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]:
        nb_appels = round(len(resultats) * part)
        atteints = resultats.head(nb_appels)["a_resilie"].sum()
        rappel = atteints / total_resilies
        precision = atteints / nb_appels
        print(f"{part:.0%} appelés ({nb_appels}) : {atteints} résiliés atteints, "
              f"rappel {rappel:.0%}, précision {precision:.0%}")

    return resultats

def estimer_resilies_atteints(resultats, nb_abonnes, nb_appels):
    """Estime combien de futurs résiliés une campagne de nb_appels atteint,
    sur un groupe de nb_abonnes, à partir des abonnés triés par risque
    (tableau renvoyé par tableau_gains)."""
    part_appelee = nb_appels / nb_abonnes
    nb_lignes = round(len(resultats) * part_appelee)
    rappel = resultats.head(nb_lignes)["a_resilie"].sum() / resultats["a_resilie"].sum()
    resilies_attendus = nb_abonnes * resultats["a_resilie"].mean()
    return rappel * resilies_attendus


def calculer_gain_net(nb_appels, resilies_atteints, taux_succes,
                      prix_mensuel, duree_mois, cout_appel):
    """Calcule le gain net d'une campagne d'appels : revenu des abonnés
    retenus moins le coût des appels."""
    abonnes_retenus = resilies_atteints * taux_succes
    revenu = abonnes_retenus * prix_mensuel * duree_mois
    cout = nb_appels * cout_appel
    return revenu - cout


def comparer_campagnes(resultats, prix_mensuel, nb_abonnes=400,
                       duree_mois=3, cout_appel=5):
    """Compare une campagne de 80 appels et une campagne de 160 appels,
    pour trois hypothèses de taux de succès."""
    for taux_succes in [0.15, 1 / 3, 0.5]:
        print(f"\n--- Taux de succès : {taux_succes:.0%} ---")
        gains = {}
        for nb_appels in [80, 160]:
            atteints = estimer_resilies_atteints(resultats, nb_abonnes, nb_appels)
            gains[nb_appels] = calculer_gain_net(nb_appels, atteints, taux_succes,
                                                 prix_mensuel, duree_mois, cout_appel)
            print(f"{nb_appels} appels : {atteints:.0f} résiliés atteints, "
                  f"{atteints * taux_succes:.0f} retenus, gain net {gains[nb_appels]:+.0f} €")
        print(f"Les 80 appels supplémentaires : {gains[160] - gains[80]:+.0f} €")