import pandas as pd
from src.data_loader import load_data, load_data_clean
from src.classification import (
    preparer_donnees_classification,
    entrainer_regression_logistique,
    tableau_gains,
    estimer_resilies_atteints,
    calculer_gain_net,
    comparer_campagnes,
)
from src.regression import (
    preparer_donnees_regression,
    decouper_donnees,
    evaluer_baseline,
    evaluer_modele,
    entrainer_regression_lineaire,
    validation_croisee,
    coefficients_standardises,
)
from src.exploration import (
    explorer_structure, 
    verifier_anomalies, 
    verifier_types_unites,
    comparer_resilies,
    taux_resiliation_par,
    test_independance_chi2,
    test_mann_whitney,
    creer_tranches_distance,
    test_kruskal,
)
from src.preprocessing import (
    supprimer_doublons,
    traiter_coaching_manquant,
    traiter_creneau_manquant,
    supprimer_anciennetes_negatives,
    corriger_prix,
    convertir_oui_non,
)


def preparer_donnees():
    """Phase 1 : exploration, nettoyage et sauvegarde des données."""
    abonnes, salles = load_data()

    print("\n--- Structure des données ---")
    explorer_structure(abonnes, salles)
    print("\n--- Recherche des anomalies ---")
    verifier_anomalies(abonnes, salles)
    print("\n--- Types et unités ---")
    verifier_types_unites(abonnes, salles)

    print("\n--- Nettoyage des données ---")
    abonnes = supprimer_doublons(abonnes)
    abonnes = traiter_coaching_manquant(abonnes)
    abonnes = traiter_creneau_manquant(abonnes)
    abonnes = supprimer_anciennetes_negatives(abonnes)
    abonnes = corriger_prix(abonnes)
    abonnes = convertir_oui_non(abonnes, "a_resilie")
    salles = convertir_oui_non(salles, "parking")

    print("\n--- Vérification finale des abonnés ---")
    print("Dimensions :", abonnes.shape)
    print("Doublons :", abonnes.duplicated().sum())
    print("Valeurs manquantes :")
    print(abonnes.isna().sum())
    print("Anciennetés négatives :", (abonnes["anciennete_mois"] < 0).sum())
    print("Prix mensuels nuls :", (abonnes["prix_mensuel_eur"] == 0).sum())

    abonnes.to_csv("data/processed/FitZone_abonnes_clean.csv", index=False)
    salles.to_csv("data/processed/FitZone_salles_clean.csv", index=False)
    print("\n--- Données nettoyées enregistrées dans data/processed/ ---")


def analyser_resiliations(abonnes):
    """Phase 2, question 1 : facteurs associés aux résiliations."""
    print("\n===== Question 1 : facteurs associés aux résiliations =====")

    comparer_resilies(abonnes, ["anciennete_mois", "distance_domicile_m",
                                "visites_par_mois", "seances_coaching"])
    taux_resiliation_par(abonnes, ["reclamations", "formule", "creneau_habituel"])

    test_independance_chi2(abonnes, "formule", "a_resilie")
    test_independance_chi2(abonnes, "creneau_habituel", "a_resilie")
    test_independance_chi2(abonnes, "salle", "a_resilie")

    # Réclamations : 3 et 4 regroupées avec 2 pour respecter la condition
    # du chi² (au moins 5 attendus par case)
    abonnes["reclamations_groupe"] = abonnes["reclamations"].clip(upper=2)
    test_independance_chi2(abonnes, "reclamations_groupe", "a_resilie")

    for colonne in ["anciennete_mois", "distance_domicile_m",
                    "visites_par_mois", "seances_coaching"]:
        test_mann_whitney(abonnes, colonne)


def analyser_distance(abonnes):
    """Phase 2, question 2 : influence de la distance domicile-salle."""
    print("\n===== Question 2 : influence de la distance =====")

    abonnes = creer_tranches_distance(abonnes)
    taux_resiliation_par(abonnes, ["tranche_distance"])
    test_independance_chi2(abonnes, "tranche_distance", "a_resilie")
    test_kruskal(abonnes, "tranche_distance", "visites_par_mois")
    print(abonnes.groupby("creneau_habituel")["visites_par_mois"].agg(["mean", "median", "count"]))
    test_kruskal(abonnes, "creneau_habituel", "visites_par_mois")


def modeliser_frequentation(abonnes):
    """Phase 2, questions 3 et 4 : prédiction de la fréquentation et évaluation."""
    print("\n===== Questions 3 et 4 : prédiction de la fréquentation =====")

    X, y = preparer_donnees_regression(abonnes, ["formule", "creneau_habituel", "salle"])

    # Évaluation sur un découpage entraînement / test
    X_train, X_test, y_train, y_test = decouper_donnees(X, y)

    print("\n----- Modèle de référence (baseline) -----")
    evaluer_baseline(y_train, y_test)

    print("\n----- Régression linéaire -----")
    modele = entrainer_regression_lineaire(X_train, y_train)
    evaluer_modele(modele, X_train, y_train, "l'entraînement")
    evaluer_modele(modele, X_test, y_test, "le test")

    predictions = modele.predict(X_test)
    comparaison = pd.DataFrame({"reel": y_test.values, "predit": predictions.round(1)})
    comparaison["erreur"] = (comparaison["reel"] - comparaison["predit"]).abs()
    print("\n--- Les 10 plus grosses erreurs ---")
    print(comparaison.sort_values("erreur", ascending=False).head(10))

    # Évaluation robuste : validation croisée sur toutes les données
    print("\n----- Validation croisée -----")
    validation_croisee(X, y)

    # Interprétation : coefficients bruts, puis standardisés (sur toutes les données)
    print("\n----- Coefficients bruts -----")
    print(pd.Series(modele.coef_, index=X_train.columns).sort_values())

    print("\n----- Coefficients standardisés -----")
    colonnes_numeriques = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m",
                           "seances_coaching", "reclamations"]
    coefficients_standardises(X, y, colonnes_numeriques)
    

def modeliser_resiliation(abonnes):
    """ Phase 3 : prédiction de la résiliation."""

    X, y = preparer_donnees_classification(abonnes, ["formule", "creneau_habituel", "salle"])

    # Évaluation sur un découpage entraînement / test
    X_train, X_test, y_train, y_test = decouper_donnees(X, y, stratify=y)

    resultats = tableau_gains(X,y)
    print(resultats)
    prix_resilies = abonnes[abonnes["a_resilie"] == 1]["prix_mensuel_eur"].mean()
    print(f"Prix mensuel moyen des résiliés : {prix_resilies:.2f} €")
    comparer_campagnes(resultats, prix_resilies)



def main():
    # Phase 1 : à relancer uniquement si les données brutes ou le nettoyage changent
    # preparer_donnees()

    abonnes_clean, salles_clean = load_data_clean()

    # Chaque analyse travaille sur sa propre copie : les colonnes ajoutées
    # par l'une (tranche_distance, reclamations_groupe) ne gênent pas les autres
    #analyser_resiliations(abonnes_clean.copy())
    #analyser_distance(abonnes_clean.copy())
    #modeliser_frequentation(abonnes_clean.copy())
    modeliser_resiliation(abonnes_clean.copy())


if __name__ == "__main__":
    main()