
# comprendre les datasets
def explorer_structure(abonnes, salles):
    print("Dimensions des abonnés :", abonnes.shape)
    print("Dimensions des salles :", salles.shape)

    print("\n--- Aperçu des abonnés ---")
    print(abonnes.head())

    print("\n--- Aperçu des salles ---")
    print(salles.head())

    print("\n--- Colonnes des abonnés ---")
    print(abonnes.columns.tolist())

    print("\n--- Colonnes des salles ---")
    print(salles.columns.tolist())

    print("\n--- Informations sur les abonnés ---")
    abonnes.info()

    print("\n--- Informations sur les salles ---")
    salles.info()

# Valeurs manquantes, doublons et incohérences
def verifier_anomalies(abonnes, salles):
    print("\n--- Valeurs manquantes des abonnés ---")
    print(abonnes.isna().sum())

    print("\n--- Valeurs manquantes des salles ---")
    print(salles.isna().sum())

    print("\n--- Doublons des abonnés ---")
    print(abonnes.duplicated().sum())

    print("\n--- Doublons des salles ---")
    print(salles.duplicated().sum())

    print("\n--- Identifiants d'abonnés dupliqués ---")
    print(abonnes["abonne_id"].duplicated().sum())

    print("\n--- Statistiques descriptives des abonnés ---")
    print(abonnes.describe())

    print("\n--- Abonnés avec une ancienneté négative ---")
    print(abonnes[abonnes["anciennete_mois"] < 0])

    print("\n--- Abonnés avec un prix mensuel nul ---")
    print(abonnes[abonnes["prix_mensuel_eur"] == 0])

    print("\n--- Statistiques des distances ---")
    print(abonnes["distance_domicile_m"].describe())

    print("\n--- Abonnés habitant à plus de 10 km ---")
    print(abonnes[abonnes["distance_domicile_m"] > 10000])

    print("\n--- Statistiques des visites mensuelles ---")
    print(abonnes["visites_par_mois"].describe())

    print("\n--- Statistiques des séances de coaching ---")
    print(abonnes["seances_coaching"].describe())

    print("\n--- Répartition des réclamations ---")
    print(abonnes["reclamations"].value_counts().sort_index())

    print("\n--- Répartition des formules ---")
    print(abonnes["formule"].value_counts(dropna=False))

    print("\n--- Répartition des créneaux habituels ---")
    print(abonnes["creneau_habituel"].value_counts(dropna=False))

    print("\n--- Répartition des résiliations ---")
    print(abonnes["a_resilie"].value_counts(dropna=False))

    print("\n--- Répartition des villes ---")
    print(salles["ville"].value_counts(dropna=False))

    print("\n--- Répartition des parkings ---")
    print(salles["parking"].value_counts(dropna=False))

    print("\n--- Salles inconnues dans les abonnés ---")
    print(abonnes[~abonnes["salle"].isin(salles["salle"])])

    print("\n--- Statistiques descriptives des salles ---")
    print(salles.describe())


# Les types de données et les unités
def verifier_types_unites(abonnes, salles):
    print("\n--- Types des colonnes des abonnés ---")
    print(abonnes.dtypes)

    print("\n--- Types des colonnes des salles ---")
    print(salles.dtypes)

    print("\n--- Valeurs décimales dans les colonnes de comptage ---")
    colonnes = ["anciennete_mois", "visites_par_mois", "seances_coaching"]

    for colonne in colonnes:
        valeurs = abonnes[colonne].dropna()
        decimales = valeurs[valeurs % 1 != 0]

        print(colonne, ":", len(decimales), "valeur(s) décimale(s)")

    distances_km = abonnes["distance_domicile_m"] / 1000

    print("\n--- Distances exprimées en kilomètres ---")
    print(distances_km.describe())


# Analyser les résiliations selon les formules et les créneaux
def analyser_resiliations(abonnes):
    print("\n--- Analyse des résiliations ---")

    total = len(abonnes)
    resilies = abonnes[abonnes["a_resilie"] == "oui"]

    taux = len(resilies) / total * 100

    print("\n--- Taux global de résiliation ---")
    print("Nombre d'abonnés :", total)
    print("Nombre de résiliations :", len(resilies))
    print("Taux de résiliation :", round(taux, 2), "%")

    print("\n--- Résiliations par formule ---")

    for formule in abonnes["formule"].unique():
        groupe = abonnes[abonnes["formule"] == formule]
        nb_resilies = (groupe["a_resilie"] == "oui").sum()
        taux = nb_resilies / len(groupe) * 100

        print(formule, ":", round(taux, 2), "%")

    print("\n--- Résiliations par créneau habituel ---")

    for creneau in abonnes["creneau_habituel"].unique():
        groupe = abonnes[abonnes["creneau_habituel"] == creneau]
        nb_resilies = (groupe["a_resilie"] == "oui").sum()
        taux = nb_resilies / len(groupe) * 100

        print(creneau, ":", round(taux, 2), "%")


    # Comparer les prix mensuels selon la résiliation
    print("\n--- Prix mensuel moyen selon la résiliation ---")

    prix_resilies = abonnes[abonnes["a_resilie"] == "oui"]["prix_mensuel_eur"].mean()
    prix_non_resilies = abonnes[abonnes["a_resilie"] == "non"]["prix_mensuel_eur"].mean()

    print("Prix moyen des abonnés résiliés :", round(prix_resilies, 2), "€")
    print("Prix moyen des abonnés non résiliés :", round(prix_non_resilies, 2), "€")

# Analyser le lien entre la distance et la résiliation
def analyser_distance(abonnes):
    print("\n--- Distance et résiliation ---")

    resilies = abonnes[abonnes["a_resilie"] == "oui"]
    non_resilies = abonnes[abonnes["a_resilie"] == "non"]

    distance_resilies = resilies["distance_domicile_m"].mean() / 1000
    distance_non_resilies = non_resilies["distance_domicile_m"].mean() / 1000

    print("\n--- Distance moyenne selon la résiliation ---")
    print("Abonnés résiliés :", round(distance_resilies, 2), "km")
    print("Abonnés non résiliés :", round(distance_non_resilies, 2), "km")

    print("\n--- Taux de résiliation par distance ---")

    tranches = [
        (0, 2000),
        (2000, 5000),
        (5000, 10000),
        (10000, float("inf"))
    ]

    for minimum, maximum in tranches:
        groupe = abonnes[
            (abonnes["distance_domicile_m"] >= minimum) &
            (abonnes["distance_domicile_m"] < maximum)
        ]

        if len(groupe) > 0:
            nb_resilies = (groupe["a_resilie"] == "oui").sum()
            taux = nb_resilies / len(groupe) * 100

            if maximum == float("inf"):
                distance = f"{minimum / 1000} km et plus"
            else:
                distance = f"{minimum / 1000} à {maximum / 1000} km"

            print(
                distance, ":",
                len(groupe), "abonnés,",
                round(taux, 2), "% de résiliation"
            )
