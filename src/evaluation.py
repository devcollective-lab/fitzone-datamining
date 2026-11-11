import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.dummy import DummyRegressor


# Évaluer les prédictions d'un modèle de régression
def evaluer_regression(y_test, predictions):
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("MAE :", round(mae, 2))
    print("RMSE :", round(rmse, 2))
    print("R² :", round(r2, 3))


# Évaluer le modèle de référence basé sur la moyenne
def evaluer_reference(X_train, X_test, y_train, y_test):
    modele = DummyRegressor(strategy="mean")
    modele.fit(X_train, y_train)

    predictions = modele.predict(X_test)

    print("\n--- Modèle de référence ---")
    evaluer_regression(y_test, predictions)

    return predictions
