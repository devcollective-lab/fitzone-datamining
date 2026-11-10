import pandas as pd
from pathlib import Path

from src.data_loader import load_abonnes, load_salles
from src.exploration import apercu
from src.preprocessing import ( supprimer_doublons,
                                remplir_creneau,
                                remplir_coaching,
                                corriger_prix,
                                supprimer_anciennete_negative,
                                convertir_oui_non,
                                sauvegarde,
                            )

pd.set_option("display.max_columns", None)  # pour voir toutes les colonnes
pd.set_option("display.width", 250)


def main():
    # Charger les données
    abonnes_df = load_abonnes()
    salles_df = load_salles()


    # Suppression des doublons et remplissage des créneaux manquants

    print(f"Shape des abonnés avant suppression des doublons : {abonnes_df.shape}")
    abonnes = supprimer_doublons(abonnes_df)
    print(f"Shape des abonnés après suppression des doublons : {abonnes.shape}\n")

    #Remplir les cases vides des crénaux abonnés par "inconnu"
    abonnes = remplir_creneau(abonnes)

    #Remplir les cases vides des séances de coaching par les médianes de chaque groupe (essentiel, confort, premium)
    abonnes = remplir_coaching(abonnes)

    #Remplacer les prix à 0 € par la médiane de la formule
    abonnes = corriger_prix(abonnes)

    # Supprimer les abonnés avec une ancienneté négative
    abonnes = supprimer_anciennete_negative(abonnes)

    # Convertir les colonnes 'oui'/'non' en 1/0
    abonnes = convertir_oui_non(abonnes, "a_resilie")
    salles = convertir_oui_non(salles_df, "parking")

    # Sauvegarder les DataFrames nettoyés
    sauvegarde(abonnes, salles)

if __name__ == "__main__":
    main()