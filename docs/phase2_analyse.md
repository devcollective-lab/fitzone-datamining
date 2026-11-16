# Phase 2 — Analyse des comportements et prédiction

## 1. Objectif

Cette deuxième phase du projet FitZone consiste à analyser les données des abonnés pour mieux comprendre les résiliations et les habitudes de fréquentation des salles de sport.

Nous avons travaillé sur les données nettoyées lors de la phase 1, soit **797 abonnés**. Notre travail répond aux quatre premières questions du projet : analyser les résiliations, étudier le lien avec la distance domicile-salle, prédire le nombre de visites mensuelles et évaluer les performances des modèles.

## 2. Analyse des résiliations

Nous avons commencé par calculer le taux global de résiliation, puis nous avons comparé les résultats selon la formule d'abonnement et le créneau habituel.

Sur les 797 abonnés, **189 ont résilié**, soit un taux de **23,71 %**.

### Résiliations par formule

| Formule | Taux de résiliation |
|---|---:|
| Premium | 5,98 % |
| Essentiel | 35,50 % |
| Confort | 19,26 % |

La formule Essentiel présente le taux de résiliation le plus élevé, tandis que Premium affiche le taux le plus faible.

Nous avons également comparé les prix mensuels moyens. Les abonnés ayant résilié payaient en moyenne **30,07 €**, contre **39,60 €** pour les abonnés toujours actifs.

Ces résultats montrent une différence entre les groupes, mais ils ne permettent pas d'affirmer que le prix ou la formule est directement responsable des résiliations.

### Résiliations par créneau habituel

| Créneau | Taux de résiliation |
|---|---:|
| Midi | 19,66 % |
| Variable | 23,91 % |
| Matin | 26,55 % |
| Soir | 23,19 % |
| Inconnu | 30,00 % |

Parmi les créneaux renseignés, le matin présente le taux de résiliation le plus élevé.

La catégorie « Inconnu » correspond aux créneaux manquants que nous avons remplacés pendant le nettoyage. Son résultat doit donc être interprété avec prudence.

Pour illustrer ces analyses, nous avons créé deux graphiques : `resiliations_formule.png` et `resiliations_creneau.png`.

## 3. Distance domicile-salle et résiliation

Nous avons ensuite étudié si la distance entre le domicile des abonnés et leur salle de sport pouvait être associée aux résiliations.

La distance moyenne est de **3,46 km pour les abonnés ayant résilié**, contre **2,93 km pour les autres**.

Nous avons également regroupé les abonnés par tranches de distance.

| Distance | Nombre d'abonnés | Taux de résiliation |
|---|---:|---:|
| 0 à 2 km | 309 | 16,50 % |
| 2 à 5 km | 354 | 27,68 % |
| 5 à 10 km | 125 | 29,60 % |
| 10 km et plus | 9 | 33,33 % |

Nous constatons que le taux de résiliation augmente globalement avec la distance.

Cependant, la dernière tranche ne contient que neuf abonnés. Son taux est donc moins représentatif que ceux des autres groupes.

Nous avons créé le graphique `resiliations_distance.png` pour visualiser cette évolution.

## 4. Prédiction des visites mensuelles

Après les analyses descriptives, nous avons utilisé le Machine Learning pour prédire le nombre de visites mensuelles des abonnés.

### Préparation des données

La variable cible est `visites_par_mois`.

Nous avons sélectionné sept variables explicatives :

- `anciennete_mois`
- `formule`
- `prix_mensuel_eur`
- `distance_domicile_m`
- `creneau_habituel`
- `seances_coaching`
- `reclamations`

Les variables catégorielles `formule` et `creneau_habituel` ont été transformées en colonnes numériques avec `pd.get_dummies()`.

Nous avons ensuite séparé les données en deux ensembles avec `train_test_split()` :

- **637 abonnés (80 %)** pour l'entraînement.
- **160 abonnés (20 %)** pour le test.

Nous avons utilisé `random_state=42` pour obtenir une séparation reproductible.

### Régression linéaire

Notre premier modèle est une régression linéaire entraînée avec `LinearRegression` de scikit-learn.

Après l'entraînement, nous avons réalisé des prédictions sur les 160 abonnés du jeu de test.

Nous avons également examiné les coefficients du modèle pour identifier les variables associées au nombre de visites.

Par exemple, le nombre de séances de coaching présente un coefficient positif d'environ **1,99**, tandis que le nombre de réclamations présente un coefficient négatif d'environ **−1,19**.

Ces coefficients décrivent des associations dans notre modèle et ne prouvent pas des relations de cause à effet. Les coefficients des catégories doivent également être interprétés avec prudence, car toutes les catégories ont été conservées lors de l'encodage.

## 5. Évaluation et comparaison des modèles

Pour mesurer les performances, nous avons utilisé trois métriques :

- **MAE** : erreur absolue moyenne entre les visites réelles et prédites.
- **RMSE** : mesure des erreurs qui donne davantage de poids aux écarts importants.
- **R²** : proportion de la variabilité des visites expliquée par le modèle sur les données évaluées.

Nous avons comparé trois approches : un modèle de référence basé sur la moyenne, une régression linéaire et un Random Forest.

### Résultats sur les données de test

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| Modèle de référence | 3,38 | 4,43 | ≈ 0 |
| Régression linéaire | **2,27** | **2,81** | **0,596** |
| Random Forest optimisé | 2,41 | 3,08 | 0,514 |

La régression linéaire obtient les meilleurs résultats parmi les modèles testés.

Sa MAE de 2,27 signifie que ses prédictions s'écartent en moyenne d'environ 2,27 visites par mois des valeurs réelles.

Son R² de 0,596 indique qu'elle explique environ 59,6 % de la variabilité des visites sur notre jeu de test.

### Optimisation du Random Forest

Nous avons d'abord entraîné un Random Forest avec 100 arbres.

Ce premier modèle obtenait un R² de **0,948 sur l'entraînement**, contre **0,469 sur le test**. Cet écart important indiquait un surapprentissage.

Nous avons donc utilisé `GridSearchCV` avec une validation croisée à cinq plis pour rechercher de meilleurs hyperparamètres sur les données d'entraînement.

Les paramètres sélectionnés sont :

```python
{
    "max_depth": 5,
    "min_samples_leaf": 4,
    "min_samples_split": 2
}
```

Après optimisation, le R² du Random Forest est passé à **0,742 sur l'entraînement** et à **0,514 sur le test**.

L'écart entre les deux ensembles a diminué, ce qui montre une réduction du surapprentissage. Malgré cette amélioration, le Random Forest reste moins performant que notre régression linéaire sur le jeu de test.

Nous avons donc choisi de **retenir la régression linéaire comme modèle principal** pour cette partie du projet.

## 6. Visualisations réalisées

Nous avons utilisé Matplotlib et Seaborn pour produire cinq graphiques :

| Fichier | Contenu |
|---|---|
| `resiliations_formule.png` | Taux de résiliation selon la formule |
| `resiliations_creneau.png` | Taux de résiliation selon le créneau |
| `resiliations_distance.png` | Taux de résiliation selon la distance |
| `predictions_regression.png` | Comparaison des visites réelles et prédites |
| `comparaison_modeles.png` | Comparaison des MAE des modèles |

Ces graphiques sont générés par `src/visualization.py` et enregistrés localement dans `outputs/figures/`.

Le graphique des visites réelles et prédites montre que notre régression linéaire suit globalement les valeurs observées, même si certaines prédictions restent éloignées de la réalité.

## 7. Limites de notre analyse

Notre travail présente plusieurs limites.

Tout d'abord, nous disposons de 797 abonnés, ce qui reste un ensemble relativement limité pour entraîner et comparer des modèles.

Ensuite, certaines catégories contiennent peu d'observations, notamment les abonnés vivant à 10 km ou plus de leur salle.

Nous avons également observé des différences de résiliation selon les formules, les créneaux et la distance, mais ces résultats ne suffisent pas à démontrer des relations de causalité.

Enfin, les performances des modèles ont été comparées sur un même jeu de test. Une validation supplémentaire sur de nouvelles données serait utile pour confirmer leur capacité de généralisation.

## 8. Conclusion

Cette deuxième phase nous a permis de mieux comprendre les comportements des abonnés FitZone et de construire un premier modèle de prédiction de leur fréquentation.

Nos analyses montrent notamment que la formule Essentiel présente le taux de résiliation le plus élevé et que les abonnés habitant plus loin de leur salle ont tendance à résilier davantage.

Pour la prédiction des visites mensuelles, nous avons comparé plusieurs modèles et retenu la régression linéaire, qui obtient les meilleurs résultats sur notre jeu de test.

Ces résultats constituent une première base pour la suite du projet, notamment pour identifier les abonnés à risque, étudier les actions de fidélisation et proposer des recommandations commerciales adaptées à FitZone.