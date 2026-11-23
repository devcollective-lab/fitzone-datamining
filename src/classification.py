import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.data_loader import charger_donnees_propre


def executer_phase3():
    abonnes, salles = charger_donnees_propre()
    df = abonnes.merge(salles, on="salle", how="left")

    features = [
        "anciennete_mois",
        "prix_mensuel_eur",
        "distance_domicile_m",
        "visites_par_mois",
        "seances_coaching",
        "reclamations",
    ]
    X = df[features].fillna(0)
    y = df["cible"]

    # ---------------------------------------------------------
    # QUESTION 5 : Estimer le risque & cibler 80 abonnés sur 400
    # ---------------------------------------------------------
    modele_risque = LogisticRegression(max_iter=1000, random_state=42)
    modele_risque.fit(X, y)

    # Extraction d'une cohorte de 400 abonnés en fin d'engagement
    cohorte_400 = df.sample(n=min(400, len(df)), random_state=42).copy()
    X_cohorte = cohorte_400[features].fillna(0)
    cohorte_400["probabilite_depart"] = modele_risque.predict_proba(X_cohorte)[:, 1]

    # Tri décroissant par risque de résiliation
    cohorte_triee = cohorte_400.sort_values(by="probabilite_depart", ascending=False)

    # Sélection des 80 abonnés prioritaires
    top_80 = cohorte_triee.head(80).copy()

    # Sauvegarde de la liste exploitable pour les conseillers
    os.makedirs("outputs/results", exist_ok=True)
    top_80.to_csv("outputs/results/top_80_prioritaires.csv", index=False)

    print("--- Question 5 : Estimation du risque et Top 80 / 400 ---")
    print(f"Risque moyen de résiliation (cohorte 400) : {cohorte_400['probabilite_depart'].mean() * 100:.1f} %")
    print(f"Risque moyen de résiliation (Top 80)      : {top_80['probabilite_depart'].mean() * 100:.1f} %")
    print(f"Panier moyen mensuel du Top 80            : {top_80['prix_mensuel_eur'].mean():.2f} €")
    print("[OK] Liste des 80 prioritaires exportée : outputs/results/top_80_prioritaires.csv")

    # ---------------------------------------------------------
    # QUESTION 6 : Capacité d'appel (+80) et gains potentiels
    # ---------------------------------------------------------
    suivants_80 = cohorte_triee.iloc[80:160].copy()

    # Hypothèses métier explicites
    TAUX_RETENTION_APPEL = 0.25   # 25 % des abonnés contactés acceptent de rester
    DUREE_MOYENNE_SAUVEE = 6      # Prolongation moyenne de 6 mois suite à la rétention
    COUT_PAR_APPEL = 5.0          # Coût opérationnel par appel (conseiller + geste commercial)

    # Scénario A : Capacité actuelle (Top 80)
    departs_evites_top80 = top_80["probabilite_depart"].sum() * TAUX_RETENTION_APPEL
    ca_sauve_top80 = (top_80["probabilite_depart"] * top_80["prix_mensuel_eur"]).sum() * TAUX_RETENTION_APPEL * DUREE_MOYENNE_SAUVEE
    cout_top80 = 80 * COUT_PAR_APPEL
    gain_net_top80 = ca_sauve_top80 - cout_top80

    # Scénario B : Extension de capacité (+80 appels, rangs 81 à 160)
    departs_evites_suiv80 = suivants_80["probabilite_depart"].sum() * TAUX_RETENTION_APPEL
    ca_sauve_suiv80 = (suivants_80["probabilite_depart"] * suivants_80["prix_mensuel_eur"]).sum() * TAUX_RETENTION_APPEL * DUREE_MOYENNE_SAUVEE
    cout_suiv80 = 80 * COUT_PAR_APPEL
    gain_net_suiv80 = ca_sauve_suiv80 - cout_suiv80

    print("\n--- Question 6 : Capacité d'appel et gains potentiels ---")
    print(f"Hypothèses : Rétention = {TAUX_RETENTION_APPEL*100:.0f}% | Durée sauvée = {DUREE_MOYENNE_SAUVEE} mois | Coût/appel = {COUT_PAR_APPEL:.2f} €")
    print(f"Risque moyen (abonnés 81 à 160) : {suivants_80['probabilite_depart'].mean() * 100:.1f} %")
    print(f"1. Équipe actuelle (Top 80)   : ~{departs_evites_top80:.1f} départs évités | CA sauvé : {ca_sauve_top80:.2f} € | Gain net : {gain_net_top80:.2f} €")
    print(f"2. Extension (+80 appels)     : ~{departs_evites_suiv80:.1f} départs évités | CA sauvé : {ca_sauve_suiv80:.2f} € | Gain net additionnel : {gain_net_suiv80:.2f} €")


if __name__ == "__main__":
    executer_phase3()