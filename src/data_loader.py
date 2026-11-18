import pandas as pd

def charger_donnees_brutes():
    abonnes = pd.read_csv("data/raw/FitZone_abonnes.csv")
    salles = pd.read_csv("data/raw/FitZone_salles.csv")
    return abonnes, salles

def charger_donnees_propre():
    abonnes_propre = pd.read_csv("data/processed/FitZone_abonnes_propre.csv")
    salles = pd.read_csv("data/raw/FitZone_salles.csv")
    return abonnes_propre, salles