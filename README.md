# FitZone — Data Mining

FitZone est un projet de Data Mining visant à analyser les comportements des abonnés d'une chaîne de salles de sport afin de mieux comprendre les résiliations, prédire la fréquentation et identifier des opportunités de fidélisation.

À travers l'exploration des données et l'utilisation de méthodes statistiques et de Machine Learning, le projet cherche à proposer des recommandations concrètes pour améliorer la prise de décision.

## 1. Contexte du projet

FitZone est une chaîne fictive de 14 salles de sport implantées en Île-de-France, comptant près de 10 000 abonnés.

L'entreprise fait face à un taux de résiliation supérieur à 30 % par an. Elle souhaite mieux comprendre les facteurs associés à ces départs et améliorer ses actions de fidélisation.

L'étude repose sur deux fichiers CSV :

- `FitZone_abonnes.csv` : caractéristiques des abonnés, abonnements, habitudes de fréquentation et résiliations.
- `FitZone_salles.csv` : caractéristiques des salles de sport.

Ces données font l'objet d'une préparation avant les différentes analyses.

## 2. Objectifs

Le projet vise à répondre à plusieurs problématiques :

- Identifier les caractéristiques et comportements associés aux résiliations.
- Étudier l'influence de la distance entre le domicile et la salle.
- Prédire la fréquentation mensuelle des abonnés.
- Identifier les facteurs qui influencent la fréquentation.
- Déterminer quels abonnés contacter en priorité pour une campagne de fidélisation.
- Évaluer l'intérêt d'augmenter la capacité d'appel.
- Segmenter les abonnés selon leurs caractéristiques et comportements.
- Analyser l'intérêt économique des différents segments.
- Détecter les abonnés atypiques.

L'objectif final est de proposer **trois recommandations commerciales concrètes, justifiées et chiffrées**.

## 3. Technologies utilisées

Le projet utilise **Python 3.13** et les bibliothèques suivantes :

| Bibliothèque | Utilisation |
|---|---|
| Pandas | Manipulation et préparation des données |
| NumPy | Calcul numérique |
| Matplotlib | Visualisation des données |
| Seaborn | Visualisation statistique |
| Scikit-learn | Machine Learning |
| SciPy | Analyses statistiques |
| Pytest | Tests du code |

Le développement repose sur des scripts Python (`.py`), sans notebooks Jupyter.

Les dépendances sont répertoriées dans `requirements.txt`.

## 4. Structure du projet

```text
fitzone-datamining/
├── data/
│   ├── raw/                  # Données originales
│   └── processed/            # Données nettoyées
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Chargement des données
│   ├── preprocessing.py      # Nettoyage et préparation
│   ├── exploration.py        # Analyse des résiliations et distances
│   ├── regression.py         # Prédiction de la fréquentation
│   ├── classification.py     # Prédiction des résiliations
│   ├── clustering.py         # Segmentation (à venir)
│   ├── evaluation.py         # Évaluation des modèles
│   └── visualization.py      # Graphiques
├── tests/                    # Tests
├── outputs/
│   ├── figures/              # Graphiques
│   ├── models/               # Modèles (à venir)
│   └── results/              # Résultats (à venir)
├── docs/
│   ├── phase1_exploration_preprocessing.md
│   ├── phase2_analyse.md
│   └── phase3_analyse.md
├── main.py                   # Point d'entrée
├── requirements.txt          # Dépendances
├── .gitignore
└── README.md
```

La documentation des traitements et des résultats est disponible dans `docs/`.

## 5. Installation et configuration

### 5.1. Cloner le dépôt

```bash
git clone https://github.com/devcollective-lab/fitzone-datamining.git
cd fitzone-datamining
```

### 5.2. Créer un environnement Python

Il est recommandé d'utiliser **Python 3.13** et un environnement virtuel dédié au projet.

Deux méthodes sont possibles : Conda ou `venv`.

#### Option A — Avec Conda

Créer l'environnement :

```bash
conda create -n fitzone-dm python=3.13 -y
```

L'activer :

```bash
conda activate fitzone-dm
```

#### Option B — Avec venv

**Sur macOS et Linux :**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

**Sur Windows — PowerShell :**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Sur Windows — Invite de commandes (CMD) :**

```cmd
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
```

Ces commandes supposent que Python 3.13 est déjà installé.

### 5.3. Installer les dépendances

Après activation de l'environnement :

```bash
python -m pip install -r requirements.txt
```

### 5.4. Vérifier l'installation

```bash
python --version
```

Puis :

```bash
python -c "import pandas, numpy, sklearn; print('Environnement FitZone OK')"
```

### 5.5. Préparer les données

Les deux fichiers CSV d'origine sont disponibles dans `data/raw/` après le clonage du dépôt :

```text
data/raw/
├── FitZone_abonnes.csv
└── FitZone_salles.csv
```

Ces fichiers sont versionnés sur GitHub et conservés sans modification.

Après exécution du programme, les données nettoyées sont automatiquement enregistrées dans `data/processed/` :

```text
data/processed/
├── FitZone_abonnes_clean.csv
└── FitZone_salles_clean.csv
```

Le dossier `data/processed/` est ignoré par Git. Les fichiers nettoyés sont donc générés localement et ne sont pas envoyés sur GitHub.

### 5.6. Exécuter le projet

Une fois les dépendances installées, lancer le programme depuis la racine du projet :

```bash
python main.py
```

Le programme charge et nettoie les données, analyse les résiliations, entraîne et évalue les modèles de régression et de classification, puis simule la priorisation des appels.

Les résultats sont affichés dans le terminal.

Les données nettoyées sont enregistrées dans `data/processed/` et les graphiques dans `outputs/figures/`.

## 6. Méthodologie

Le projet est organisé en cinq phases, conformément au guide de travail.

| Phase | Description | Statut |
|---|---|---|
| 1 | Exploration et préparation des données | Terminée |
| 2 | Analyse des comportements et prédiction | Terminée sur la branche de travail |
| 3 | Fidélisation et priorisation | Terminée sur la branche de travail |
| 4 | Segmentation et détection des anomalies | À venir |
| 5 | Synthèse et finalisation | À venir |

### Phase 1 — Exploration et préparation des données

**Statut : terminée et intégrée à `main`.**

Cette phase a permis d'explorer les deux fichiers CSV, d'identifier les anomalies et de nettoyer les données.

Les principaux traitements concernent les doublons, les valeurs manquantes, les anciennetés négatives et les prix mensuels nuls.

Après nettoyage, nous disposons de **797 abonnés et 14 salles**.

Les traitements sont détaillés dans [la documentation de la phase 1](docs/phase1_exploration_preprocessing.md).

### Phase 2 — Analyse des comportements et prédiction

**Statut : développement terminé sur la branche de travail.**

Cette phase répond aux questions 1 à 4 du projet :

- Analyse des résiliations selon les formules, les créneaux et les prix.
- Étude de l'influence de la distance domicile-salle.
- Prédiction de la fréquentation mensuelle avec une régression linéaire et un Random Forest.
- Évaluation et comparaison des modèles.

La régression linéaire obtient un **R² de 0,596** sur le jeu de test, contre **0,514** pour le Random Forest optimisé.

Les résultats sont détaillés dans [la documentation de la phase 2](docs/phase2_analyse.md).

### Phase 3 — Fidélisation et priorisation

**Statut : développement terminé sur la branche de travail.**

Cette phase répond aux questions 5 et 6 du projet.

Une régression logistique a été entraînée pour estimer le risque de résiliation et classer les abonnés à contacter en priorité.

Sur le jeu de test de 160 abonnés :

- **32 abonnés prioritaires** : 15 résiliations identifiées.
- **64 abonnés prioritaires** : 28 résiliations identifiées.

Ces sélections reproduisent les proportions de 80 et 160 appels parmi 400 abonnés.

Une simulation économique, fondée sur des hypothèses, estime un **gain net mensuel de 72,50 €** pour les 32 appels supplémentaires sur cet échantillon.

Les résultats et les limites sont détaillés dans [la documentation de la phase 3](docs/phase3_analyse.md).

### Phase 4 — Segmentation et détection des anomalies

**Statut : à venir.**

Cette phase portera sur la segmentation des abonnés, l'analyse économique des différents profils et la détection des abonnés atypiques.

### Phase 5 — Synthèse et finalisation

**Statut : à venir.**

Cette dernière phase permettra de vérifier les réponses aux neuf questions, de formuler trois recommandations commerciales chiffrées et de finaliser les livrables du projet.

## 7. Organisation du travail et collaboration

Le projet est réalisé en groupe de cinq membres.

Chaque membre travaille sur sa propre branche afin de développer et de tester ses contributions.

Les résultats et les approches sont ensuite comparés collectivement. Les solutions retenues sont intégrées progressivement à la branche principale.

### Gestion des branches

Chaque membre crée sa branche de travail à partir de `main` :

```bash
git switch main
git pull origin main
git switch -c nom-de-branche
```

Les modifications sont enregistrées avec des commits réguliers et explicites.

Pour publier une branche :

```bash
git push -u origin nom-de-branche
```

Une Pull Request permet ensuite de proposer les modifications à intégrer.

### Règles de collaboration

- Chaque membre travaille sur sa propre branche.
- Les contributions doivent être compréhensibles et justifiées.
- Les commits sont réalisés depuis les comptes GitHub individuels.
- Les travaux sont comparés avant toute intégration dans `main`.
- La branche `main` contient uniquement les contributions validées.
- L'intégration dans `main` est supervisée par le responsable du dépôt.

## 8. Livrables

Les livrables du projet comprennent :

- Le code source des traitements et des analyses.
- Les résultats des explorations et des modèles.
- Les graphiques et évaluations associés.
- Trois recommandations finales argumentées et chiffrées.
- La documentation et la présentation PDF.

Le dépôt sera enrichi progressivement au fil de l'avancement du projet.