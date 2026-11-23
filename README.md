## Suivi de l'avancement

### Phase 1 — Exploration, Nettoyage et Préparation (Terminée)
- **Anomalies traitées** :
  - Suppression des doublons stricts.
  - Suppression des lignes comportant des anciennetés négatives (erreurs de saisie).
  - Imputation des prix à 0 € par la médiane de la formule d'abonnement correspondante.
- **Sortie** : Fichier `data/processed/FitZone_abonnes_propre.csv` généré et prêt pour les analyses suivantes.

---

## Phase 2 — Analyse des comportements et prédiction (Questions 1 à 4)

### Justification des méthodes appliquées
- **Analyse comparative des résiliations (Q1)** : Analyse descriptive bivariée (calcul des moyennes groupées) pour identifier les variables discriminantes entre abonnés fidèles et résiliés.
- **Étude de l'impact de la distance (Q2)** : Discrétisation de `distance_domicile_m` en tranches afin d'évaluer l'existence d'un seuil critique sur le taux de résiliation.
- **Modélisation de la fréquentation (Q3 & Q4)** : Régression linéaire multiple pour estimer l'impact de chaque variable explicative sur `visites_par_mois`.
- **Évaluation des performances (Q4)** :
  - **$R^2$** : Proportion de la variance expliquée par le modèle.
  - **RMSE** : Erreur moyenne exprimée en nombre de visites par mois.

---

## Phase 3 — Fidélisation et priorisation (Questions 5 et 6)

### Stratégie de fidélisation fondée sur les données
1. **Scoring prédictif du risque (Question 5)** : Utilisation d'une régression logistique (`src/classification.py`) calculant la probabilité individuelle de résiliation à partir de l'ancienneté, de la fréquence de visite, des réclamations, du coaching, de la distance et du tarif mensuel.
2. **Priorisation opérationnelle (Question 5)** : Sur une cohorte de 400 abonnés en fin d'engagement, extraction des 80 profils présentant la probabilité de départ la plus critique (`outputs/results/top_80_prioritaires.csv`) afin de concentrer les appels sortants sur les cas à plus fort enjeu.
3. **Arbitrage sur la capacité d'appel et gains estimés (Question 6)** :
   - **Hypothèses explicites** : Taux de conversion/rétention de **25 %** sur les abonnés contactés, prolongation moyenne de **6 mois** d'abonnement par client retenu, et coût opérationnel unitaire de **5 €** par appel.
   - **Décision métier** : Le traitement du Top 80 génère la rentabilité maximale par appel. L'extension de capacité à 160 appels (rangs 81 à 160) présente un rendement marginal décroissant (risque moyen plus faible) mais reste financièrement pertinente tant que le gain net additionnel couvre le coût de mobilisation des conseillers.