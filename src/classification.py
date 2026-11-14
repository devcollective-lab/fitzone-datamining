import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.data_loader import charger_donnees_propre

def executer_classification():
    abonnes, salles = charger_donnees_propre()
    df = abonnes.merge(salles, on="salle", how="left")
    
    features = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m", "visites_par_mois", "seances_coaching", "reclamations"]
    X = df[features].fillna(0)
    y = df["cible"]
    
    model_risk = LogisticRegression(max_iter=1000, random_state=42)
    model_risk.fit(X, y)
    
    fin_engagement = df.sample(n=min(400, len(df)), random_state=42).copy()
    fin_engagement["probabilite_depart"] = model_risk.predict_proba(fin_engagement[features])[:, 1]
    
    top_80 = fin_engagement.sort_values(by="probabilite_depart", ascending=False).head(80)
    print(f"Probabilité moyenne Top 80 : {top_80['probabilite_depart'].mean() * 100:.1f} %")

if __name__ == "__main__":
    executer_classification()


    def executer_simulation():
    abonnes, salles = charger_donnees_propre()
    df = abonnes.merge(salles, on="salle", how="left")
    features = ["anciennete_mois", "prix_mensuel_eur", "distance_domicile_m", "visites_par_mois", "seances_coaching", "reclamations"]
    X = df[features].fillna(0)
    y = df["cible"]
    
    model_risk = LogisticRegression(max_iter=1000, random_state=42)
    model_risk.fit(X, y)
    
    fin_engagement = df.sample(n=min(400, len(df)), random_state=42).copy()
    fin_engagement["probabilite_depart"] = model_risk.predict_proba(fin_engagement[features])[:, 1]
    
    top_160 = fin_engagement.sort_values(by="probabilite_depart", ascending=False).head(160)
    suivants_80 = top_160.iloc[80:160]
    print(f"Risque moyen abonnés 81 à 160 : {suivants_80['probabilite_depart'].mean() * 100:.1f} %")