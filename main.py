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
from src.evaluation import (
    evaluer_regression,
    evaluer_reference,
    evaluer_classification,
    evaluer_priorites,
    simuler_appels
)
from src.visualization import (
    visualiser_resiliations_formule,
    visualiser_resiliations_creneau,
    visualiser_resiliations_distance,
    visualiser_predictions,
    visualiser_comparaison_modeles,
    tracer_evaluation_clusters
)
from src.classification import (
    preparer_classification,
    entrainer_classification,
    predire_resiliations,
    predire_probabilites_resiliation,
    classer_abonnes
)
from src.clustering import (
    COLONNES_NUMERIQUES,
    preparer_donnees_clustering,
    calculer_inerties,
    calculer_silhouettes,
    creer_clusters,
    identifier_profils_clusters,
    analyser_profils_clusters,
    analyser_formules_clusters,
    analyser_revenus_clusters,
    analyser_utilisation_clusters,
    detecter_anomalies,
    analyser_profils_anomalies,
    analyser_formules_anomalies,
    analyser_premium_anomalies,
    analyser_rentabilite_anomalies,
    simuler_scenario_atypiques
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

    print("\n--- Random forest optimisé ---")
    modele_rf = optimiser_random_forest(X_train, y_train)
    predictions_rf = predire_visites(modele_rf, X_test)
    evaluer_regression(y_test, predictions_rf)

    visualiser_comparaison_modeles(
        y_test,
        predictions_reference,
        predictions,
        predictions_rf
    )

    print("\n--- Préparation de la classification ---")
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = preparer_classification(
        abonnes
    )

    modele_clf = entrainer_classification(X_train_clf, y_train_clf)

    predictions_clf = predire_resiliations(modele_clf, X_test_clf)
    evaluer_classification(y_test_clf, predictions_clf)

    probabilites_clf = predire_probabilites_resiliation(
        modele_clf, X_test_clf
    )

    classement = classer_abonnes(X_test_clf, probabilites_clf)

    print("\n--- Abonnés prioritaires ---")
    print(classement.head(10))

    print("\n--- Comparaison des capacités d'appel ---")

    resiliations_32 = evaluer_priorites(
        classement, y_test_clf, nombre=32
    )

    resiliations_64 = evaluer_priorites(
        classement, y_test_clf, nombre=64
    )

    simuler_appels(resiliations_32, resiliations_64)

    print("\n--- Préparation du clustering ---")
    X_scaled = preparer_donnees_clustering(abonnes)

    print("Dimensions des données :", X_scaled.shape)

    print("\n--- Calcul des inerties ---")
    inerties = calculer_inerties(X_scaled)

    for k, inertie in enumerate(inerties, start=2):
        print(f"K = {k} : inertie = {inertie:.2f}")

    print("\n--- Calcul des scores de silhouette ---")
    scores = calculer_silhouettes(X_scaled)

    for k, score in enumerate(scores, start=2):
        print(f"K = {k} : silhouette = {score:.4f}")

    tracer_evaluation_clusters(inerties, scores)

    print("\n--- Comparaison des segmentations ---")

    for k in [2, 4]:
        clusters = creer_clusters(X_scaled, k)

        abonnes_clusters = abonnes.copy()
        abonnes_clusters["cluster"] = clusters

        print(f"\n--- Segmentation en {k} groupes ---")

        moyennes = (
            abonnes_clusters.groupby("cluster")[COLONNES_NUMERIQUES]
            .mean()
            .round(2)
        )

        print(moyennes.to_string())

        print("\nEffectifs par cluster :")
        print(abonnes_clusters["cluster"].value_counts().sort_index())

        if k == 4:
            clusters_retenus = abonnes_clusters.copy()

    abonnes_clusters = clusters_retenus

    print("\n--- Correspondance des profils ---")
    noms_profils = identifier_profils_clusters(abonnes_clusters)

    for cluster, profil in sorted(noms_profils.items()):
        print(f"Cluster {cluster} : {profil}")

    print("\n--- Profils des abonnés ---")
    profils = analyser_profils_clusters(abonnes_clusters)
    print(profils.to_string(index=False))

    print("\n--- Répartition des formules par profil ---")
    formules = analyser_formules_clusters(abonnes_clusters)
    print(formules.to_string())

    print("\n--- Analyse économique des profils ---")
    revenus = analyser_revenus_clusters(abonnes_clusters)
    print(revenus.to_string())

    print("\n--- Utilisation des services par profil ---")
    utilisation = analyser_utilisation_clusters(abonnes_clusters)
    print(utilisation.to_string())

    print("\n--- Détection des abonnés atypiques ---")
    anomalies = detecter_anomalies(X_scaled)

    abonnes_anomalies = abonnes.copy()
    abonnes_anomalies["anomalie"] = anomalies

    nombre_anomalies = (abonnes_anomalies["anomalie"] == -1).sum()

    print("Nombre d'abonnés atypiques :", nombre_anomalies)
    print("Nombre d'autres abonnés :", len(abonnes_anomalies) - nombre_anomalies)

    print("\n--- Profils des abonnés atypiques ---")
    profils_anomalies = analyser_profils_anomalies(abonnes_anomalies)
    print(profils_anomalies.to_string())

    print("\n--- Formules des abonnés atypiques ---")
    formules_anomalies = analyser_formules_anomalies(abonnes_anomalies)
    print(formules_anomalies.to_string())

    print("\n--- Comparaison des abonnés Premium ---")
    profils_premium = analyser_premium_anomalies(abonnes_anomalies)
    print(profils_premium.to_string())

    print("\n--- Simulation de marge des abonnés Premium ---")
    print("Hypothèses : coaching inclus et coût de 25 € par séance.")
    rentabilite = analyser_rentabilite_anomalies(abonnes_anomalies)
    print(rentabilite.to_string())

    print("\n--- Scénario élargi à tous les atypiques ---")
    print(
        "Hypothèse : le coaching serait inclus pour tous les atypiques, "
        "ce qui n'est pas établi par les données."
    )
    scenario = simuler_scenario_atypiques(abonnes_anomalies)
    print(scenario.to_string())
    print("Cette simulation ne représente pas un résultat financier réel.")


if __name__ == "__main__":
    main()
