import pandas as pd
from src.data_loader import charger_donnees_propre

def executer_phase2():
    abonnes, salles = charger_donnees_propre()
    df = abonnes.merge(salles, on="salle", how="left")
    
    print("--- Question 1 : Facteurs de résiliation ---")
    cols_num = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m", "visites_par_mois", "seances_coaching", "reclamations"]
    print(df.groupby("a_resilie")[cols_num].mean().round(2))
    
    print("\n--- Question 2 : Influence de la distance ---")
    df["tranche_distance"] = pd.cut(df["distance_domicile_m"], bins=[0, 1000, 2000, 3000, 5000, 8000, 20000])
    print((df.groupby("tranche_distance", observed=True)["cible"].mean() * 100).round(1))

if __name__ == "__main__":
    executer_phase2()