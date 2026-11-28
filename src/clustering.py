import pandas as pd
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

COUT_SEANCE_COACHING = 25


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


# Associer les noms marketing aux caractéristiques des clusters
def identifier_profils_clusters(abonnes_clusters):
    caracteristiques = abonnes_clusters.groupby("cluster").agg(
        part_premium=("formule", lambda valeurs: (valeurs == "Premium").mean()),
        reclamations=("reclamations", "mean"),
        distance=("distance_domicile_m", "mean")
    )

    cluster_premium = caracteristiques["part_premium"].idxmax()
    restants = caracteristiques.drop(index=cluster_premium)

    cluster_insatisfaits = restants["reclamations"].idxmax()
    restants = restants.drop(index=cluster_insatisfaits)

    cluster_eloignes = restants["distance"].idxmax()
    cluster_reguliers = restants.drop(index=cluster_eloignes).index[0]

    return {
        cluster_reguliers: "Réguliers de proximité",
        cluster_premium: "Fidèles Premium",
        cluster_insatisfaits: "Insatisfaits",
        cluster_eloignes: "Éloignés"
    }


# Décrire les caractéristiques et la résiliation des clusters
def analyser_profils_clusters(abonnes_clusters):
    profils = abonnes_clusters.groupby("cluster")[COLONNES_NUMERIQUES].mean()
    profils["effectif"] = abonnes_clusters.groupby("cluster").size()
    profils["taux_resiliation"] = (
        abonnes_clusters.groupby("cluster")["a_resilie"]
        .apply(lambda valeurs: (valeurs == "oui").mean() * 100)
    )

    noms_profils = identifier_profils_clusters(abonnes_clusters)
    profils.insert(0, "profil", profils.index.map(noms_profils))

    return profils.round(2)


# Calculer la répartition des formules par profil
def analyser_formules_clusters(abonnes_clusters):
    repartition = pd.crosstab(
        abonnes_clusters["cluster"],
        abonnes_clusters["formule"],
        normalize="index"
    ) * 100

    noms_profils = identifier_profils_clusters(abonnes_clusters)
    repartition.index = repartition.index.map(noms_profils)
    repartition.index.name = "profil"

    return repartition.round(2)


# Calculer les indicateurs économiques par profil
def analyser_revenus_clusters(abonnes_clusters):
    donnees = abonnes_clusters.copy()
    donnees["est_resilie"] = donnees["a_resilie"] == "oui"
    donnees["ca_perdu"] = donnees["prix_mensuel_eur"].where(
        donnees["est_resilie"], 0
    )

    revenus = donnees.groupby("cluster").agg(
        effectif=("cluster", "size"),
        prix_mensuel_moyen=("prix_mensuel_eur", "mean"),
        nombre_resiliations=("est_resilie", "sum"),
        ca_mensuel_theorique=("prix_mensuel_eur", "sum"),
        ca_mensuel_perdu=("ca_perdu", "sum")
    )

    revenus["taux_resiliation"] = (
        revenus["nombre_resiliations"] / revenus["effectif"] * 100
    )
    revenus["part_ca"] = (
        revenus["ca_mensuel_theorique"]
        / revenus["ca_mensuel_theorique"].sum()
        * 100
    )
    revenus["part_pertes"] = (
        revenus["ca_mensuel_perdu"]
        / revenus["ca_mensuel_perdu"].sum()
        * 100
    )

    revenus = revenus.drop(columns="nombre_resiliations")
    revenus = revenus[[
        "effectif",
        "prix_mensuel_moyen",
        "taux_resiliation",
        "ca_mensuel_theorique",
        "part_ca",
        "ca_mensuel_perdu",
        "part_pertes"
    ]]

    noms_profils = identifier_profils_clusters(abonnes_clusters)
    revenus.index = revenus.index.map(noms_profils)
    revenus.index.name = "profil"

    return revenus.round(2)


# Calculer l'utilisation mensuelle des services par profil
def analyser_utilisation_clusters(abonnes_clusters):
    utilisation = abonnes_clusters.groupby("cluster")[[
        "visites_par_mois",
        "seances_coaching"
    ]].agg(["sum", "mean"])

    noms_profils = identifier_profils_clusters(abonnes_clusters)
    utilisation.index = utilisation.index.map(noms_profils)
    utilisation.index.name = "profil"

    return utilisation.round(2)


# Identifier les abonnés atypiques
def detecter_anomalies(X_scaled):
    modele = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    anomalies = modele.fit_predict(X_scaled)

    return anomalies


# Comparer les caractéristiques des abonnés atypiques et des autres abonnés
def analyser_profils_anomalies(abonnes_anomalies):
    profils = abonnes_anomalies.groupby("anomalie")[
        COLONNES_NUMERIQUES
    ].mean()
    profils["effectif"] = abonnes_anomalies.groupby("anomalie").size()
    profils["taux_resiliation"] = (
        abonnes_anomalies.groupby("anomalie")["a_resilie"]
        .apply(lambda valeurs: (valeurs == "oui").mean() * 100)
    )

    profils.index = profils.index.map({-1: "Atypiques", 1: "Autres"})
    profils.index.name = "profil"

    return profils.round(2)


# Comparer les formules des abonnés atypiques et des autres abonnés
def analyser_formules_anomalies(abonnes_anomalies):
    formules = pd.crosstab(
        abonnes_anomalies["anomalie"],
        abonnes_anomalies["formule"]
    )

    formules.index = formules.index.map({-1: "Atypiques", 1: "Autres"})
    formules.index.name = "profil"

    return formules


# Comparer les abonnés Premium atypiques aux autres Premium
def analyser_premium_anomalies(abonnes_anomalies):
    premium = abonnes_anomalies[
        abonnes_anomalies["formule"] == "Premium"
    ]

    profils = premium.groupby("anomalie")[COLONNES_NUMERIQUES].mean()
    profils["effectif"] = premium.groupby("anomalie").size()
    profils["taux_resiliation"] = (
        premium.groupby("anomalie")["a_resilie"]
        .apply(lambda valeurs: (valeurs == "oui").mean() * 100)
    )

    profils.index = profils.index.map({-1: "Atypiques", 1: "Autres"})
    profils.index.name = "Premium"

    return profils.round(2)


# Simuler la marge partielle des abonnés Premium
def analyser_rentabilite_anomalies(
    abonnes_anomalies,
    cout_seance=COUT_SEANCE_COACHING
):
    premium = abonnes_anomalies[
        abonnes_anomalies["formule"] == "Premium"
    ].copy()

    premium["marge_simulee"] = (
        premium["prix_mensuel_eur"]
        - premium["seances_coaching"] * cout_seance
    )

    resultats = premium.groupby("anomalie").agg(
        effectif=("anomalie", "size"),
        prix_moyen=("prix_mensuel_eur", "mean"),
        coaching_moyen=("seances_coaching", "mean"),
        marge_moyenne_simulee=("marge_simulee", "mean"),
        marge_totale_simulee=("marge_simulee", "sum")
    )

    resultats.index = resultats.index.map({-1: "Atypiques", 1: "Autres"})
    resultats.index.name = "Premium"

    return resultats.round(2)


# Simuler le scénario élargi à tous les abonnés atypiques
def simuler_scenario_atypiques(
    abonnes_anomalies,
    cout_seance=COUT_SEANCE_COACHING
):
    atypiques = abonnes_anomalies[
        abonnes_anomalies["anomalie"] == -1
    ].copy()

    atypiques["marge_simulee"] = (
        atypiques["prix_mensuel_eur"]
        - atypiques["seances_coaching"] * cout_seance
    )

    seuil_equilibre = (
        atypiques["prix_mensuel_eur"].sum()
        / atypiques["seances_coaching"].sum()
    )

    return pd.Series({
        "effectif": len(atypiques),
        "marge_totale_simulee": atypiques["marge_simulee"].sum(),
        "seuil_equilibre_cout_seance": seuil_equilibre
    }).round(2)
