from src.regression import executer_phase2, executer_regression
from src.classification import executer_phase3


def main():
    print("=== EXÉCUTION DU PROJET FITZONE ===")

    # Phase 2
    executer_phase2()
    executer_regression()

    # Phase 3
    executer_phase3()

    print("\n[OK] Exécution terminée.")


if __name__ == "__main__":
    main()