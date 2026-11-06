import pandas as pd


def load_data():
    abonnes = pd.read_csv("data/raw/FitZone_abonnes.csv")
    salles = pd.read_csv("data/raw/FitZone_salles.csv")

    return abonnes, salles
