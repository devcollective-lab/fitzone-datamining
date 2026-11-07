import pandas as pd
import os

def nettoyer_donnees():
    print("===== PHASE 1 : NETTOYAGE ET PRÉPARATION DES DONNÉES =====")
    
    # 1. Chargement des données brutes
    abonnes = pd.read_csv("data/raw/FitZone_abonnes.csv")
    salles = pd.read_csv("data/raw/FitZone_salles.csv")
    print(f"Dimensions initiales abonnés : {abonnes.shape}")

    # 2. Retrait des doublons stricts
    abonnes = abonnes.drop_duplicates()
    print(f"Après suppression des doublons : {abonnes.shape}")

    # 3. Traitement des anciennetés négatives
    # Décision : suppression des lignes aberrantes (erreur de saisie système)
    nb_negatifs = (abonnes["anciennete_mois"] < 0).sum()
    abonnes = abonnes[abonnes["anciennete_mois"] >= 0]
    print(f"Lignes avec ancienneté négative supprimées : {nb_negatifs}")

    # 4. Traitement des prix à 0 €
    # Décision : remplacement par la médiane de la formule d'abonnement correspondante
    prix_medians = abonnes.groupby("formule")["prix_mensuel_eur"].transform("median")
    abonnes.loc[abonnes["prix_mensuel_eur"] == 0, "prix_mensuel_eur"] = prix_medians[abonnes["prix_mensuel_eur"] == 0]
    print("Prix à 0 € corrigés par la médiane de leur formule.")

    # 5. Création de la variable cible numérique (1 = résilié, 0 = fidèle)
    abonnes["cible"] = (abonnes["a_resilie"] == "oui").astype(int)

    # 6. Sauvegarde du fichier propre dans data/processed/
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/FitZone_abonnes_propre.csv"
    abonnes.to_csv(output_path, index=False)
    print(f"\nDonnées nettoyées enregistrées avec succès dans : {output_path}")
    print(f"Dimensions finales : {abonnes.shape}")

if __name__ == "__main__":
    nettoyer_donnees()