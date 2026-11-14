from src.data_loader import charger_donnees_propre

def main():
    abonnes, salles = charger_donnees_propre()
    print(f"[OK] Données chargées : {abonnes.shape[0]} abonnés, {salles.shape[0]} salles.")

if __name__ == "__main__":
    main()