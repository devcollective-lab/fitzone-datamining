import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

ABONNES_CLEAN = ROOT / "data" / "processed" / "FitZone_abonnes_clean.csv"
SALLES_CLEAN = ROOT / "data" / "processed" / "FitZone_salles_clean.csv"

def load_data():
    abonnes = pd.read_csv("data/raw/FitZone_abonnes.csv")
    salles = pd.read_csv("data/raw/FitZone_salles.csv")

    return abonnes, salles

def load_data_clean():
    """ Charge les données nettoyées à partir des fichiers CSV dans le dossier data/processed."""
    abonnes = pd.read_csv(ABONNES_CLEAN)
    salles = pd.read_csv(SALLES_CLEAN)

    return abonnes, salles