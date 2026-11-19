import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.ensemble import IsolationForest

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 250)

NOMS_GROUPES = {
    0: "Les réguliers de proximité",
    1: "Les fidèles Premium",
    2: "Les insatisfaits",
    3: "Les éloignés",
}

def choisir_nombres_groupes(abonnes, colonnes):
    
    donnees_std = StandardScaler().fit_transform(abonnes[colonnes])
    
    for k in range(2, 9):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(donnees_std)
        silhouette = silhouette_score(donnees_std, kmeans.labels_)
        print(f"k = {k} : inertie {kmeans.inertia_:.0f}, silhouette {silhouette:.3f}")

def decrire_groupes(abonnes, colonnes, k):
    """Forme k groupes d'abonnés avec KMeans, affiche le profil moyen de chaque
    groupe et sa répartition par formule, puis renvoie une copie des abonnés
    avec une colonne 'groupe'."""
    donnees_std = StandardScaler().fit_transform(abonnes[colonnes])

    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(donnees_std)

    abonnes_groupes = abonnes.copy()
    abonnes_groupes["groupe"] = kmeans.labels_

    resume = abonnes_groupes.groupby("groupe")[colonnes + ["a_resilie"]].mean().round(2)
    resume["effectif"] = abonnes_groupes.groupby("groupe").size()

    print(f"--- Profil des groupes pour k = {k} ---")
    print(resume)

    print("\n--- Répartition des groupes par formule ---")
    print(pd.crosstab(abonnes_groupes["groupe"], abonnes_groupes["formule"]))

    return abonnes_groupes

def interet_economique(abonnes_groupes, noms=NOMS_GROUPES):
    """Calcule, pour chaque groupe d'abonnés, le chiffre d'affaires mensuel,
    le chiffre d'affaires perdu par les résiliations et leur part dans le total."""
    df = abonnes_groupes.copy()
    df["ca_perdu"] = df["prix_mensuel_eur"] * df["a_resilie"]

    tableau = df.groupby("groupe").agg(
        effectif=("prix_mensuel_eur", "size"),
        prix_moyen=("prix_mensuel_eur", "mean"),
        taux_resiliation=("a_resilie", "mean"),
        ca_mensuel=("prix_mensuel_eur", "sum"),
        ca_perdu=("ca_perdu", "sum"),
    )
    tableau["part_ca"] = tableau["ca_mensuel"] / tableau["ca_mensuel"].sum()
    tableau["part_pertes"] = tableau["ca_perdu"] / tableau["ca_perdu"].sum()
    tableau.index = tableau.index.map(noms)

    print(tableau.round(2))
    return tableau

def detecter_atypiques(abonnes, colonnes, part_atypiques=0.05):
    """Repère les abonnés atypiques avec une Isolation Forest, puis compare
    leur profil moyen à celui des autres abonnés. Renvoie une copie des abonnés
    avec une colonne 'atypique' (True / False)."""
    donnees_std = StandardScaler().fit_transform(abonnes[colonnes])

    modele = IsolationForest(contamination=part_atypiques, random_state=42)
    modele.fit(donnees_std)

    abonnes_atyp = abonnes.copy()
    abonnes_atyp["atypique"] = modele.predict(donnees_std) == -1

    profil = abonnes_atyp.groupby("atypique")[colonnes + ["a_resilie"]].mean().round(2)
    profil["effectif"] = abonnes_atyp.groupby("atypique").size()
    print("--- Profil des abonnés atypiques (True) et des autres (False) ---")
    print(profil)

    print("\n--- Répartition des atypiques par formule ---")
    print(abonnes_atyp[abonnes_atyp["atypique"]]["formule"].value_counts())

    return abonnes_atyp

def cout_atypiques(abonnes_atyp, cout_seance=25):
    """Estime la marge mensuelle des abonnés (prix - coût du coaching),
    en supposant le coaching inclus dans l'abonnement, et compare les
    atypiques aux autres abonnés."""
    df = abonnes_atyp.copy()
    df["marge"] = df["prix_mensuel_eur"] - df["seances_coaching"] * cout_seance

    bilan = df.groupby(["formule", "atypique"]).agg(
        effectif=("marge", "size"),
        prix_moyen=("prix_mensuel_eur", "mean"),
        coaching_moyen=("seances_coaching", "mean"),
        marge_moyenne=("marge", "mean"),
        marge_totale=("marge", "sum"),
    )
    print(f"--- Marge mensuelle (coût d'une séance : {cout_seance} €) ---")
    print(bilan.round(2))

    atypiques = df[df["atypique"]]
    seuil = atypiques["prix_mensuel_eur"].sum() / atypiques["seances_coaching"].sum()
    print(f"\nMarge totale des atypiques : {atypiques['marge'].sum():.0f} € par mois")
    print(f"Les atypiques deviennent déficitaires au-delà de {seuil:.2f} € par séance")
    return bilan