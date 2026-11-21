# Phase 4 — Segmentation et détection des anomalies

## 1. Objectif

Cette phase vise à mieux comprendre les profils des abonnés de FitZone à travers trois analyses : la segmentation des abonnés, l'estimation de leur rentabilité et la détection des comportements atypiques.

Les résultats doivent permettre de proposer des actions marketing adaptées et d'orienter les décisions de gestion.

## 2. Question 7 — Segmentation des abonnés

**Problématique :** Le service marketing souhaite proposer quatre messages différents aux abonnés. Nous devons déterminer les profils existants et leur donner des noms compréhensibles.

### 2.1. Méthode utilisée

Nous avons utilisé l'algorithme **K-Means**, qui regroupe les abonnés présentant des caractéristiques similaires.

Six variables numériques ont été sélectionnées :

- Ancienneté en mois ;
- Prix mensuel de l'abonnement ;
- Distance entre le domicile et la salle ;
- Nombre de visites par mois ;
- Nombre de séances de coaching ;
- Nombre de réclamations.

Ces variables ont été standardisées avec `StandardScaler` pour éviter que leurs différences d'échelle influencent la formation des groupes.

La variable `a_resilie` n'a pas été utilisée pour créer les clusters. Elle intervient uniquement après la segmentation pour analyser les taux de résiliation.

### 2.2. Choix du nombre de clusters

Nous avons testé plusieurs valeurs de K, de 2 à 10, à l'aide de deux indicateurs :

- **L'inertie**, qui mesure la dispersion des abonnés autour du centre de leur cluster.
- **Le score de silhouette**, qui évalue la cohésion et la séparation des groupes.

La courbe d'inertie diminue progressivement, sans présenter de coude très marqué.

Le meilleur score de silhouette est obtenu avec **K = 2 (0,4289)**, contre **0,2683 pour K = 4**.

Nous avons néanmoins retenu **K = 4**, car cette segmentation permet d'obtenir quatre profils interprétables et de répondre au besoin du service marketing. Ce choix privilégie donc l'utilité métier plutôt que le meilleur score de silhouette.

Graphiques générés :

- `outputs/figures/inertie_clusters.png`
- `outputs/figures/silhouette_clusters.png`

### 2.3. Résultats de la segmentation

La segmentation a été réalisée sur **797 abonnés**.

| Cluster | Nombre d'abonnés | Part des abonnés | Taux de résiliation |
|---|---:|---:|---:|
| 0 | 307 | 38,5 % | 18,24 % |
| 1 | 170 | 21,3 % | 5,88 % |
| 2 | 192 | 24,1 % | 39,06 % |
| 3 | 128 | 16,1 % | 37,50 % |

Les caractéristiques moyennes permettent de distinguer quatre profils.

**Cluster 0 — Les réguliers de proximité**

Ce groupe compte 307 abonnés. Ils habitent en moyenne à 2,15 km de leur salle, effectuent 15,09 visites par mois et ne présentent aucune réclamation dans les données.

Leur taux de résiliation est de 18,24 %, inférieur au taux global de FitZone.

**Cluster 1 — Les fidèles Premium**

Ce groupe rassemble 170 abonnés, dont 98,24 % possèdent la formule Premium.

Ils présentent une ancienneté moyenne de 60,91 mois, effectuent 22,31 visites mensuelles et paient en moyenne 61,85 €.

Leur taux de résiliation est le plus faible, avec 5,88 %.

**Cluster 2 — Les abonnés avec réclamations**

Ce groupe compte 192 abonnés. Il présente une moyenne de 1,27 réclamation par abonné et une fréquentation de 13,64 visites par mois.

Son taux de résiliation atteint 39,06 %, le plus élevé des quatre groupes.

**Cluster 3 — Les abonnés éloignés**

Ce groupe rassemble 128 abonnés. Ils habitent en moyenne à 6,45 km de leur salle et effectuent 13,21 visites mensuelles, soit la fréquentation la plus faible.

Leur taux de résiliation est de 37,50 %.

### 2.4. Interprétation des résultats

Les quatre profils permettent d'envisager différentes actions marketing :

- **Les réguliers de proximité :** proposer des avantages de fidélisation.
- **Les fidèles Premium :** valoriser leur engagement avec des avantages adaptés.
- **Les abonnés avec réclamations :** améliorer le traitement des problèmes rencontrés.
- **Les abonnés éloignés :** étudier des solutions facilitant l'accès aux salles.

Les taux de résiliation complètent cette analyse, mais ne permettent pas d'affirmer que la distance ou les réclamations provoquent directement les départs.

### 2.5. Conclusion de la question 7

K-Means a permis d'identifier quatre profils d'abonnés exploitables pour adapter les actions marketing.

Même si K = 2 présente une meilleure séparation statistique, **K = 4 répond davantage au besoin métier** en proposant une segmentation plus détaillée.

## 3. Question 8 — Rentabilité des groupes

**Problématique :** Quel groupe rapporte le plus, lequel coûte le plus, et lequel ne mérite pas qu'on dépense un euro ?

### 3.1. Méthode utilisée

Pour comparer les clusters, nous avons analysé les revenus mensuels théoriques des abonnements, le nombre de visites et les séances de coaching.

Les données ne précisent pas les dépenses réelles de FitZone. Nous avons donc réalisé une **simulation économique** à partir de deux hypothèses :

- **1 € par visite en salle ;**
- **10 € par séance de coaching.**

Les calculs utilisés sont les suivants :

**Coût estimé = (Visites × 1 €) + (Séances de coaching × 10 €)**

**Marge simulée = Revenu théorique − Coût estimé**

Cette simulation ne comprend pas l'ensemble des charges de l'entreprise. Les revenus théoriques sont également calculés sur les 797 abonnés, y compris ceux indiqués comme résiliés. Ils ne représentent donc pas nécessairement les montants réellement encaissés.

### 3.2. Revenus mensuels par cluster

| Cluster | Nombre d'abonnés | Revenu mensuel théorique | Revenu moyen par abonné |
|---|---:|---:|---:|
| 0 | 307 | 9 361,05 € | 30,49 € |
| 1 | 170 | 10 515,10 € | 61,85 € |
| 2 | 192 | 5 716,15 € | 29,77 € |
| 3 | 128 | 4 168,70 € | 32,57 € |

Le **cluster 1 — Les fidèles Premium** génère le revenu mensuel théorique le plus élevé, avec **10 515,10 €**, malgré un effectif inférieur à celui des clusters 0 et 2.

Ce résultat s'explique notamment par son prix moyen d'abonnement plus élevé.

### 3.3. Utilisation des services

| Cluster | Visites mensuelles totales | Visites moyennes par abonné | Séances de coaching totales |
|---|---:|---:|---:|
| 0 | 4 632 | 15,09 | 105 |
| 1 | 3 793 | 22,31 | 404 |
| 2 | 2 619 | 13,64 | 70 |
| 3 | 1 691 | 13,21 | 56 |

Le cluster 0 enregistre le plus grand nombre total de visites.

Cependant, le **cluster 1** présente la fréquentation moyenne la plus élevée et concentre 404 séances de coaching, ce qui représente une utilisation importante des services.

### 3.4. Résultats de la simulation économique

| Cluster | Revenu théorique | Coût estimé | Marge simulée |
|---|---:|---:|---:|
| 0 | 9 361,05 € | 5 682,00 € | 3 679,05 € |
| 1 | 10 515,10 € | 7 833,00 € | 2 682,10 € |
| 2 | 5 716,15 € | 3 319,00 € | 2 397,15 € |
| 3 | 4 168,70 € | 2 251,00 € | 1 917,70 € |

Le **cluster 1** présente le coût estimé le plus élevé, avec **7 833 €**, principalement en raison de sa forte utilisation du coaching.

En revanche, le **cluster 0 — Les réguliers de proximité** obtient la meilleure marge totale simulée, avec **3 679,05 €**.

### 3.5. Comparaison des marges par abonné

Pour tenir compte des différences d'effectifs, nous avons également calculé la marge simulée moyenne par abonné.

| Cluster | Marge simulée par abonné |
|---|---:|
| 0 | 11,98 € |
| 1 | 15,78 € |
| 2 | 12,49 € |
| 3 | 14,98 € |

Le cluster 1 possède la marge simulée par abonné la plus élevée, tandis que le cluster 0 présente la meilleure marge totale.

Cette comparaison montre que les résultats économiques dépendent de l'indicateur retenu et de la taille des groupes.

### 3.6. Quel groupe faut-il éviter de financer ?

Nos résultats ne permettent pas d'identifier avec certitude un cluster dans lequel FitZone ne devrait réaliser aucun investissement.

Les quatre groupes présentent une marge positive dans notre simulation.

Le **cluster 2 — Les abonnés avec réclamations** mérite toutefois une attention particulière, car il présente le taux de résiliation le plus élevé (39,06 %) et une marge simulée par abonné relativement faible (12,49 €).

Il serait donc préférable d'étudier les problèmes rencontrés avant de proposer des avantages marketing coûteux.

Cela ne signifie pas qu'il faut abandonner ce groupe : des actions ciblées pourraient améliorer sa fidélisation.

### 3.7. Conclusion de la question 8

L'analyse permet de distinguer trois résultats principaux :

- **Le cluster 1** génère le revenu théorique le plus élevé et présente les coûts estimés les plus importants.
- **Le cluster 0** obtient la meilleure marge totale simulée.
- **Aucun cluster** ne peut être considéré comme ne méritant aucun investissement sur la seule base des données disponibles.

Une véritable analyse de rentabilité nécessiterait les dépenses réelles, les revenus effectivement encaissés et les coûts des actions marketing.

## 4. Question 9 — Détection des abonnés atypiques

**Problématique :** Il y a des abonnés qui ne ressemblent à personne. Combien sont-ils, qui sont-ils, et est-ce qu'on perd de l'argent avec eux ?

### 4.1. Méthode utilisée

Nous avons utilisé l'algorithme **Isolation Forest** de `scikit-learn` pour identifier les abonnés présentant des caractéristiques inhabituelles.

Contrairement à K-Means, qui regroupe les observations similaires, Isolation Forest cherche à détecter celles qui se distinguent des autres.

Nous avons réutilisé les six variables numériques standardisées de la question 7 : ancienneté, prix mensuel, distance, visites, coaching et réclamations.

Le modèle a été configuré avec `contamination=0.05`, correspondant à une hypothèse d'environ 5 % d'anomalies.

Il attribue deux étiquettes :

- `1` : abonné considéré comme normal ;
- `-1` : abonné considéré comme atypique.

Le nombre d'anomalies détectées dépend notamment du paramètre de contamination choisi.

### 4.2. Nombre d'abonnés atypiques

| Catégorie | Nombre d'abonnés | Pourcentage |
|---|---:|---:|
| Abonnés atypiques | 40 | 5,02 % |
| Autres abonnés | 757 | 94,98 % |
| **Total** | **797** | **100 %** |

Isolation Forest identifie **40 abonnés atypiques** parmi les 797 observations.

Ces abonnés présentent des caractéristiques inhabituelles, sans être nécessairement problématiques pour FitZone.

### 4.3. Caractéristiques des abonnés atypiques

| Caractéristique | Abonnés atypiques | Autres abonnés |
|---|---:|---:|
| Ancienneté moyenne | 56,78 mois | 26,53 mois |
| Prix mensuel moyen | 59,98 € | 36,15 € |
| Distance moyenne | 4,51 km | 2,98 km |
| Visites mensuelles moyennes | 22,62 | 15,63 |
| Séances de coaching moyennes | 3,58 | 0,65 |
| Nombre moyen de réclamations | 1,25 | 0,39 |

Les abonnés atypiques sont en moyenne plus anciens, paient des abonnements plus chers et fréquentent davantage les salles.

Ils utilisent également beaucoup plus le coaching et présentent davantage de réclamations.

Ces résultats décrivent les caractéristiques moyennes du groupe, mais ne signifient pas que les 40 abonnés possèdent exactement le même comportement.

### 4.4. Analyse économique des abonnés atypiques

Nous avons repris les hypothèses économiques de la question 8 pour comparer les deux catégories.

| Indicateur | Abonnés atypiques | Autres abonnés |
|---|---:|---:|
| Nombre d'abonnés | 40 | 757 |
| Revenus mensuels théoriques | 2 399,02 € | 27 361,98 € |
| Visites mensuelles totales | 905 | 11 830 |
| Séances de coaching totales | 143 | 492 |
| Coûts estimés | 2 335,00 € | 16 750,00 € |
| **Marge totale simulée** | **64,02 €** | **10 611,98 €** |
| **Marge simulée par abonné** | **1,60 €** | **14,02 €** |

Les abonnés atypiques génèrent des revenus moyens plus élevés, mais leur utilisation importante des services entraîne également des coûts estimés plus importants.

Leur marge simulée atteint seulement **1,60 € par abonné**, contre **14,02 €** pour les autres abonnés.

Cette différence suggère que leur forte consommation des services, notamment du coaching, réduit leur marge dans notre simulation.

### 4.5. Identification des abonnés à marge négative

Nous avons calculé la marge simulée individuellement pour les 40 abonnés atypiques.

| Situation | Nombre d'abonnés | Pourcentage |
|---|---:|---:|
| Marge simulée négative | 19 | 47,5 % |
| Marge simulée positive ou nulle | 21 | 52,5 % |
| **Total** | **40** | **100 %** |

**19 abonnés atypiques sur 40 présentent une marge individuelle simulée négative.**

Selon nos hypothèses, leurs coûts d'utilisation dépassent le montant théorique de leur abonnement.

Toutefois, la marge totale du groupe reste positive à **64,02 €**, grâce aux marges des autres abonnés atypiques.

### 4.6. Interprétation des résultats

Les abonnés atypiques ne doivent pas être automatiquement considérés comme peu rentables.

Leur engagement et leur utilisation des services peuvent représenter un intérêt pour FitZone. Cependant, leurs coûts estimés justifient une analyse plus précise des prestations proposées, notamment du coaching.

Il serait également pertinent d'étudier leurs réclamations afin de mieux comprendre leurs besoins.

Ces résultats restent hypothétiques : les données ne permettent pas de déterminer leur rentabilité réelle ni d'affirmer qu'ils font effectivement perdre de l'argent à l'entreprise.

### 4.7. Conclusion de la question 9

Isolation Forest a identifié **40 abonnés atypiques**, soit 5,02 % des abonnés étudiés.

Parmi eux, **19 présentent une marge individuelle simulée négative**, bien que la marge totale du groupe reste positive.

Ces résultats invitent FitZone à examiner plus précisément l'utilisation des services et les coûts associés, sans considérer automatiquement ces abonnés comme déficitaires.

## 5. Conclusion de la phase 4

Cette phase a permis de compléter l'analyse des abonnés de FitZone à travers trois approches.

La **segmentation K-Means** a identifié quatre profils permettant d'adapter les actions marketing selon les comportements des abonnés.

La **simulation économique** a montré que les fidèles Premium génèrent les revenus théoriques les plus élevés, tandis que les réguliers de proximité présentent la meilleure marge totale simulée.

Enfin, **Isolation Forest** a permis d'identifier 40 abonnés atypiques, dont 19 présentent une marge individuelle simulée négative.

Ces analyses fournissent des informations utiles pour orienter les décisions de fidélisation et de gestion.

Toutefois, les résultats économiques reposent sur des hypothèses et ne remplacent pas une analyse fondée sur les dépenses et les revenus réels de FitZone.