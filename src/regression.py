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



    import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def executer_regression():
    abonnes, salles = charger_donnees_propre()
    df = abonnes.merge(salles, on="salle", how="left")
    
    features = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m", "seances_coaching", "reclamations"]
    X = df[features].dropna()
    y = df.loc[X.index, "visites_par_mois"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modele = LinearRegression()
    modele.fit(X_train, y_train)
    
    y_pred = modele.predict(X_test)
    print(f"R² : {r2_score(y_test, y_pred):.3f}")
    print(f"RMSE : {np.sqrt(mean_squared_error(y_test, y_pred)):.3f}")

if __name__ == "__main__":
    executer_regression()