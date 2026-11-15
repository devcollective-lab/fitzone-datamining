import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

def preparer_donnees_regression(df, colonnes):
    """Prépare les données pour la régression en encodant les variables catégorielles et en séparant les variables
    indépendantes (X) de la variable dépendante (y)."""

    df_encode = pd.get_dummies(df, columns=colonnes, drop_first=True, dtype=int)
    y = df_encode["visites_par_mois"]
    X = df_encode.drop(columns=["abonne_id", "visites_par_mois", "a_resilie", "tranche_distance", "reclamations_groupe"],
    errors="ignore")

    return X, y

def decouper_donnees(X, y, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=random_state
    )

    return X_train, X_test, y_train, y_test

def evaluer_baseline(y_train, y_test):
    """Évalue le modèle de référence : prédit la médiane de y_train pour tous
    les abonnés du test, et renvoie l'erreur absolue moyenne (MAE)."""
    prediction = y_train.median()
    mae = (y_test - prediction).abs().mean()
    print(f"Baseline (prédiction : {prediction}) - MAE : {mae:.2f}")
    return mae


def evaluer_modele(modele, X, y, nom_jeu):
    """Évalue un modèle entraîné sur un jeu de données (entraînement ou test)
    et renvoie l'erreur absolue moyenne (MAE)."""
    predictions = modele.predict(X)
    mae = (y - predictions).abs().mean()
    r2 = r2_score(y, predictions)
    print(f"MAE sur {nom_jeu} : {mae:.2f}\nR2 score : {r2:.2f}")
    return mae, r2


def entrainer_regression_lineaire(X_train, y_train):
    """Crée et entraîne une régression linéaire, puis renvoie le modèle entraîné."""
    modele = LinearRegression()
    modele.fit(X_train, y_train)
    return modele

def validation_croisee(X, y):
    """Effectue une validation croisée sur les données et renvoie les scores R2 pour chaque pli."""
    decoupage = KFold(n_splits=5, shuffle=True, random_state=42)

    scores_r2 = cross_val_score(LinearRegression(), X, y, cv=decoupage, scoring="r2")
    scores_mae = -cross_val_score(LinearRegression(), X, y, cv=decoupage,
                              scoring="neg_mean_absolute_error")
    print("\n--- Validation croisée ---")
    print(f"Scores R2 pour chaque pli : {scores_r2.round(2)}")
    print(f"Moyenne: {scores_r2.mean():.2f}, écart-type: {scores_r2.std():.2f}")
    print(f"Scores MAE pour chaque pli : {scores_mae.round(2)}")
    print(f"Moyenne: {scores_mae.mean():.2f}, écart-type: {scores_mae.std():.2f}")

    return scores_r2, scores_mae

def coefficients_standardises(X, y, colonnes_numeriques):
    """ Calcule et affiche les coefficients standardisés d'une régression linéaire."""
    X_std = X.copy()
    X_std[colonnes_numeriques] = StandardScaler().fit_transform(X[colonnes_numeriques])

    modele_std = LinearRegression()
    modele_std.fit(X_std, y)

    coefficients_std = pd.Series(modele_std.coef_, index=X_std.columns)
    print(coefficients_std[colonnes_numeriques].sort_values())