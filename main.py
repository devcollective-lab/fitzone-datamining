from src.data_loader import load_data
from src.exploration import explorer_structure, verifier_anomalies, verifier_types_unites


def main():
    abonnes, salles = load_data()

    print("\n---- Structure des données ----")
    explorer_structure(abonnes, salles)

    print("\n---- Recherche des anomalies ----")
    verifier_anomalies(abonnes, salles)

    print("\n---- Types et unités ----")
    verifier_types_unites(abonnes, salles)


if __name__ == "__main__":
    main()