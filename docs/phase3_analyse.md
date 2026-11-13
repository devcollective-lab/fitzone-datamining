# Phase 3 — Fidélisation et priorisation

## 1. Objectif

Cette troisième phase du projet FitZone vise à identifier les abonnés présentant un risque élevé de résiliation et à évaluer l'intérêt d'augmenter la capacité d'appel de l'équipe commerciale.

Elle répond aux questions 5 et 6 du projet : déterminer quels abonnés contacter en priorité parmi 400 personnes arrivant en fin d'engagement, puis estimer l'intérêt de passer de 80 à 160 appels.

## 2. Préparation des données

Nous avons utilisé les **797 abonnés** obtenus après le nettoyage de la phase 1.

La variable cible est `a_resilie` (`oui` ou `non`). Les huit variables explicatives retenues sont l'ancienneté, la formule, le prix mensuel, la distance domicile-salle, le créneau habituel, les visites mensuelles, les séances de coaching et les réclamations.

Les variables catégorielles ont été encodées avec `pd.get_dummies()`.

Les données ont ensuite été séparées avec `train_test_split()` :

- **637 abonnés (80 %)** pour l'entraînement.
- **160 abonnés (20 %)** pour le test.

Nous avons utilisé `random_state=42` et `stratify=y` afin d'obtenir une séparation reproductible conservant approximativement la proportion de résiliations.

## 3. Classification et évaluation

Nous avons entraîné une **régression logistique** avec scikit-learn pour prédire les résiliations.

Le modèle utilise `StandardScaler()` pour standardiser les données et `class_weight="balanced"` pour tenir compte du déséquilibre entre les deux classes.

### Résultats sur le jeu de test

| Indicateur | Résultat |
|---|---:|
| Accuracy | 71 % |
| Précision — résiliation | 43 % |
| Rappel — résiliation | 61 % |
| F1-score — résiliation | 50 % |

Sur les 38 abonnés ayant réellement résilié dans le jeu de test, le modèle en identifie correctement 23.

Ces résultats montrent que le modèle permet de repérer une partie des résiliations, même s'il commet encore des erreurs.

## 4. Question 5 — Sélection des abonnés prioritaires

FitZone peut appeler 80 abonnés parmi 400, soit **20 %**.

Pour reproduire cette proportion sur notre jeu de test, nous avons sélectionné les **32 abonnés ayant les scores de résiliation les plus élevés**, obtenus avec `predict_proba()`.

Parmi ces 32 abonnés, **15 ont réellement résilié**, soit une précision de ciblage de **46,88 %**.

Cette méthode permet de concentrer les appels sur les abonnés présentant les risques les plus élevés plutôt que de les sélectionner au hasard.

## 5. Question 6 — Comparaison et simulation des appels

Pour simuler le doublement de la capacité d'appel, nous avons comparé les 32 premiers abonnés aux 64 premiers du classement.

| Indicateur | 32 appels | 64 appels |
|---|---:|---:|
| Résiliations identifiées | 15 | 28 |
| Précision du ciblage | 46,88 % | 43,75 % |

Les **32 appels supplémentaires** permettent d'identifier **13 résiliations supplémentaires**, soit une augmentation de 86,67 % des résiliations identifiées.

Nous avons ensuite réalisé une simulation économique avec trois hypothèses : un taux de fidélisation de 30 %, un revenu mensuel de 35 € par abonné conservé et un coût de 2 € par appel.

La simulation donne les résultats suivants :

- Abonnés conservés estimés : **3,9**.
- Revenus mensuels supplémentaires : **136,50 €**.
- Coût des appels supplémentaires : **64 €**.
- Gain net mensuel estimé : **72,50 €**.

Ces résultats concernent notre échantillon de test et reposent sur des hypothèses, et non sur des mesures réelles de l'efficacité des appels.

## 6. Limites de l'analyse

Notre jeu de données ne permet pas d'identifier les abonnés arrivant réellement en fin d'engagement. Nous avons donc reproduit les proportions de l'énoncé sur les 160 abonnés du jeu de test.

Les scores du modèle ne sont pas nécessairement des probabilités parfaitement calibrées. De plus, identifier un abonné à risque ne garantit pas qu'un appel permettra de le conserver.

Enfin, la simulation économique utilise des valeurs hypothétiques et ne prend pas en compte les éventuels coûts supplémentaires de personnel.

## 7. Conclusion

Cette phase nous a permis d'utiliser la classification pour identifier les abonnés à contacter en priorité et comparer deux capacités d'appel.

Le modèle obtient une accuracy de 71 % et permet d'identifier 15 résiliations parmi les 32 abonnés prioritaires.

Le doublement des appels permet d'identifier 13 résiliations supplémentaires. La simulation suggère un gain économique positif avec les hypothèses retenues, sans garantir la rentabilité réelle de l'élargissement.

Ces résultats constituent une aide à la décision pour les actions de fidélisation de FitZone.