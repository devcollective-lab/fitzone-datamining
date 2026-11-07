from src.data_loader import load_data
from src.exploration import explorer_structure, verifier_anomalies, verifier_types_unites
from src.preprocessing import (
    supprimer_doublons,
    traiter_coaching_manquant,
    traiter_creneau_manquant,
    corriger_anciennetes,
    corriger_prix
)


# Exécuter les différentes étapes du projet
def main():
    abonnes, salles = load_data()

    print("\n--- Structure des données ---")
    explorer_structure(abonnes, salles)

    print("\n--- Recherche des anomalies ---")
    verifier_anomalies(abonnes, salles)

    print("\n--- Types et unités ---")
    verifier_types_unites(abonnes, salles)

    print("\n--- Nettoyage des données ---")

    abonnes = supprimer_doublons(abonnes)
    abonnes = traiter_coaching_manquant(abonnes)
    abonnes = traiter_creneau_manquant(abonnes)
    abonnes = corriger_anciennetes(abonnes)
    abonnes = corriger_prix(abonnes)

    print("\n--- Vérification finale des abonnés ---")

    print("Dimensions :", abonnes.shape)
    print("Doublons :", abonnes.duplicated().sum())

    print("Valeurs manquantes :")
    print(abonnes.isna().sum())

    print("Anciennetés négatives :", (abonnes["anciennete_mois"] < 0).sum())
    print("Prix mensuels nuls :", (abonnes["prix_mensuel_eur"] == 0).sum())

    abonnes.to_csv("data/processed/FitZone_abonnes_clean.csv", index=False)
    salles.to_csv("data/processed/FitZone_salles_clean.csv", index=False)

    print("\n--- Sauvegarde des données nettoyées ---")
    print("Fichiers enregistrés dans data/processed/")


if __name__ == "__main__":
    main()