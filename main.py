
from src.data_loader import load_data
from src.exploration import analyser_resiliations, analyser_distance
from src.preprocessing import (
    supprimer_doublons,
    traiter_coaching_manquant,
    traiter_creneau_manquant,
    corriger_anciennetes,
    corriger_prix
)
from src.regression import (
    preparer_regression,
    entrainer_regression,
    predire_visites,
    analyser_coefficients,
    optimiser_random_forest
)
from src.evaluation import evaluer_regression, evaluer_reference
from src.visualization import (
    visualiser_resiliations_formule,
    visualiser_resiliations_creneau,
    visualiser_resiliations_distance,
    visualiser_predictions,
    visualiser_comparaison_modeles
)


# Exécuter les différentes étapes du projet
def main():
    abonnes, salles = load_data()

    print("\n--- Nettoyage des données ---")
    abonnes = supprimer_doublons(abonnes)
    abonnes = traiter_coaching_manquant(abonnes)
    abonnes = traiter_creneau_manquant(abonnes)
    abonnes = corriger_anciennetes(abonnes)
    abonnes = corriger_prix(abonnes)

    abonnes.to_csv("data/processed/FitZone_abonnes_clean.csv", index=False)
    salles.to_csv("data/processed/FitZone_salles_clean.csv", index=False)

    print("\n--- Sauvegarde des données nettoyées ---")
    print("Fichiers enregistrés dans data/processed/")

    analyser_resiliations(abonnes)
    visualiser_resiliations_formule(abonnes)
    visualiser_resiliations_creneau(abonnes)

    analyser_distance(abonnes)
    visualiser_resiliations_distance(abonnes)

    print("\n--- Préparation de la régression ---")
    X_train, X_test, y_train, y_test = preparer_regression(abonnes)

    modele = entrainer_regression(X_train, y_train)

    print("\n--- Régression linéaire ---")
    predictions = predire_visites(modele, X_test)
    evaluer_regression(y_test, predictions)
    visualiser_predictions(y_test, predictions)

    analyser_coefficients(modele, X_train)

    predictions_reference = evaluer_reference(
        X_train, X_test, y_train, y_test
    )

    print("\n--- Random Forest optimisé ---")
    modele_rf = optimiser_random_forest(X_train, y_train)
    predictions_rf = predire_visites(modele_rf, X_test)
    evaluer_regression(y_test, predictions_rf)

    visualiser_comparaison_modeles(
        y_test,
        predictions_reference,
        predictions,
        predictions_rf
    )


if __name__ == "__main__":
    main()
