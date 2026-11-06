
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
