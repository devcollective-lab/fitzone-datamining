# Phase 1 — Exploration et prétraitement des données

## 1. Objectif

Cette première phase du projet FitZone consiste à explorer les données disponibles, identifier les éventuelles anomalies et préparer un jeu de données exploitable pour les prochaines étapes du Data Mining.

L'objectif est de garantir une meilleure qualité des données avant les analyses et la construction des modèles.

## 2. Présentation des données

Le projet utilise deux fichiers CSV :

- **FitZone_abonnes.csv** : informations relatives aux abonnés, notamment leur formule, leur ancienneté, leur fréquentation, leurs séances de coaching et leur statut de résiliation.
- **FitZone_salles.csv** : informations sur les salles de sport, notamment leur localisation, leur superficie, leur ancienneté, le nombre de coachs et la présence d'un parking.

Avant nettoyage, le fichier des abonnés contient **840 lignes et 11 colonnes**, tandis que celui des salles contient **14 lignes et 6 colonnes**.

## 3. Exploration des données

L'exploration a été réalisée avec la bibliothèque Pandas.

Nous avons examiné :

- Les dimensions et la structure des deux datasets.
- Les noms et types des colonnes.
- Les valeurs manquantes et les doublons.
- Les statistiques descriptives des variables numériques.
- La répartition de certaines variables catégorielles.
- La cohérence des unités et des valeurs.

Cette exploration a permis d'identifier plusieurs anomalies dans les données des abonnés.

## 4. Anomalies détectées et traitements

### 4.1. Doublons

Le fichier des abonnés contenait **40 lignes dupliquées**.

Ces doublons ont été supprimés avec `drop_duplicates()` afin d'éviter de compter plusieurs fois les mêmes observations.

Le nombre d'abonnés est ainsi passé de 840 à **800**.

### 4.2. Séances de coaching manquantes

Après suppression des doublons, **20 valeurs manquantes** subsistaient dans la colonne `seances_coaching`.

Nous avons choisi de les remplacer par la médiane des séances de coaching correspondant à chaque formule d'abonnement.

Cette méthode permet de tenir compte des différences entre les formules Essentiel, Confort et Premium, tout en limitant l'influence des valeurs extrêmes.

Le traitement a été réalisé avec `groupby()`, `transform("median")` et `fillna()`.

### 4.3. Créneaux habituels manquants

Après suppression des doublons, la colonne `creneau_habituel` contenait **20 valeurs manquantes**.

Nous les avons remplacées par la catégorie **« Inconnu »**.

Ce choix permet de conserver les abonnés concernés sans leur attribuer artificiellement un créneau comme matin, midi ou soir.

### 4.4. Anciennetés négatives

Trois abonnés présentaient une ancienneté de **-1 mois**, une valeur incohérente pour cette variable.

Ces trois abonnés appartenaient à la formule Essentiel.

Nous avons choisi de **supprimer ces trois observations du jeu de données**, plutôt que de remplacer leurs anciennetés par une valeur estimée.

Cette décision permet d'éviter d'introduire des anciennetés artificielles dans les analyses, tout en conservant la grande majorité des observations.

Le nombre d'abonnés est ainsi passé de **800 à 797**.

### 4.5. Prix mensuels nuls

Trois abonnés présentaient un prix mensuel égal à zéro.

Dans le cadre de ce nettoyage, ces valeurs ont été considérées comme des anomalies.

Nous les avons remplacées par la médiane des prix strictement positifs correspondant à chaque formule d'abonnement, avec un arrondi à deux décimales.

Cette approche permet de conserver les différences tarifaires entre les formules.

### 4.6. Distances supérieures à 10 km

Neuf abonnés présentaient une distance domicile-salle supérieure à 10 km.

Après examen, nous avons décidé de conserver ces observations, car ces distances restent plausibles.

Elles peuvent également être pertinentes pour étudier l'influence de l'éloignement géographique sur la fréquentation et la résiliation.

## 5. Vérification finale

Après les traitements, nous avons effectué une nouvelle vérification du fichier des abonnés.

| Contrôle | Résultat |
|---|---|
| Nombre d'abonnés | 797 |
| Nombre de colonnes | 11 |
| Doublons restants | 0 |
| Valeurs manquantes restantes | 0 |
| Anciennetés négatives | 0 |
| Prix mensuels nuls | 0 |

Le fichier des salles ne présentait ni doublons ni valeurs manquantes et n'a nécessité aucune correction.

## 6. Sauvegarde des données

Les données préparées ont été enregistrées dans le dossier `data/processed/` :

- `FitZone_abonnes_clean.csv`
- `FitZone_salles_clean.csv`

Les fichiers originaux sont conservés dans `data/raw/` afin de préserver les données sources.

## 7. Conclusion

Cette première phase a permis d'explorer les deux datasets, de traiter les anomalies identifiées et d'obtenir un jeu de données préparé pour la suite du projet.

Les décisions de nettoyage ont été prises en tenant compte des caractéristiques des variables, notamment des différences entre les formules d'abonnement et de la nécessité d'écarter les observations présentant des anciennetés incohérentes.

Après nettoyage, le fichier des abonnés contient **797 observations exploitables**, sans doublons ni valeurs manquantes.

Les prochaines étapes porteront sur les analyses et les méthodes de Data Mining nécessaires pour répondre aux questions du projet FitZone.