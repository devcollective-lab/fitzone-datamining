import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABONNES_CLEAN_PATH = ROOT / "data" / "processed" / "abonnes_clean.csv"
SALLES_CLEAN_PATH = ROOT / "data" / "processed" / "salles_clean.csv"

def supprimer_doublons(df):
    """Supprime les lignes entièrement identiques (copies exactes)."""
    nb_avant = len(df)
    df = df.drop_duplicates()
    nb_apres = len(df)
    print(f"Doublons supprimés : {nb_avant - nb_apres}")
    return df

def remplir_creneau(df):
    """Remplace les créneaux manquants par la catégorie 'inconnu'."""
    nb_manquants = df["creneau_habituel"].isna().sum()
    df["creneau_habituel"] = df["creneau_habituel"].fillna("inconnu")
    print(f"Créneaux manquants remplacés par 'inconnu' : {nb_manquants}")
    return df

def remplir_coaching(df):
    """Remplace les séances de coaching manquantes par la médiane de la formule."""
    nb_manquants = df["seances_coaching"].isna().sum()
    mediane_par_formule = df.groupby("formule")["seances_coaching"].transform("median")
    df["seances_coaching"] = df["seances_coaching"].fillna(mediane_par_formule)
    print(f"Séances de coaching manquantes remplacées par la médiane de la formule : {nb_manquants}")
    return df

def corriger_prix(df):
    """Remplace les prix à 0 € (erreurs d'enregistrement) par la médiane du prix de la formule."""
    nb_corriges = (df["prix_mensuel_eur"] == 0).sum()
    df["prix_mensuel_eur"] = df["prix_mensuel_eur"].replace(0, np.nan)
    mediane_par_formule = df.groupby("formule")["prix_mensuel_eur"].transform("median")
    df["prix_mensuel_eur"] = df["prix_mensuel_eur"].fillna(mediane_par_formule)
    print(f"Prix à 0 € remplacés par la médiane de la formule : {nb_corriges}")
    return df


def supprimer_anciennete_negative(df):
    """Supprime les abonnés dont l'ancienneté vaut -1 (valeur inconnue, codée -1)."""
    nb_avant = len(df)
    df = df[df["anciennete_mois"] >= 0]
    print(f"Abonnés supprimés (ancienneté négative) : {nb_avant - len(df)}")
    return df

def convertir_oui_non(df, colonne):
    """Convertit une colonne 'oui'/'non' en 1/0."""
    df[colonne] = df[colonne].map({"oui": 1, "non": 0})
    nb_problemes = df[colonne].isna().sum()
    print(f"Colonne '{colonne}' convertie en 1/0 (valeurs non reconnues : {nb_problemes})")
    return df


def sauvegarde(df_abonnes, df_salles):
    # Sauvegarder les DataFrames nettoyés

    ABONNES_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SALLES_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_abonnes.to_csv(ABONNES_CLEAN_PATH, index=False)
    df_salles.to_csv(SALLES_CLEAN_PATH, index=False)

    print(f"Nombre de lignes sauvegardées pour les abonnés : {len(df_abonnes)}")
    print(f"Nombre de lignes sauvegardées pour les salles : {len(df_salles)}")