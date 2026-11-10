# FitZone — Data Mining

FitZone est un projet de Data Mining visant à analyser les comportements des abonnés d'une chaîne de salles de sport afin de mieux comprendre les résiliations, prédire la fréquentation et identifier des opportunités de fidélisation.

À travers l'exploration des données et l'utilisation de méthodes statistiques et de Machine Learning, le projet cherche à proposer des recommandations concrètes pour améliorer la prise de décision.

## 1. Contexte du projet

FitZone est une chaîne fictive de 14 salles de sport implantées en Île-de-France, comptant près de 10 000 abonnés.

Au cours de la dernière année, l'entreprise a constaté une augmentation de 30 % des résiliations. Elle souhaite mieux comprendre les facteurs associés à ces départs et optimiser ses actions de fidélisation.

L'étude repose sur deux fichiers CSV :

- `FitZone_abonnes.csv` : caractéristiques des abonnés, abonnements, habitudes de fréquentation et résiliations.
- `FitZone_salles.csv` : caractéristiques des salles de sport.

Ces données ont fait l'objet d'une phase d'exploration et de préparation avant les analyses approfondies.

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
│   ├── exploration.py        # Structure, anomalies, types et unités
│   ├── classification.py     # Classification
│   ├── regression.py         # Régression
│   ├── clustering.py         # Segmentation
│   └── evaluation.py         # Évaluation des modèles
├── tests/                    # Tests
├── outputs/
│   ├── figures/              # Graphiques
│   ├── models/               # Modèles entraînés
│   └── results/              # Résultats
├── docs/
│   └── phase1_exploration_preprocessing.md
├── main.py                   # Point d'entrée
├── requirements.txt          # Dépendances
├── .gitignore
└── README.md
```

Les différents scripts et dossiers seront complétés progressivement.

La documentation détaillée des traitements et des résultats est placée dans `docs/`.

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

Les deux fichiers CSV d'origine sont disponibles dans `data/raw/` après le clonage du dépôt :

```text
data/raw/
├── FitZone_abonnes.csv
└── FitZone_salles.csv
```

Les fichiers originaux sont conservés sans modification.

Après exécution du programme, les données préparées sont enregistrées automatiquement dans `data/processed/` :

```text
data/processed/
├── FitZone_abonnes_clean.csv
└── FitZone_salles_clean.csv
```

### 5.6. Exécuter le projet

Une fois les dépendances installées, lancer le programme depuis la racine du projet :

```bash
python main.py
```

Le programme charge les données, exécute les vérifications d'exploration, applique les traitements de nettoyage et enregistre les fichiers préparés.

Les résultats sont affichés dans le terminal.

## 6. Méthodologie

Le projet est organisé en cinq phases :

| Phase | Description | Statut |
|---|---|---|
| 1 | Exploration, vérification, nettoyage et préparation des données | Terminée et validée |
| 2 | Analyse des résiliations et prédiction de la fréquentation | En préparation |
| 3 | Fidélisation et priorisation des appels | À venir |
| 4 | Segmentation des abonnés et détection des anomalies | À venir |
| 5 | Synthèse des résultats, documentation et présentation | À venir |

### Phase 1 — Exploration et préparation des données

**Statut : terminée et validée.**

La phase 1 est terminée et ses développements ont été intégrés à la branche principale `main`.

Les traitements d'exploration, de nettoyage et de préparation des données sont opérationnels. Les résultats sont documentés et les fichiers nettoyés sont générés automatiquement lors de l'exécution du programme.

**Travail réalisé :**

- Exploration de la structure des deux jeux de données.
- Identification des valeurs manquantes, doublons et incohérences.
- Vérification des types de données et des unités.
- Contrôle de la correspondance des salles entre les deux fichiers.
- Suppression des doublons et traitement des valeurs manquantes.
- Correction des anciennetés négatives et des prix mensuels nuls.
- Vérification finale et sauvegarde des données nettoyées.

Après nettoyage, le fichier des abonnés contient **800 lignes et 11 colonnes**, sans doublons ni valeurs manquantes.

Le fichier des salles contient **14 lignes et 6 colonnes** et n'a nécessité aucune correction.

**Organisation du code :**

- `src/data_loader.py` : chargement des données.
- `src/exploration.py` : exploration et recherche des anomalies.
- `src/preprocessing.py` : nettoyage et préparation des données.
- `main.py` : exécution des étapes et sauvegarde des résultats.

Les choix de traitement et les résultats sont détaillés dans [la documentation de la phase 1](docs/phas1_doc.md).

### Phase 2 — Analyse des résiliations et prédiction de la fréquentation

**Statut : en préparation.**

Cette phase vise à analyser les facteurs associés aux résiliations et à développer des modèles de Machine Learning permettant de prédire la fréquentation mensuelle des abonnés.

**Travail prévu :**

- Étudier la répartition des résiliations et les caractéristiques des abonnés concernés.
- Analyser l'influence de la distance entre le domicile et la salle sur les résiliations.
- Identifier les variables susceptibles d'influencer la fréquentation mensuelle.
- Préparer les données nécessaires à la modélisation.
- Entraîner et comparer des modèles de régression.
- Évaluer les performances des modèles et interpréter les résultats.
- Documenter les analyses et les choix méthodologiques.

Les développements seront réalisés progressivement sur les branches de travail avant leur validation et leur intégration dans `main`.

### Phase 3 — Fidélisation et priorisation des appels

**Statut : à venir.**

Cette phase sera consacrée à l'identification des abonnés à contacter en priorité dans le cadre des campagnes de fidélisation.

**Travail prévu :**

- Identifier les abonnés présentant un risque de résiliation.
- Définir des critères de priorisation des appels.
- Étudier l'intérêt d'augmenter les moyens consacrés aux campagnes de fidélisation.
- Évaluer les résultats obtenus afin de proposer des actions adaptées.

### Objectif de la semaine

L'objectif collectif est de finaliser et de valider les phases 2 et 3 d'ici le **dimanche 15 novembre 2026**.

Les analyses, les développements et les résultats devront être vérifiés et documentés avant leur intégration dans la branche principale.

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
