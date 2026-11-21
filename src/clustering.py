from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.ensemble import IsolationForest


COLONNES_NUMERIQUES = [
    "anciennete_mois",
    "prix_mensuel_eur",
    "distance_domicile_m",
    "visites_par_mois",
    "seances_coaching",
    "reclamations"
]

COUT_VISITE = 1
COUT_COACHING = 10


# Sélectionner et standardiser les variables de segmentation
def preparer_donnees_clustering(abonnes):
    X = abonnes[COLONNES_NUMERIQUES].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled


# Calculer l'inertie pour plusieurs nombres de clusters
def calculer_inerties(X_scaled):
    inerties = []

    for k in range(2, 11):
        modele = KMeans(n_clusters=k, random_state=42, n_init=10)
        modele.fit(X_scaled)

        inerties.append(modele.inertia_)

    return inerties


# Évaluer la qualité des clusters pour plusieurs valeurs de K
def calculer_silhouettes(X_scaled):
    scores = []

    for k in range(2, 11):
        modele = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = modele.fit_predict(X_scaled)

        score = silhouette_score(X_scaled, labels)
        scores.append(score)

    return scores


# Regrouper les abonnés avec K-Means
def creer_clusters(X_scaled, k):
    modele = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = modele.fit_predict(X_scaled)

    return clusters


# Calculer les revenus mensuels par cluster
def analyser_revenus_clusters(abonnes_clusters):
    revenus = abonnes_clusters.groupby("cluster")["prix_mensuel_eur"].agg(
        ["count", "sum", "mean"]
    )

    revenus.columns = [
        "nombre_abonnes",
        "revenu_mensuel_total",
        "revenu_mensuel_moyen"
    ]

    return revenus.round(2)


# Calculer l'utilisation mensuelle des services par cluster
def analyser_utilisation_clusters(abonnes_clusters):
    utilisation = abonnes_clusters.groupby("cluster")[
        ["visites_par_mois", "seances_coaching"]
    ].agg(["sum", "mean"])

    return utilisation.round(2)


# Estimer les coûts et les marges par cluster
def simuler_couts_clusters(abonnes_clusters):
    resultats = abonnes_clusters.groupby("cluster").agg(
        revenu=("prix_mensuel_eur", "sum"),
        visites=("visites_par_mois", "sum"),
        coaching=("seances_coaching", "sum")
    )

    resultats["cout_estime"] = (
        resultats["visites"] * COUT_VISITE
        + resultats["coaching"] * COUT_COACHING
    )

    resultats["marge_simulee"] = (
        resultats["revenu"] - resultats["cout_estime"]
    )

    return resultats.round(2)


# Identifier les abonnés atypiques
def detecter_anomalies(X_scaled):
    modele = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    anomalies = modele.fit_predict(X_scaled)

    return anomalies


# Comparer les caractéristiques des abonnés
def analyser_profils_anomalies(abonnes_anomalies):
    profils = abonnes_anomalies.groupby("anomalie")[
        COLONNES_NUMERIQUES
    ].mean()

    return profils.round(2)


# Comparer les marges simulées des abonnés
def analyser_rentabilite_anomalies(abonnes_anomalies):
    resultats = abonnes_anomalies.groupby("anomalie").agg(
        nombre_abonnes=("anomalie", "size"),
        revenu=("prix_mensuel_eur", "sum"),
        visites=("visites_par_mois", "sum"),
        coaching=("seances_coaching", "sum")
    )

    resultats["cout_estime"] = (
        resultats["visites"] * COUT_VISITE
        + resultats["coaching"] * COUT_COACHING
    )

    resultats["marge_simulee"] = (
        resultats["revenu"] - resultats["cout_estime"]
    )

    resultats["marge_par_abonne"] = (
        resultats["marge_simulee"] / resultats["nombre_abonnes"]
    )

    return resultats.round(2)


# Identifier les abonnés atypiques à marge négative
def analyser_marges_individuelles(abonnes_anomalies):
    atypiques = abonnes_anomalies[
        abonnes_anomalies["anomalie"] == -1
    ].copy()

    atypiques["cout_estime"] = (
        atypiques["visites_par_mois"] * COUT_VISITE
        + atypiques["seances_coaching"] * COUT_COACHING
    )

    atypiques["marge_simulee"] = (
        atypiques["prix_mensuel_eur"] - atypiques["cout_estime"]
    )

    return atypiques
