import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    classification_report,
    confusion_matrix
)
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


# Évaluer les prédictions de classification
def evaluer_classification(y_test, predictions):
    print("\n--- Évaluation de la classification ---")
    print(classification_report(y_test, predictions, zero_division=0))

    print("\n--- Matrice de confusion ---")
    print(confusion_matrix(y_test, predictions, labels=["non", "oui"]))


# Évaluer les abonnés prioritaires
def evaluer_priorites(classement, y_test, nombre=20):
    prioritaires = classement.head(nombre)

    resiliations = y_test.loc[prioritaires.index].eq("oui").sum()
    precision = resiliations / len(prioritaires)

    print("\n--- Évaluation des abonnés prioritaires ---")
    print("Abonnés sélectionnés :", len(prioritaires))
    print("Résiliations réelles :", resiliations)
    print("Précision :", round(precision * 100, 2), "%")

    return resiliations


# Estimer le gain des appels supplémentaires
def simuler_appels(resiliations_actuelles, resiliations_doublees):
    taux_fidelisation = 0.30
    revenu_mensuel = 35
    cout_appel = 2

    appels_actuels = 32
    appels_doubles = 64

    abonnes_conserves = (resiliations_doublees - resiliations_actuelles) * taux_fidelisation
    revenus_supplementaires = abonnes_conserves * revenu_mensuel
    cout_supplementaire = (appels_doubles - appels_actuels) * cout_appel
    gain_net = revenus_supplementaires - cout_supplementaire

    print("\n--- Simulation des appels supplémentaires ---")
    print("Abonnés conservés estimés :", round(abonnes_conserves, 2))
    print("Revenus mensuels supplémentaires :", round(revenus_supplementaires, 2), "€")
    print("Coût des appels supplémentaires :", cout_supplementaire, "€")
    print("Gain net estimé :", round(gain_net, 2), "€")
