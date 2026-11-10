from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

ABONNES_PATH = ROOT / "data" / "raw" / "FitZone_abonnes.csv"
SALLES_PATH = ROOT / "data" / "raw" / "FitZone_salles.csv"

def load_abonnes():
    """
    Load the abonnes data from the CSV file into a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the abonnes data.
    """
    return pd.read_csv(ABONNES_PATH)

def load_salles():
    """
    Load the salles data from the CSV file into a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the salles data.
    """
    return pd.read_csv(SALLES_PATH)