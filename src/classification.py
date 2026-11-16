import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Préparer les données pour la classification
def preparer_classification(abonnes):
    colonnes = [
        "anciennete_mois",
        "formule",
        "prix_mensuel_eur",
        "distance_domicile_m",
        "creneau_habituel",
        "visites_par_mois",
        "seances_coaching",
        "reclamations"
    ]

    X = abonnes[colonnes]
    y = abonnes["a_resilie"]

    X = pd.get_dummies(
        X,
        columns=["formule", "creneau_habituel"],
        dtype=int
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\n--- Préparation des données de classification ---")
    print("Données d'entraînement :", len(X_train))
    print("Données de test :", len(X_test))
    print("Répartition des résiliations :")
    print(y.value_counts(normalize=True).round(3))

    return X_train, X_test, y_train, y_test

# Entraîner la régression logistique
def entrainer_classification(X_train, y_train):
    modele = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )

    modele.fit(X_train, y_train)

    print("\n--- Entraînement de la régression logistique ---")
    print("Modèle entraîné avec succès.")

    return modele

# Prédire les résiliations des abonnés
def predire_resiliations(modele, X_test):
    return modele.predict(X_test)

# Estimer la probabilité de résiliation
def predire_probabilites_resiliation(modele, X_test):
    indice_oui = list(modele.classes_).index("oui")
    return modele.predict_proba(X_test)[:, indice_oui]

# Classer les abonnés selon leur risque de résiliation
def classer_abonnes(X_test, probabilites):
    classement = pd.DataFrame({
        "score_resiliation": probabilites
    }, index=X_test.index)

    classement = classement.sort_values(
        by="score_resiliation",
        ascending=False
    )

    return classement