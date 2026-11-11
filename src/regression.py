import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


# Préparer les données pour la régression
def preparer_regression(abonnes):
    colonnes = [
        "anciennete_mois",
        "formule",
        "prix_mensuel_eur",
        "distance_domicile_m",
        "creneau_habituel",
        "seances_coaching",
        "reclamations"
    ]

    X = abonnes[colonnes]
    y = abonnes["visites_par_mois"]

    X = pd.get_dummies(
        X,
        columns=["formule", "creneau_habituel"],
        dtype=int
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


# Entraîner la régression linéaire
def entrainer_regression(X_train, y_train):
    modele = LinearRegression()
    modele.fit(X_train, y_train)

    print("\n--- Entraînement de la régression linéaire ---")
    print("Modèle entraîné avec succès.")

    return modele


# Prédire les visites mensuelles
def predire_visites(modele, X_test):
    return modele.predict(X_test)


# Afficher les coefficients de la régression linéaire
def analyser_coefficients(modele, X_train):
    coefficients = pd.Series(modele.coef_, index=X_train.columns)

    print("\n--- Coefficients de la régression ---")
    print(coefficients.sort_values(ascending=False))


# Entraîner un Random Forest
def entrainer_random_forest(X_train, y_train):
    modele = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    modele.fit(X_train, y_train)

    print("\n--- Entraînement du Random Forest ---")
    print("Modèle entraîné avec succès.")

    return modele


# Optimiser le Random Forest par validation croisée
def optimiser_random_forest(X_train, y_train):
    modele = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    parametres = {
        "max_depth": [5, 10, 15],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
    }

    recherche = GridSearchCV(
        estimator=modele,
        param_grid=parametres,
        cv=5,
        scoring="neg_mean_absolute_error",
        n_jobs=-1
    )

    recherche.fit(X_train, y_train)

    print("\n--- Optimisation du Random Forest ---")
    print("Meilleurs paramètres :", recherche.best_params_)
    print("Meilleure MAE en validation :", round(-recherche.best_score_, 2))

    return recherche.best_estimator_
