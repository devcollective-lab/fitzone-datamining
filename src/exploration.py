from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
import pandas as pd

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


def comparer_resilies(df, colonnes):
    """Compare les abonnés résiliés et non résiliés pour les colonnes spécifiées."""
    for colonne in colonnes:
        print(f"\n--- Comparaison pour la colonne '{colonne}' ---")
        print(df.groupby("a_resilie")[colonne].agg(['mean', 'median']))

def taux_resiliation_par(df, colonnes):
    """Calcule le taux de résiliation pour les colonnes spécifiées."""
    for colonne in colonnes:
        print(f"\n--- Taux de résiliation pour la colonne '{colonne}' ---")
        print(df.groupby(colonne)["a_resilie"].agg(['mean', 'count']).round(3))

def test_independance_chi2(df, colonne1, colonne2):
    """Effectue un test d'indépendance du chi2 entre deux colonnes catégorielles."""
    print(f"\n--- Test d'indépendance du chi2 entre '{colonne1}' et '{colonne2}' ---")
    tableau = pd.crosstab(df[colonne1], df[colonne2])
    print(tableau)
    
    chi2, p_value, ddl, attendus = chi2_contingency(tableau)
    print("p-value :", p_value)

    if p_value < 0.05: # type: ignore
        print(f"Il existe une dépendance significative entre '{colonne1}' et '{colonne2}' (p < 0.05).")
    else :
        print(f"Il n'existe pas une dépendance significative entre '{colonne1}' et '{colonne2}' (p >= 0.05).")

def test_mann_whitney(df, colonne):
    """
    Compare une colonne numérique entre abonnés résiliés et non résiliés
    avec un test de Mann-Whitney.

    Affiche la médiane de chaque groupe (sens de l'écart), la p-value
    (fiabilité de l'écart) et une conclusion au seuil de 0,05.
    """
    print(f"\n--- Test de Mann-Whitney pour la colonne '{colonne}' ---")

    restes = df[df["a_resilie"] == 0][colonne].dropna()
    resilies = df[df["a_resilie"] == 1][colonne].dropna()

    print(f"Médiane des non-résiliés : {restes.median()}")
    print(f"Médiane des résiliés     : {resilies.median()}")

    resultat = mannwhitneyu(restes, resilies)
    p_value = resultat.pvalue  # type: ignore
    print(f"p-value : {p_value:.2e}")

    if p_value < 0.05:
        print(f"Différence significative entre les deux groupes pour '{colonne}' (p < 0,05).")
    else:
        print(f"Aucune différence significative n'a été mise en évidence pour '{colonne}' (p >= 0,05).")

def creer_tranches_distance(df):
    """ Crée une nouvelle colonne 'tranche_distance' dans le DataFrame df """

    bins = [0, 1000, 2000, 3000, 4000, 6000, float('inf')]
    labels = ["< 1 km", "1-2 km", "2-3 km", "3-4 km", "4-6 km", "6 km et plus"]

    df['tranche_distance'] = pd.cut(
        df['distance_domicile_m'], 
        bins=bins, labels=labels, 
        right=False
        )
    return df

def test_kruskal(df, colonne_groupe, colonne_valeur):
    """ test de kruskal pour comparer les distributions d'une variable continue entre plusieurs groupes """
    print(f"\n--- Test de Kruskal-Wallis pour la colonne '{colonne_valeur}' par '{colonne_groupe}' ---")

    groupes = []

    for tranche in df[colonne_groupe].unique():
        groupes.append(df[df[colonne_groupe] == tranche][colonne_valeur].dropna())

    stat, p_value = kruskal(*groupes)
    print(f"Statistique : {stat:.4f}, p-value : {p_value:.4e}")

    if p_value < 0.05:
        print(f"Différence significative entre les groupes pour '{colonne_valeur}' (p < 0,05).")
    else:
        print(f"Aucune différence significative n'a été mise en évidence pour '{colonne_valeur}' (p >= 0,05).")
    
