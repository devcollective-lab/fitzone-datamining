# Phase 1 - Analyse exploratoire des données FitZone
# Branche : junior_Bch
# Démarche du cours "Analyse exploratoire" : regarder les données avant de les modéliser
 
import pandas as pd
import matplotlib.pyplot as plt
 
# Afficher toutes les colonnes dans le terminal (sinon pandas coupe avec "...")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
 
abonnes = pd.read_csv("data/raw/FitZone_abonnes.csv")
salles = pd.read_csv("data/raw/FitZone_salles.csv")
 
# ------------------------------------------------------------
# 1. Ce qu'on a : structure des fichiers
# ------------------------------------------------------------
print("===== 1. STRUCTURE =====")
print("Abonnés :", abonnes.shape)
print("Salles  :", salles.shape)
print(abonnes.head())
print(abonnes.dtypes)
 
# ------------------------------------------------------------
# 2. Qualité : manquants, doublons, valeurs impossibles
# ------------------------------------------------------------
print("\n===== 2. QUALITÉ DES DONNÉES =====")
print("Valeurs manquantes :")
print(abonnes.isnull().sum())
 
print("\nLignes en double :", abonnes.duplicated().sum())
print("Identifiants en double :", abonnes["abonne_id"].duplicated().sum())
 
print("\nAnciennetés négatives :", (abonnes["anciennete_mois"] < 0).sum())
print("Prix à 0 € :", (abonnes["prix_mensuel_eur"] == 0).sum())
 
print("\nSalles : manquants =", salles.isnull().sum().sum(),
      "/ doublons =", salles.duplicated().sum())
 
# On retire les doublons pour la suite de l'exploration
# (le fichier d'origine dans data/raw n'est pas modifié)
abonnes = abonnes.drop_duplicates()
print("\nAbonnés après retrait des doublons :", abonnes.shape)
 
# La cible : a_resilie (oui / non) -> 1 / 0
abonnes["cible"] = (abonnes["a_resilie"] == "oui").astype(int)
print("Taux de résiliation :", round(abonnes["cible"].mean() * 100, 1), "%")
 
# ------------------------------------------------------------
# 3. Les sept nombres d'une colonne
# ------------------------------------------------------------
print("\n===== 3. LES SEPT NOMBRES =====")
colonnes = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m",
            "visites_par_mois", "seances_coaching", "reclamations"]
print(abonnes[colonnes].describe().round(2))
 
# Moyenne et médiane éloignées = distribution asymétrique
print("\nMoyenne vs médiane :")
for col in colonnes:
    print(col, ": moyenne =", round(abonnes[col].mean(), 2),
          "/ médiane =", round(abonnes[col].median(), 2))
 
# ------------------------------------------------------------
# 4. Boîtes à moustaches et valeurs extrêmes
#    seuil = Q3 + 1,5 x (Q3 - Q1)
# ------------------------------------------------------------
print("\n===== 4. VALEURS EXTRÊMES =====")
for col in colonnes:
    q1 = abonnes[col].quantile(0.25)
    q3 = abonnes[col].quantile(0.75)
    seuil = q3 + 1.5 * (q3 - q1)
    nb = (abonnes[col] > seuil).sum()
    print(col, ": seuil =", round(seuil, 2), "/ au-delà :", nb)
 
abonnes[colonnes].plot(kind="box", subplots=True, layout=(2, 3), figsize=(12, 7))
plt.tight_layout()
plt.savefig("outputs/figures/boites_moustaches_junior.png")
plt.close()
 
# ------------------------------------------------------------
# 5. Comparer selon la cible : résiliés vs fidèles
# ------------------------------------------------------------
print("\n===== 5. COMPARAISON RÉSILIÉS / FIDÈLES =====")
print(abonnes.groupby("a_resilie")[colonnes].mean().round(2))
 
# ------------------------------------------------------------
# 6. Découper en tranches : taux de résiliation par groupe
# ------------------------------------------------------------
print("\n===== 6. TAUX DE RÉSILIATION PAR TRANCHE =====")
print("Par formule (%) :")
print((abonnes.groupby("formule")["cible"].mean() * 100).round(1))
 
print("\nPar créneau habituel (%) :")
print((abonnes.groupby("creneau_habituel")["cible"].mean() * 100).round(1))
 
abonnes["tranche_anciennete"] = pd.cut(abonnes["anciennete_mois"],
                                       bins=[0, 6, 12, 24, 48, 120])
print("\nPar ancienneté en mois (%) :")
print((abonnes.groupby("tranche_anciennete", observed=True)["cible"].mean() * 100).round(1))
 
print("\nPar nombre de réclamations (%) :")
print((abonnes.groupby("reclamations")["cible"].mean() * 100).round(1))
 
# ------------------------------------------------------------
# 7. Matrice de corrélation
# ------------------------------------------------------------
print("\n===== 7. MATRICE DE CORRÉLATION =====")
correlation = abonnes[colonnes + ["cible"]].corr().round(2)
print(correlation)
 
plt.figure(figsize=(8, 6))
plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(correlation)), correlation.columns, rotation=45, ha="right")
plt.yticks(range(len(correlation)), correlation.columns)
plt.title("Matrice de corrélation")
plt.tight_layout()
plt.savefig("outputs/figures/correlation_junior.png")
plt.close()
 
print("\nGraphiques enregistrés dans outputs/figures/")
 
# ------------------------------------------------------------
# 8. Relier les deux fichiers grâce à la colonne "salle"
# ------------------------------------------------------------
print("\n===== 8. FUSION ABONNÉS + SALLES =====")
fusion = abonnes.merge(salles, on="salle", how="left")
print("Dimensions après fusion :", fusion.shape)
print("Abonnés sans salle correspondante :", fusion["ville"].isnull().sum())
 
print("\nTaux de résiliation par salle (%) :")
print((fusion.groupby("ville")["cible"].mean() * 100).round(1).sort_values())
 
print("\nTaux de résiliation selon le parking (%) :")
print((fusion.groupby("parking")["cible"].mean() * 100).round(1))
 
print("\nCorrélation avec la cible :")
print(fusion[["nb_coachs", "surface_m2", "ouverte_depuis_mois", "cible"]].corr().round(2)["cible"])
 
# Question 2 : la distance, vérifiée par tranche (la corrélation ne voit que les droites)
fusion["tranche_distance"] = pd.cut(fusion["distance_domicile_m"],
                                    bins=[0, 1000, 2000, 3000, 5000, 8000, 20000])
print("\nTaux de résiliation par distance en mètres (%) :")
print((fusion.groupby("tranche_distance", observed=True)["cible"].mean() * 100).round(1))
 