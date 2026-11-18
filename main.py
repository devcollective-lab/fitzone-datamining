from src.data_loader import charger_donnees_propre

def main():
    abonnes, salles = charger_donnees_propre()
    print(f"[OK] Données chargées : {abonnes.shape[0]} abonnés, {salles.shape[0]} salles.")

if __name__ == "__main__":
    main()

    from src.regression import executer_phase2, executer_regression
from src.classification import executer_classification, executer_simulation

def main():
    print("=== EXÉCUTION DU PROJET FITZONE ===")
    
    # Phase 2
    executer_phase2()
    executer_regression()
    
    # Phase 3
    executer_classification()
    executer_simulation()
    
    print("\n[OK] Analyse terminée avec succès.")

if __name__ == "__main__":
    main()