# FitZone — Data Mining

FitZone est un projet de Data Mining visant à analyser les comportements des abonnés d'une chaîne de salles de sport afin de mieux comprendre les résiliations, prédire la fréquentation et identifier des opportunités de fidélisation.

À travers l'exploration des données et l'utilisation de méthodes statistiques et de Machine Learning, le projet cherche à proposer des recommandations concrètes pour améliorer la prise de décision.

## 1. Contexte du projet

FitZone est une chaîne fictive de 14 salles de sport implantées en Île-de-France, comptant près de 10 000 abonnés.

Au cours de la dernière année, l'entreprise a constaté une augmentation de 30 % des résiliations. Elle souhaite mieux comprendre les facteurs associés à ces départs et optimiser ses actions de fidélisation.

L'étude repose sur deux fichiers CSV :

- `FitZone_abonnes.csv` : caractéristiques des abonnés, abonnements, habitudes de fréquentation et résiliations.
- `FitZone_salles.csv` : caractéristiques des salles de sport.

Ces données nécessitent une phase de vérification et de préparation avant toute analyse approfondie.

## 2. Objectifs

Le projet vise à répondre à plusieurs problématiques :

- Identifier les caractéristiques et comportements associés aux résiliations.
- Étudier l'influence de la distance entre le domicile et la salle.
- Prédire la fréquentation mensuelle des abonnés et évaluer la fiabilité des prédictions.
- Identifier les principaux facteurs qui influencent la fréquentation.
- Déterminer quels abonnés contacter en priorité pour une campagne de fidélisation.
- Évaluer l'intérêt d'augmenter les moyens consacrés aux appels.
- Segmenter les abonnés selon leurs caractéristiques et comportements.
- Analyser l'intérêt économique des différents segments.
- Détecter les abonnés atypiques et étudier leur impact économique.

L'objectif final est de formuler **trois recommandations concrètes, justifiées et chiffrées**.

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
│   ├── exploration.py        # Analyse exploratoire
│   ├── classification.py     # Classification
│   ├── regression.py         # Régression
│   ├── clustering.py         # Segmentation
│   └── evaluation.py         # Évaluation des modèles
├── tests/                    # Tests
├── outputs/
│   ├── figures/              # Graphiques
│   ├── models/               # Modèles entraînés
│   └── results/              # Résultats
├── docs/                     # Documentation et présentation
├── main.py                   # Point d'entrée
├── requirements.txt          # Dépendances
├── .gitignore
└── README.md
```

Les différents scripts et dossiers seront complétés progressivement.

## 5. Installation et configuration

### 5.1. Cloner le dépôt

```bash
git clone https://github.com/devcollective-lab/fitzone-datamining.git
cd fitzone-datamining
```

### 5.2. Créer un environnement Python

Il est recommandé d'utiliser **Python 3.13** et un environnement virtuel dédié au projet.

Deux méthodes sont possibles : Conda ou `venv`.

#### Option A — Avec Conda (Windows, macOS et Linux)

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

Les commandes supposent que Python 3.13 est déjà installé sur l'ordinateur.

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

Les deux fichiers CSV du sujet doivent être placés dans `data/raw/` :

```text
data/raw/
├── FitZone_abonnes.csv
└── FitZone_salles.csv
```

Les fichiers originaux doivent être conservés sans modification.

Les données nettoyées ou transformées seront enregistrées séparément dans `data/processed/`.

## 6. Méthodologie

Le projet est organisé en cinq phases :

| Phase | Description |
|---|---|
| 1 | Exploration, vérification, nettoyage et préparation des données |
| 2 | Analyse des résiliations et prédiction de la fréquentation |
| 3 | Fidélisation et priorisation des appels |
| 4 | Segmentation des abonnés et détection des anomalies |
| 5 | Synthèse des résultats, documentation et présentation |

### Phase actuelle : Exploration et préparation des données

Cette première phase consiste à :

- Examiner la structure des deux jeux de données.
- Identifier les valeurs manquantes et les doublons.
- Repérer les valeurs incohérentes ou impossibles.
- Vérifier les types de données et les unités.
- Étudier les premières distributions et relations entre variables.
- Proposer des traitements de nettoyage justifiés.
- Préparer des données exploitables pour les analyses suivantes.

Les données originales sont conservées afin de garantir la traçabilité des transformations.

## 7. Organisation du travail et collaboration

Le projet est réalisé en groupe de cinq membres.

Pendant la première phase, chaque membre travaille indépendamment sur sa propre branche afin d'explorer les données et de proposer une méthode de préparation.

Les résultats et les approches seront ensuite comparés collectivement. Les solutions retenues seront intégrées progressivement à la branche principale.

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
 



 ## Suivi de l'avancement

 Exploration, Nettoyage et Préparation (Terminée)
- **Anomalies traitées** : 
  - Suppression des doublons stricts.
  - Suppression des lignes comportant des anciennetés négatives (erreurs de saisie).
  - Imputation des prix à 0 € par la médiane de la formule d'abonnement correspondante.
- **Sortie** : Fichier `data/processed/FitZone_abonnes_propre.csv` généré et prêt pour la Phase 2.