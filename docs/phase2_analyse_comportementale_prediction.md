# Phase 2 : Analyse comportementale et prédictions

## 1. Facteurs associés aux résiliations

### Hypothèses (formulées avant l'analyse)

| Variable | Hypothèse pour les résiliés | Justification |
|---|---|---|
| visites_par_mois | moyenne plus basse | par manque de régularité, les abonnés seraient susceptibles de résilier |
| anciennete_mois | moyenne plus basse | les nouveaux abonnés surtout ceux ayant été en période d'essai seraient susceptibles de résilier s'ils ne sont pas assez satisfaits |
| reclamations | moyenne plus haute | plus on fait de réclamations, plus on n'est pas satisfait des solutions apportées et plus on résilie  |
| distance_domicile_m | moyenne plus haute | plus la distance est élevée plus on perd la motivation pour aller s'entraîner |
| seances_coaching | moyenne plus basse | les abonnés qui s'entrainent sans coaching n'ont pas de suivi en temps réel, il serait donc plus facile pour eux de résilier |

### Méthode
Pour chaque groupe : ` résilié ` et `non résilié `, nous calculons la moyenne et la médiane en fonction des variables suivantes: l'ancienneté, la distance domicile salle, les visites par mois et les séances de coaching.
Pour les variables suivantes : la formule, les réclamations et le créneau habituel, nous calculons le taux de résiliation par catégorie, avec leur effectif.
On regarde la médiane, parce que la moyenne peut être influencée par des valeurs atypiques comme 15970m qui la grossiront et fausseront le résultat.

### Résultats et Interprétations
Après analyse :

| Variable | Hypothèse pour les résiliés | Résultats | Interprétation |
|---|---|---|---|
| visites_par_mois | moyenne plus basse | 13.3 visites par mois en moyenne pour les résiliés contre 16.8 pour les non-résiliés | Les résiliés fréquentaient moins la salle |
| anciennete_mois | moyenne plus basse | les résiliés sont partis après une ancienneté moyenne de 16.65 mois et une médiane de 13 mois tandis que ceux qui sont restés ont une ancienneté moyenne de 31.58 mois et une médiane de 25 mois | Ce qui suggère que les départs se concentrent dans la première année. On suppose que l’ancienneté d’un résilié s’arrête à son départ, puisque le sujet ne le précise pas. Pour un résilié, le compteur s’arrête à son départ, alors qu’il continue pour les autres. Une partie de l’écart vient donc de la façon de mesurer |
| reclamations | moyenne plus haute | On passe de 19 % à 41 %, soit plus du double entre 0 et 2 réclamations : on parle d’un risque qui augmente, pas d’une majorité qui part. Les taux pour 3 et 4 réclamations reposent sur 4 et 2 abonnés, donc ne sont pas fiables | plus un abonné fait de réclamations, plus le risque de résiliation augmente |
| distance_domicile_m | moyenne plus haute | ceux qui ont résilié se trouvaient à une distance moyenne de 3465m de la salle de sport contre 2932m pour ceux qui ne l'ont pas fait. Pour les non-résiliés la médiane est de 2443m et pour les résiliés elle est de 3054m | la médiane confirme la moyenne, l'écart ne vient pas majoritairement des 9 clients habitant à plus de 10km : une distance plus importante est associée à davantage de résiliations |
| seances_coaching | moyenne plus basse | les clients n'ayant pas résilié ont environ 0.96 séances de coaching tandis que ceux ayant résilié en ont 0.28 seulement. La médiane des non-résiliés vaut 1 et celle des résiliés 0 | Ce sont surtout les Premium qui font du coaching, et ce sont aussi eux qui résilient le moins. On ne sait pas encore si c’est le coaching ou la formule qui compte |


| Variable | Taux de résiliation | Effectif | Résultats |
|---|---|---|---|
| formule | 5.9% pour les abonnés Premium contre 35.5% et 19.26% pour les abonnés Essentiel et Confort | 11 abonnés Premium résiliés sur 184 contre 47 abonnés Confort résiliés sur 244 et 131 abonnés Essentiel résiliés sur 369 | de 6 % (Premium) à 36 % (Essentiel). Un écart énorme, et sur de gros groupes (184 à 369 personnes). C’est un facteur fort |
| creneau_habituel | 26.55% pour ceux qui viennent le `matin`, 19.65% pour le `midi`, 23.18% pour le `soir`, 23.91% pour un créneau `variable` et 30% pour un créneau `Inconnu` (mais calculé sur 20 personnes seulement donc pas fiable) | `matin`: 47 résiliés sur 177, `midi`: 23 sur 117, `soir` : 80 sur 345, `variable`: 33 sur 138 et ` inconnu `: 6 résiliés sur 20  | tout est entre 20 % et 27 %, très proche du taux global. Venir le matin ou le soir ne semble pas changer grand-chose. C’est un facteur faible, voire pas un facteur du tout |

### Tests statistiques : les écarts observés sont-ils réels ?

#### Objectif
Les taux de résiliation varient d'une catégorie à l'autre, mais une partie de ces écarts peut être due au hasard : même si une variable n'avait aucun effet, les groupes n'auraient jamais exactement le même taux. Le test du χ² (khi-deux) permet de savoir si un écart est trop grand pour s'expliquer par le hasard.

#### Méthode
- `Hypothèse nulle` : la variable n'a aucun lien avec la résiliation. Dans ce cas, chaque catégorie devrait avoir le même taux de résiliation que l'ensemble des abonnés (23,7 %).
  Exemple : pour les 117 abonnés du midi, on attendrait 117 × 0,237 ≈ 28 résiliés. On en observe 23.
- Le test compare, pour chaque catégorie, le nombre de résiliés **observé** au nombre **attendu** sous l'hypothèse nulle, puis calcule une **p-value** : la probabilité d'observer des écarts au moins aussi grands si la variable n'avait aucun effet.
- `Seuil retenu : 0,05.` Si p < 0,05, l'écart est jugé statistiquement significatif.
- Outils : `pd.crosstab` pour construire le tableau croisé (catégorie × résiliation), `scipy.stats.chi2_contingency` pour le test.

#### Hypothèses (formulées avant les tests)

| Variable | Pari | Justification |
|---|---|---|
| formule | significatif | écart très important entre les taux (6,0 % pour Premium contre 35,5 % pour Essentiel), sur de grands groupes |
| reclamations | significatif | taux qui augmente nettement avec le nombre de réclamations (19,4 % à 0 réclamation, 41,7 % à 2 ou plus) |
| creneau_habituel | non significatif | taux tous proches du taux global (entre 19,7 % et 26,6 %) |
| salle | non significatif | le taux de résiliation se répartit entre 14% et 31% sans réel écart significatif |

#### Conditions de validité
Le test du χ² n'est fiable que si le nombre **attendu** dans chaque case du tableau est d'au moins 5.
- `Réclamations` : les catégories 3 et 4 réclamations ne comptent que 4 et 2 abonnés (environ 0,5 résilié attendu pour 4 réclamations). Elles ont été **regroupées** avec la catégorie 2 en une catégorie « 2 ou plus » (60 abonnés, environ 14 résiliés attendus), via `clip(upper=2)` dans une nouvelle colonne `reclamations_groupe`. La colonne d'origine n'est pas modifiée.
- `Créneau` : la catégorie « Inconnu » (20 abonnés) donne 4,7 résiliés attendus, légèrement sous le seuil. Vu la p-value très élevée (0,67), cela ne remet pas en cause la conclusion.

#### Résultats

| Variable | p-value | Conclusion | Pari |
|---|---|---|---|
| formule | 2,1 × 10⁻¹⁴ | significatif | vérifié |
| reclamations (2 ou plus regroupés) | 6,1 × 10⁻⁵ | significatif | vérifié |
| creneau_habituel | 0,67 | aucune dépendance significative mise en évidence | vérifié |
| salle | 0,44 | aucune dépendance significative mise en évidence | vérifié |

Pour information, le test sur les réclamations non regroupées donnait p = 0,0006, mais il ne respectait pas les conditions de validité.

#### Interprétation
- `Formule et réclamations` sont associées de façon significative à la résiliation. Les écarts observés ne s'expliquent pas par le hasard.
- `Créneau` : l'écart entre midi (19,7 %) et matin (26,6 %) est compatible avec le hasard. Venir à un moment ou à un autre de la journée ne semble pas lié au départ.
- `Salle` : les taux varient pourtant de 14,3 % (S13) à 31,7 % (S07), mais avec 14 salles de 45 à 76 abonnés, de tels écarts sont attendus par simple hasard (p = 0,44). Pour FitZone, cela suggère que les résiliations dépendent davantage du profil des abonnés que de la salle fréquentée.

#### Limites
- **« Non significatif » ne veut pas dire « aucun effet »** : le test indique seulement qu'aucun effet n'est détectable avec nos 797 abonnés. Un effet faible pourrait exister.
- **« Significatif » ne veut pas dire « cause »** : le test montre une association, pas une causalité. Par exemple, les abonnés les plus motivés choisissent peut-être Premium, et c'est leur motivation qui les fait rester.
- **« Significatif » ne veut pas dire « fort »** : une p-value très petite indique que l'écart est réel, pas qu'il est grand. Pour mesurer l'importance d'un facteur, il faut regarder l'écart entre les taux.

### Tests statistiques pour les variables numériques : test de Mann-Whitney

#### Pourquoi pas le test du χ² ?
Le χ² compte le nombre d'abonnés par case d'un tableau croisé. Or `distance_domicile_m` prend 752 valeurs différentes pour 797 abonnés : le tableau aurait une ligne par valeur, avec environ 0,2 résilié attendu par case, très loin du minimum de 5. Pour les variables numériques, il faut un test adapté.

#### Méthode
Le test de Mann-Whitney vérifie si les valeurs d'un groupe sont globalement plus élevées que celles de l'autre :
1. tous les abonnés (résiliés et non résiliés mélangés) sont classés du plus petit au plus grand selon la variable ;
2. chacun reçoit un rang (de 1 à 797) ;
3. le test regarde si les résiliés sont répartis au hasard dans ce classement (hypothèse nulle : la variable n'a aucun lien avec la résiliation) ou concentrés d'un côté.

Il donne une p-value, interprétée avec le même seuil de 0,05.

**Pourquoi Mann-Whitney plutôt que le test t (Student) ?** Le test t compare les moyennes, qui sont sensibles aux valeurs atypiques (par exemple les abonnés habitant à près de 16 km). Mann-Whitney travaille sur les rangs : une valeur extrême garde simplement le dernier rang, quelle que soit sa taille. C'est la même logique que l'utilisation de la médiane plutôt que de la moyenne.

Le test indique si les groupes diffèrent, mais pas dans quel sens : les médianes de chaque groupe sont donc affichées à côté de la p-value.

#### Hypothèses (formulées avant les tests)
- Les 4 variables seront significatives (p < 0,05).
- L'ancienneté et la distance auront les p-values les plus petites ; les visites et le coaching auront des p-values plus grandes, mais toujours sous 0,05.

#### Résultats

| Variable | Médiane non-résiliés | Médiane résiliés | p-value | Conclusion |
|---|---|---|---|---|
| visites_par_mois | 16 | 13 | 2,0 × 10⁻²¹ | significatif |
| anciennete_mois | 25 mois | 13 mois | 1,2 × 10⁻¹⁶ | significatif |
| seances_coaching | 1 | 0 | 1,4 × 10⁻¹³ | significatif |
| distance_domicile_m | 2 443 m | 3 054 m | 4,8 × 10⁻⁴ | significatif |

**Bilan des paris :** les 4 variables sont bien significatives. En revanche, le classement est différent de celui attendu : les visites ont la p-value la plus petite et la distance la plus grande.

#### Interprétation
- `Visites` : c'est le signal le plus net. Un écart de 3 visites par mois est important comparé à la fourchette habituelle (la plupart des abonnés viennent entre 13 et 18 fois par mois) : les résiliés sont nettement décalés vers le bas du classement.
- `Distance` : l'écart est réel mais plus discret. Les distances sont très étalées (de 150 m à près de 16 km, la plupart entre 1,5 et 4 km) : un écart de 600 m entre les médianes laisse les deux groupes très mélangés. La distance est associée à la résiliation, mais c'est le facteur numérique le moins marqué. Elle est étudiée plus en détail dans la question 2.
- `Ancienneté` : l'écart est significatif, mais une partie vient de la façon de mesurer (le compteur d'ancienneté s'arrête au départ d'un résilié et continue pour les autres). Le test ne corrige pas ce biais.
- `Coaching` : l'écart est significatif, mais le coaching est surtout pratiqué par les abonnés Premium, qui résilient aussi le moins. On ne peut pas encore séparer l'effet du coaching de celui de la formule.

#### Limites
- Comme pour le χ², une p-value indique à quel point on est **sûr** qu'un écart existe, pas à quel point il est **grand**. Les p-values peuvent être comparées entre elles ici uniquement parce que les 4 tests portent sur les mêmes 797 abonnés.
- Ces tests montrent des associations, pas des causes.

---

### Synthèse de la question 1

| Facteur | Lien avec la résiliation | Remarque |
|---|---|---|
| Visites par mois | **significatif**, signal le plus net | les résiliés venaient environ 3 fois de moins par mois |
| Formule | **significatif**, facteur fort | de 6,0 % (Premium) à 35,5 % (Essentiel) |
| Ancienneté | **significatif** | en partie dû à la façon de mesurer |
| Coaching | **significatif** | lié à la formule Premium, effet propre à vérifier |
| Réclamations | **significatif** | de 19,4 % (0 réclamation) à 41,7 % (2 ou plus) |
| Distance | **significatif**, plus discret | étudiée en détail dans la question 2 |
| Créneau habituel | aucun lien mis en évidence | taux entre 19,7 % et 26,6 % |
| Salle | aucun lien mis en évidence | les écarts entre salles sont compatibles avec le hasard |

`Le profil type de l'abonné qui résilie` : formule Essentiel, fréquentation faible, peu ou pas de coaching, au moins une réclamation, inscrit depuis peu.

## 2. Influence de la distance domicile-salle

### Rappel (question 1)
Le test de Mann-Whitney a déjà montré que les résiliés habitent plus loin de leur salle que les non-résiliés (médiane de 3 054 m contre 2 443 m, p = 4,8 × 10⁻⁴). Cette partie cherche à préciser **comment** le risque évolue avec la distance, et **pourquoi**.

### Hypothèses (formulées avant l'analyse)
| Question | Pari | Justification |
|---|---|---|
| Forme de l'évolution du taux de résiliation avec la distance | un seuil : taux stable, puis qui augmente d'un coup à partir d'une certaine distance | le risque n’augmente pas forcément à chaque kilomètre : il pourrait exister une distance au-delà de laquelle se rendre à la salle devient vraiment contraignant |
| Les abonnés éloignés viennent-ils moins souvent ? | oui, différence significative | plus la distance est grande, plus l'envie de se déplacer diminue |

### Méthode

**1. Découpage en tranches.** La distance prend 752 valeurs différentes, ce qui empêche de calculer un taux par valeur ou d'utiliser le χ². Les abonnés ont été répartis en 6 tranches avec `pd.cut` :
moins de 1 km, 1-2 km, 2-3 km, 3-4 km, 4-6 km, 6 km et plus.
- Des tranches de 1 km sont faciles à interpréter pour FitZone.
- Au-delà de 4 km, les abonnés sont moins nombreux : les tranches ont été élargies pour que chaque groupe compte au moins 78 abonnés.
- Une nouvelle colonne `tranche_distance` a été créée ; la colonne d'origine n'est pas modifiée.

**2. Taux de résiliation par tranche**, avec effectifs, puis test du χ² (tranche × résiliation).

**3. Fréquentation par tranche** : médiane et moyenne des visites par mois dans chaque tranche, puis test de **Kruskal-Wallis**. Ce test est l'équivalent de Mann-Whitney pour plus de deux groupes : il compare les rangs des valeurs entre les 6 tranches.

### Résultats

**Taux de résiliation par tranche**

| Tranche | Abonnés | Résiliés | Taux de résiliation |
|---|---|---|---|
| < 1 km | 102 | 15 | 14,7 % |
| 1-2 km | 207 | 36 | 17,4 % |
| 2-3 km | 152 | 42 | 27,6 % |
| 3-4 km | 132 | 32 | 24,2 % |
| 4-6 km | 126 | 41 | 32,5 % |
| 6 km et plus | 78 | 23 | 29,5 % |

Test du χ² : p = 0,004, significatif. Conditions de validité respectées : le plus petit nombre attendu de résiliés est d'environ 18,5 (tranche « 6 km et plus »).

En regroupant en deux catégories :
- moins de 2 km : 51 résiliés sur 309 abonnés, soit **16,5 %** ;
- 2 km et plus : 138 résiliés sur 488 abonnés, soit **28,3 %**, environ **1,7 fois plus**.

**Fréquentation par tranche**

| Tranche | Visites par mois (médiane) | Visites par mois (moyenne) |
|---|---|---|
| < 1 km | 17 | 17,8 |
| 1-2 km | 15 | 16,5 |
| 2-3 km | 15 | 15,5 |
| 3-4 km | 16 | 16,3 |
| 4-6 km | 14 | 14,8 |
| 6 km et plus | 14 | 14,7 |

Test de Kruskal-Wallis : p = 3,4 × 10⁻⁶, significatif.

**Bilan des paris :** les deux paris sont confirmés. Le seuil observé se situe autour de 2 km.

### Interprétation
- **Un seuil autour de 2 km** : en dessous, le taux de résiliation reste entre 15 et 17 % ; au-dessus, il se situe entre 24 et 33 %. Une hypothèse possible est qu'en dessous de 2 km, la salle reste accessible à pied ou à vélo, alors qu'au-delà, il faut prendre les transports ou la voiture.
- **Les petites irrégularités** (3-4 km plus bas que 2-3 km, 6 km et plus plus bas que 4-6 km) portent sur des écarts de 3 à 4 points, entre des groupes de 78 à 152 abonnés : elles sont compatibles avec le hasard et ne doivent pas être sur-interprétées. Seule la tendance générale compte.
- **Les abonnés éloignés viennent moins souvent** : environ 3 visites de moins par mois entre les tranches extrêmes. Comme la fréquentation est le facteur le plus fortement associé à la résiliation (question 1), une hypothèse cohérente est la chaîne suivante :
  **distance élevée → fréquentation plus faible → résiliation**.
  L'effet de la distance pourrait donc passer, au moins en partie, par une baisse de fréquentation.

### Limites
- **Le choix des tranches est arbitraire** : d'autres bornes donneraient des taux légèrement différents. La conclusion générale (risque plus élevé au-delà de 2 km) est cependant cohérente avec le test de Mann-Whitney réalisé sur les distances brutes, sans découpage.
- **La chaîne distance → fréquentation → résiliation n'est pas prouvée** : elle est seulement cohérente avec les résultats. Pour la vérifier, il faudrait montrer qu'à fréquentation égale, la distance n'a plus de lien avec la résiliation.
- Comme pour la question 1, ces résultats montrent des associations, pas des causes.

### Piste pour FitZone
Les abonnés habitant à plus de 2 km de leur salle (488 abonnés sur 797, soit 61 %) présentent un risque de résiliation plus élevé. Ils constituent une population à surveiller, notamment pour la campagne de fidélisation étudiée en phase 3.

## 3. Prédiction de la fréquentation mensuelle

### Type de problème
La variable à prédire, `visites_par_mois`, est un **nombre** (de 5 à 31 visites) et non une catégorie : il s'agit d'un problème de **régression**.

### Choix des variables d'entrée
Pour chaque colonne, la question posée est : FitZone connaît-elle cette information au moment de prédire la fréquentation d'un abonné actuel ?

| Colonne | Utilisée ? | Raison |
|---|---|---|
| anciennete_mois, prix_mensuel_eur, distance_domicile_m, seances_coaching, reclamations | oui | connues pour un abonné actuel |
| formule, creneau_habituel, salle | oui (après encodage) | connues pour un abonné actuel |
| a_resilie | **non** | information future : pour un abonné encore inscrit, on ne sait pas s'il va résilier. L'utiliser serait une **fuite de données** |
| abonne_id | **non** | simple étiquette, sans lien avec le comportement ; risque d'apprentissage par cœur |
| tranche_distance, reclamations_groupe | **non** | colonnes créées pendant l'analyse, redondantes avec les colonnes d'origine |

### Encodage des variables catégorielles
Un modèle ne calcule qu'avec des nombres. Numéroter les catégories (matin = 0, midi = 1, soir = 2…) créerait un faux ordre : le soir serait « plus grand » que le matin. Les variables `formule`, `creneau_habituel` et `salle` ont donc été transformées par **one-hot encoding** (`pd.get_dummies`) : une colonne 0/1 par catégorie.

Avec `drop_first=True`, la première catégorie (ordre alphabétique) est retirée et sert de **référence** : elle se déduit des autres colonnes (0 partout), et sa présence créerait une redondance.
- formule : référence **Confort**
- créneau : référence **Inconnu**
- salle : référence **S01**

Résultat : 24 colonnes d'entrée (5 numériques + 2 formules + 4 créneaux + 13 salles), pour 797 abonnés.

### Méthode d'évaluation
- **Découpage** : 80 % des abonnés pour l'entraînement (637), 20 % pour le test (160), avec `train_test_split`. Le modèle est évalué sur des abonnés qu'il n'a jamais vus. `random_state=42` rend le découpage reproductible pour tout le groupe.
- **Mesures** :
  - **MAE** (erreur absolue moyenne) : de combien de visites le modèle se trompe en moyenne ;
  - **R²** : part des différences de fréquentation entre abonnés expliquée par le modèle (0 = n'explique rien, 1 = prédiction parfaite).
- **Modèle de référence (baseline)** : prédire la même valeur pour tous les abonnés, la **médiane** des visites de l'entraînement (15). La médiane est la valeur unique qui minimise la MAE. Tout modèle doit faire mieux que cette référence pour être utile.

### Modèle : régression linéaire
La régression linéaire cherche une formule du type :
visites = base + a × distance + b × coaching + … (un coefficient par colonne d'entrée).
L'entraînement (`fit`) consiste à trouver les coefficients qui minimisent les erreurs sur les abonnés d'entraînement.

### Hypothèses (formulées avant chaque calcul)

| Question | Pari | Résultat | Pari gagné ? |
|---|---|---|---|
| MAE de la baseline | entre 3 et 5 visites | 3,36 | oui |
| MAE du modèle sur le test | environ 2 visites | 2,29 | oui |
| MAE du modèle sur l'entraînement | entre 1 et 3 visites | 2,07 | oui |
| R² sur le test | entre 0,5 et 0,7 | 0,59 | oui |
| Les résultats changent-ils avec un autre découpage ? | oui | MAE de 2,06 à 2,49 | oui |
| MAE moyenne en validation croisée | dans la fourchette des découpages manuels (2,06 à 2,49) | 2,22 | oui |

### Résultats (découpage random_state = 42)

| Modèle | MAE entraînement | MAE test | R² entraînement | R² test |
|---|---|---|---|---|
| Baseline (médiane = 15) | – | 3,36 | – | – |
| Régression linéaire | 2,07 | 2,29 | 0,71 | 0,59 |

Le modèle réduit l'erreur d'environ **32 %** par rapport à la baseline.

**Surapprentissage ?** L'écart entre entraînement et test est faible pour la MAE (0,22 visite). Le modèle a appris des règles générales et ne s'est pas contenté de mémoriser les abonnés d'entraînement, ce qui est attendu pour un modèle simple (24 coefficients pour 637 abonnés).

**Analyse des erreurs.** Les prédictions restent le plus souvent entre 11 et 17 visites, alors que les valeurs réelles vont de 6 à 25 sur le test. Les plus grosses erreurs (jusqu'à 9,5 visites) concernent des abonnés **extrêmes**, qui viennent très peu ou très souvent : ce qui les rend atypiques (motivation, emploi du temps, santé…) n'est pas mesuré dans les données.

---

## 4. Évaluation de la fiabilité et interprétation

### Sensibilité au découpage
Le même modèle a été évalué avec quatre découpages différents :

| random_state | Baseline (MAE test) | MAE test | R² test | R² entraînement | Gain par rapport à la baseline |
|---|---|---|---|---|---|
| 42 | 3,36 | 2,29 | 0,59 | 0,71 | 32 % |
| 1 | 3,58 | 2,18 | 0,65 | 0,70 | 39 % |
| 7 | 3,78 | 2,49 | 0,65 | 0,70 | 34 % |
| 123 | 3,14 | 2,06 | 0,60 | 0,71 | 34 % |

- La MAE du test varie de **2,06 à 2,49** selon les 160 abonnés tirés au sort.
- La baseline varie dans le même sens : les découpages où le modèle se trompe le plus sont aussi ceux où la baseline se trompe le plus. La variation vient donc de la **difficulté du jeu de test**, pas du modèle.
- Le **gain** par rapport à la baseline reste stable (environ un tiers d'erreur en moins).
- L'écart de R² observé avec random_state = 42 (0,71 contre 0,59) est en grande partie dû au découpage : avec d'autres découpages, le R² du test atteint 0,65.

Conclusion : un seul découpage donne un résultat qui dépend du hasard. Il faut une évaluation plus robuste.

### Validation croisée
Les 797 abonnés sont répartis aléatoirement en 5 parts (`KFold(n_splits=5, shuffle=True, random_state=42)`). Le modèle est entraîné 5 fois sur 4 parts et évalué sur la 5e, en changeant de part à chaque fois (`cross_val_score`). Chaque abonné est ainsi utilisé **une fois pour le test** et **quatre fois pour l'entraînement**.

| Pli | 1 | 2 | 3 | 4 | 5 | Moyenne ± écart-type |
|---|---|---|---|---|---|---|
| R² | 0,59 | 0,64 | 0,71 | 0,68 | 0,67 | **0,66 ± 0,04** |
| MAE | 2,29 | 2,26 | 2,13 | 2,09 | 2,34 | **2,22 ± 0,09** |

**Conclusion sur la fiabilité :** le modèle prédit la fréquentation mensuelle d'un abonné avec une erreur moyenne d'environ **2,2 visites**, et explique environ **deux tiers** des différences de fréquentation entre abonnés. Les faibles écarts-types montrent que ces performances sont stables et ne dépendent pas d'un découpage particulier.

### Facteurs qui influencent la fréquentation

**Coefficients bruts** (modèle entraîné sur le découpage random_state = 42) :

| Variable | Coefficient | Lecture |
|---|---|---|
| formule_Premium | +3,11 | un abonné Premium vient environ 3 fois de plus par mois qu'un abonné Confort |
| formule_Essentiel | −0,38 | un abonné Essentiel vient légèrement moins qu'un abonné Confort |
| seances_coaching | +1,98 | +2 visites environ par séance de coaching |
| reclamations | −1,12 | −1 visite environ par réclamation |
| distance_domicile_m | −0,000407 | −0,41 visite par kilomètre |
| anciennete_mois | +0,04 | +0,5 visite environ par année d'ancienneté |
| creneau_habituel_soir | +1,65 | par rapport aux créneaux « Inconnu » |
| salles (S02 à S14) | de −0,30 (S10) à −1,71 (S02) | toutes inférieures à S01 |

Toutes ces lectures s'entendent **toutes choses égales par ailleurs** (les autres variables étant fixées).

**Le piège des unités.** Un coefficient dépend de l'unité de sa variable : la distance mesurée en kilomètres aurait un coefficient 1 000 fois plus grand, pour un effet identique. Les coefficients bruts ne permettent donc pas de comparer l'importance des facteurs.

**Coefficients standardisés.** Les variables numériques ont été standardisées (`StandardScaler`) : chacune est exprimée en nombre d'écarts-types par rapport à sa moyenne. Chaque coefficient indique alors de combien de visites varie la fréquentation quand la variable augmente d'un écart habituel. Le modèle a été réentraîné sur l'ensemble des données (l'objectif ici est d'interpréter, pas d'évaluer).

| Rang | Facteur | Coefficient standardisé | Écart habituel (environ) |
|---|---|---|---|
| 1 | seances_coaching | +2,49 | 1,2 séance |
| 2 | anciennete_mois | +0,90 | 22 mois |
| 3 | distance_domicile_m | −0,84 | 2,1 km |
| 4 | reclamations | −0,75 | 0,7 réclamation |
| 5 | prix_mensuel_eur | −0,52 | non interprétable (voir limites) |

### Interprétation
- **Coaching** : c'est le facteur le plus fortement associé à la fréquentation. Ce résultat doit cependant être interprété avec prudence. D'une part, une séance de coaching se déroulant à la salle compte probablement aussi comme une visite, ce qui crée un lien en partie mécanique. D'autre part, le sens du lien n'est pas établi : le coaching pourrait motiver les abonnés à venir plus souvent, mais les abonnés les plus réguliers pourraient aussi être ceux qui choisissent de prendre du coaching.
- **Formule** : les abonnés Premium viennent nettement plus souvent, toutes choses égales par ailleurs.
- **Ancienneté, distance et réclamations** ont des effets du même ordre de grandeur. La distance, qui semblait négligeable avec son coefficient brut, est en réalité aussi importante que l'ancienneté. Cela rejoint le résultat de la question 2 : les abonnés éloignés viennent moins souvent.
- **Réclamations** : les abonnés qui se plaignent viennent moins. Le sens du lien n'est pas établi (insatisfaction qui fait moins venir, ou abonnés moins présents donc moins attachés à la salle).

### Limites
- **Multicolinéarité prix / formule.** Le prix dépend en grande partie de la formule. Le modèle « partage » leur effet entre les deux colonnes de façon arbitraire, d'où un coefficient de prix négatif qui contredit le coefficient positif de Premium. Cela ne dégrade pas les prédictions, mais empêche d'interpréter le prix seul. Piste : retirer `prix_mensuel_eur` du modèle.
- **Catégories de référence peu parlantes.** Le créneau de référence est « Inconnu » (20 abonnés), ce qui rend la lecture des coefficients de créneau difficile. Piste : choisir une référence plus représentative (par exemple « soir », le créneau le plus fréquent).
- **Coefficients des salles imprécis** : chaque salle compte 45 à 76 abonnés.
- **Facteurs non mesurés** : environ un tiers des différences de fréquentation reste inexpliqué (motivation, emploi du temps, santé…).
- **Associations, pas causes** : les coefficients décrivent des liens dans les données, pas l'effet qu'aurait une action de FitZone.

### Synthèse des questions 3 et 4
- Une régression linéaire prédit la fréquentation mensuelle avec une erreur moyenne de **2,2 visites** (validation croisée), soit environ **un tiers d'erreur en moins** qu'une prédiction constante.
- Le modèle est **stable** (faible variation entre les plis) et ne montre **pas de surapprentissage**.
- Les facteurs les plus associés à la fréquentation sont le **coaching** (avec prudence), la **formule Premium**, puis l'**ancienneté**, la **distance** et les **réclamations**.