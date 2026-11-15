# Phase 2 — Analyse des résiliations et prédiction de la fréquentation

## 1. Objectif

Cette deuxième phase du projet FitZone répond aux quatre premières questions posées par la direction.

Les deux premières portent sur la **résiliation** : comprendre ce qui sépare un abonné qui reste d'un abonné qui part, et vérifier si la distance domicile-salle explique réellement les départs.

Les deux suivantes portent sur la **fréquentation** : prédire le nombre de visites mensuelles d'un abonné qui vient de signer, et déterminer de quoi dépend cette fréquentation et avec quelle marge d'erreur.

Les analyses s'appuient sur le fichier `data/processed/FitZone_abonnes_clean.csv` produit par la phase 1, soit **797 abonnés** sans doublons ni valeurs manquantes. Parmi eux, **189 ont résilié**, soit un taux de résiliation de **23,7 %**.

L'ensemble des traitements est exécuté par `phase2.py`, qui appelle les modules `src/analyse_resiliation.py` et `src/regression.py`.

## 2. Question 1 — Qu'est-ce qui distingue un abonné qui reste d'un abonné qui part

### 2.1. Méthode retenue

Nous avons procédé en trois temps :

1. Un test de **Mann-Whitney** sur chacune des six variables numériques, pour comparer les abonnés restants et les abonnés partants.
2. Un test du **chi2 d'indépendance** sur les trois variables qualitatives : la formule, le créneau habituel et la salle.
3. Une **régression logistique multivariée** sur variables standardisées, qui estime l'effet propre de chaque variable, les autres étant tenues constantes.

À chaque test numérique nous avons ajouté une **taille d'effet**, calculée comme l'écart des moyennes divisé par l'écart-type global.

### 2.2. Pourquoi celle-là

Nous avons écarté le test de Student au profit de **Mann-Whitney** parce que le test de Student suppose des distributions normales dans chaque groupe. Or l'ancienneté et les séances de coaching sont très asymétriques : beaucoup d'abonnés récents, beaucoup d'abonnés à zéro séance. L'hypothèse de normalité est donc fausse. Mann-Whitney compare les rangs et ne suppose rien sur la forme des distributions.

Nous avons ajouté une taille d'effet parce qu'une p-value dit seulement qu'un écart est difficilement attribuable au hasard, pas qu'il est important. Avec 797 abonnés, un écart minuscule peut ressortir comme significatif.

Nous avons terminé par une **régression logistique** parce que les tests précédents sont bivariés : ils regardent une variable à la fois et ne disent pas si un effet survit au contrôle des autres. C'est exactement le point qui permet de trancher les deux théories du comité. Les variables sont standardisées, sans quoi un coefficient portant sur une distance en mètres et un coefficient portant sur un nombre de réclamations ne seraient pas comparables.

La variable `salle` n'entre pas dans le modèle multivarié : son chi2 est non significatif (p = 0,4438) et elle aurait coûté treize variables indicatrices sans rien apporter.

### 2.3. Ce qui a été vérifié

La performance du modèle a été mesurée par l'**AUC en validation croisée à 5 plis**, et non sur les données d'entraînement : un modèle évalué sur les données qui l'ont entraîné surestime toujours sa performance.

**AUC moyenne = 0,748**, avec des valeurs par pli comprises entre 0,727 et 0,759. Le modèle tient donc sur des abonnés qu'il n'a pas vus, et la faible dispersion entre les plis indique que ce résultat ne dépend pas du découpage.

Nous avons retenu l'AUC plutôt que le taux de bonnes réponses parce que les classes sont déséquilibrées : un modèle qui répondrait systématiquement « ne résilie pas » obtiendrait 76 % de bonnes réponses tout en étant parfaitement inutile.

### 2.4. Résultats

Les variables qui pèsent le plus, par coefficient standardisé décroissant en valeur absolue :

| Variable | Coefficient | Odds ratio | Lecture |
|---|---|---|---|
| Ancienneté (mois) | -0,654 | 0,52 | Divise par deux le risque de départ |
| Visites par mois | -0,541 | 0,58 | L'assiduité protège |
| Séances de coaching | -0,527 | 0,59 | Le coaching protège |
| Réclamations | +0,296 | 1,34 | Augmente le risque d'un tiers |
| Distance domicile-salle | +0,226 | 1,25 | Facteur aggravant, traité en question 2 |
| Prix mensuel | +0,094 | 1,10 | Effet quasi nul une fois les autres variables contrôlées |

Les variables étant standardisées, **chaque odds ratio correspond à une variation d'un écart-type** et non d'une unité. Pour une lecture opérationnelle, il faut donc reconvertir dans l'unité d'origine :

- l'écart-type de l'ancienneté est de 22,5 mois : **une année d'ancienneté supplémentaire réduit le risque de départ de 29 %** ;
- l'écart-type des réclamations est de 0,67 : **une réclamation supplémentaire majore le risque de départ de 56 %**.

Confondre les deux lectures reviendrait à annoncer au comité des effets deux fois trop faibles sur les variables à faible dispersion.

### 2.5. Les deux théories du comité sont réfutées

C'est le résultat central de cette question.

**Le créneau du soir ne protège pas.** Le chi2 du créneau habituel donne **p = 0,6725** : aucun lien détectable entre l'horaire de fréquentation et la résiliation. Les taux de résiliation par créneau sont tous proches les uns des autres.

| Créneau | Taux de résiliation |
|---|---|
| Midi | 19,7 % |
| Soir | 23,2 % |
| Variable | 23,9 % |
| Matin | 26,6 % |
| Inconnu | 30,0 % |

Les abonnés du soir résilient à 23,2 % contre 23,7 % pour l'ensemble des abonnés. L'écart avec le créneau du midi n'est pas distinguable du hasard. L'affirmation des responsables de salle selon laquelle les abonnés du soir seraient les plus fidèles n'est pas vérifiée par les données.

**Le prix n'est pas la cause des départs.** En analyse bivariée, l'effet semble pourtant massif : les partants payent en moyenne **30,07 €** contre **39,60 €** pour les restants, avec une taille d'effet de -0,61. Mais une fois la formule contrôlée dans le modèle multivarié, le coefficient du prix s'effondre à **+0,094**, et change même de signe.

L'explication est que ce n'est pas le prix qui agit, mais la **formule**, dont le prix n'est que le reflet :

| Formule | Taux de résiliation |
|---|---|
| Essentiel | 35,5 % |
| Confort | 19,3 % |
| Premium | 6,0 % |

Le chi2 de la formule est significatif (**p < 0,0001**). Les formules les plus chères incluent du coaching et vont de pair avec des abonnés anciens et assidus. L'écart bivarié observé sur le prix provenait de ces variables-là, pas du montant payé.

### 2.6. Conclusion et recommandation

Ce qui distingue réellement un abonné qui part, c'est une **ancienneté faible**, une **fréquentation basse**, une **absence de coaching** et la **présence de réclamations**. Ni l'horaire ni le montant payé n'interviennent une fois ces variables prises en compte.

**Recommandation.** Cibler les actions de fidélisation sur les abonnés dont l'ancienneté est faible et dont la fréquentation baisse, et non sur le créneau horaire. Concrètement :

- **Arrêter les actions commerciales fondées sur l'horaire de fréquentation** : elles reposent sur une corrélation inexistante (p = 0,6725) et consomment un budget sans effet mesurable.
- **Ne pas engager de baisse de prix dans un objectif de rétention** : le prix ne porte aucun effet propre (+0,094). Une remise générale coûterait du chiffre d'affaires sur tous les abonnés sans retenir ceux qui partent.
- **Déclencher une action dès la première réclamation** : c'est la seule variable d'alerte directement observable en temps réel par les équipes, et une réclamation supplémentaire majore le risque de départ de 56 %.
- **Traiter le coaching comme un levier de rétention** et non comme un service annexe : à ancienneté et fréquentation égales, un écart-type de coaching (1,2 séance) réduit le risque de départ de 41 %.

## 3. Question 2 — La distance domicile-salle explique-t-elle les départs

### 3.1. Méthode retenue

Trois mesures successives :

1. Un test de Mann-Whitney sur la distance entre restants et partants.
2. Le taux de résiliation par **tranche de distance**, pour vérifier si l'effet est progressif ou s'il tient à quelques valeurs extrêmes.
3. La **position de la distance dans le modèle multivarié** de la question 1.

### 3.2. Pourquoi celle-là

Un test bivarié seul aurait conclu « oui, la distance explique les départs », puisque l'écart est significatif. C'est précisément le piège que la question de la direction désigne.

Le découpage en tranches sert à vérifier que l'effet est **monotone** : si le taux de résiliation ne montait que dans la dernière tranche, l'écart global serait l'effet de quelques abonnés très éloignés et non d'une tendance de fond.

La position dans le modèle multivarié est ce qui permet de trancher entre un **facteur réel** et un **facteur dominant**. Ces deux notions sont différentes, et c'est la confusion entre elles qui produit les « histoires qu'on se raconte ».

### 3.3. Ce qui a été vérifié

L'écart est réel et significatif : les partants habitent en moyenne à **3 465 m** contre **2 933 m** pour les restants, soit **532 m de plus**, avec **p = 0,000482**.

L'effet est bien progressif sur l'ensemble de l'échelle de distance :

| Tranche | Nombre d'abonnés | Taux de résiliation |
|---|---|---|
| Moins de 1 km | 102 | 14,7 % |
| 1 à 2 km | 207 | 17,4 % |
| 2 à 3 km | 152 | 27,6 % |
| 3 à 5 km | 202 | 27,7 % |
| Plus de 5 km | 134 | 29,9 % |

Les bornes sont fermées à gauche : un abonné situé à exactement 1 000 m est compté dans la tranche « 1 à 2 km ».

Le taux double entre la première et la dernière tranche. La progression est nette jusqu'à 3 km, puis s'aplatit : au-delà, un kilomètre de plus ne change presque rien.

**Mais la distance n'arrive qu'en 5e position sur 12 dans le modèle multivarié**, avec un coefficient de +0,226 contre -0,654 pour l'ancienneté.

### 3.4. Conclusion et recommandation

La distance est un **facteur aggravant réel, mais ce n'est pas la cause des départs**. On ne se raconte donc pas entièrement une histoire : l'effet existe, il est significatif et il est progressif. Mais il pèse environ **trois fois moins que l'ancienneté** (+0,226 contre -0,654), et il est devancé par quatre variables, dont trois sur lesquelles l'entreprise peut agir directement : les visites, le coaching et les réclamations.

Présenter la distance comme la cause principale des résiliations serait une erreur de hiérarchie, et conduirait à investir dans l'implantation là où le problème est la fidélisation des premiers mois.

**Recommandation.**

- **Ne pas fonder la stratégie d'implantation sur ce seul critère.** Ouvrir une salle pour réduire la distance moyenne agirait sur le cinquième facteur de résiliation, au prix d'un investissement immobilier, là où le coaching et le suivi des premiers mois agissent sur les trois premiers à coût bien inférieur.
- **Utiliser la distance comme variable d'appoint dans un score de risque**, ce que fait la phase 3 : elle n'est pas assez forte pour décider seule, mais elle améliore le classement des abonnés à rappeler.
- **Concentrer toute action liée à l'éloignement sur le seuil des 2 km**, où le taux de résiliation passe de 17,4 % à 27,6 %. Au-delà de 3 km, l'effet est déjà saturé et une action supplémentaire ne rapporterait presque rien.

## 4. Question 3 — Prédire les visites mensuelles d'un abonné qui signe demain

### 4.1. Méthode retenue

Une **régression linéaire multiple** avec pour cible `visites_par_mois`.

Les variables explicatives sont l'ancienneté, le prix mensuel, la distance au domicile, les séances de coaching, les réclamations, ainsi que la formule et le créneau habituel transformés en variables indicatrices.

Le jeu de données est découpé en 75 % d'entraînement et **25 % de test**, soit 597 abonnés d'entraînement et **200 abonnés de test**.

### 4.2. Pourquoi celle-là

La cible est une **quantité numérique continue** : il s'agit donc d'un problème de régression et non de classification.

Nous avons retenu un modèle linéaire plutôt qu'un modèle plus puissant parce que la question 4 demande **de quoi dépend** la fréquentation. Un modèle linéaire fournit un coefficient lisible par variable, ce qu'un modèle non interprétable ne donnerait pas. La performance seule n'était donc pas le seul critère de choix.

**Précision importante : la variable `a_resilie` est volontairement exclue des variables explicatives.** La direction demande une prédiction pour un abonné qui signe demain : à cet instant, nul ne sait s'il résiliera. La conserver ferait entrer dans le modèle une information du futur, ce qui gonflerait artificiellement la performance affichée et la rendrait impossible à reproduire en situation réelle. L'identifiant `abonne_id` est également exclu : il ne porte aucune information.

### 4.3. Ce qui a été vérifié

Trois vérifications successives.

**Un jeu de test de 200 abonnés jamais vus** à l'entraînement, pour mesurer une capacité à prédire et non à réciter.

**Une validation croisée à 5 plis** en complément, parce qu'un découpage unique peut être chanceux ou malchanceux. L'écart-type obtenu indique à quel point le résultat dépend du découpage.

**Une comparaison à un modèle naïf** qui prédirait toujours la moyenne. Un R2 ou une MAE seuls ne disent pas si un modèle sert à quelque chose : il faut un point de comparaison.

| Mesure | Jeu de test | Validation croisée 5 plis |
|---|---|---|
| R2 | 0,623 | 0,663 ± 0,041 |
| MAE | 2,29 visites | 2,20 ± 0,09 visites |
| RMSE | 2,81 visites | — |

Le modèle naïf obtient une **MAE de 3,48 visites**. Le modèle réduit donc l'erreur moyenne de **34 %**.

La validation croisée donne un R2 légèrement supérieur à celui du jeu de test unique (0,663 contre 0,623), avec un écart-type de 0,041. Le découpage de test se trouvait donc du côté défavorable, et les chiffres annoncés sont plutôt prudents.

### 4.4. Conclusion et recommandation

Le modèle explique **62 % de la variance** de la fréquentation sur des abonnés jamais vus, et prédit les visites mensuelles d'un nouvel abonné à **2,3 visites près en moyenne**, contre 3,5 visites pour la moyenne simple.

**Recommandation.** Dimensionner les plannings de coachs sur la prédiction du modèle plutôt que sur la moyenne actuellement utilisée : le gain est de **34 % d'erreur en moins**, sans coût supplémentaire puisque toutes les variables nécessaires sont connues dès la signature du contrat.

Concrètement, le modèle est utilisable dès le jour de la signature : aucune de ses variables ne demande d'attendre l'historique de fréquentation de l'abonné. Il peut donc servir à répartir les nouveaux abonnés entre les salles et les créneaux dès leur inscription.

## 5. Question 4 — De quoi dépend la fréquentation et avec quelle marge d'erreur

### 5.1. Méthode retenue

Les **coefficients standardisés** de la régression linéaire, obtenus en appliquant un StandardScaler aux variables explicatives avant l'ajustement, puis triés par valeur absolue décroissante.

### 5.2. Pourquoi celle-là

Les coefficients bruts sont exprimés dans l'unité de chaque variable : celui de la distance se lit en visites par mètre, celui du coaching en visites par séance. **Ils ne sont pas comparables entre eux.**

Après standardisation, chaque coefficient se lit « variation de la fréquentation lorsque la variable augmente d'un écart-type », ce qui permet enfin de les classer. Nous affichons l'écart-type de la cible à côté, faute de quoi il serait impossible de juger si un coefficient est grand ou petit.

### 5.3. Résultats

| Variable | Coefficient standardisé |
|---|---|
| Séances de coaching | **+2,354** |
| Formule Premium | +1,448 |
| Créneau du soir | +0,924 |
| Distance domicile-salle | -0,916 |
| Ancienneté | +0,820 |
| Réclamations | -0,730 |
| Prix mensuel | -0,515 |

Écart-type des visites observées : **4,72 visites par mois**.

Le coaching domine très largement : un écart-type de séances de coaching vaut à lui seul **la moitié d'un écart-type de fréquentation**. Il pèse 1,6 fois plus que la variable suivante.

On note que le créneau du soir, qui n'avait **aucun effet sur la résiliation** (question 1), a bien un effet sur la **fréquentation** : les abonnés du soir viennent davantage, mais ils ne restent pas plus longtemps. Les deux questions ne portent pas sur la même chose, et c'est une confusion à éviter dans la lecture des résultats.

### 5.4. La réponse à retenir pour la direction

**La marge d'erreur est de ± 2,3 visites par mois.**

C'est ce chiffre qui sert à dimensionner, et non le R2. Un R2 de 0,623 est une mesure de qualité statistique qui ne se traduit en aucune décision opérationnelle. La MAE, elle, se lit directement : lorsque le modèle annonce 14 visites, il faut lire « entre 12 et 16 ».

La RMSE de 2,81 est supérieure à la MAE de 2,29, ce qui indique la présence de quelques erreurs importantes. Le modèle se trompe rarement beaucoup, mais cela arrive : une prédiction individuelle ne doit jamais être annoncée comme un chiffre exact.

### 5.5. Conclusion et recommandation

La fréquentation dépend d'abord du **coaching**, loin devant tout le reste, puis de la formule et du créneau, et négativement de la distance et des réclamations.

**Recommandation.**

- **Prévoir les plannings avec une marge de 2 à 3 visites par abonné et par mois.** Dimensionner au chiffre exact conduirait à sous-doter une salle sur deux.
- **Augmenter le volume de coaching proposé**, puisqu'il est à la fois le premier levier de fréquentation (+2,354) et un facteur de rétention (odds ratio 0,59 en question 1). C'est la seule variable du projet qui agit favorablement sur les deux objectifs à la fois, et elle est entièrement sous le contrôle de l'entreprise, contrairement à la distance ou à l'ancienneté.
- **Ne pas chercher à augmenter la fréquentation par le prix** : son coefficient est négatif (-0,515) et le plus faible du tableau. Ce signe reflète le fait que les abonnés des formules les moins chères viennent moins, pas que baisser le prix ferait venir davantage.

## 6. Point de vigilance sur la lecture des coefficients

Un résultat du modèle logistique de la question 1 peut surprendre et doit être expliqué avant d'être présenté à la direction.

**Le coefficient de la formule Premium est positif (+0,205), alors que Premium affiche le taux de résiliation le plus bas du jeu de données (6,0 %).**

Ce n'est pas une erreur. C'est un effet classique de la régression multivariée. Le modèle n'estime pas l'effet brut de la formule, mais son effet **une fois l'ancienneté, les visites et le coaching tenus constants**. Or ces trois variables portent déjà presque toute l'information que contient la formule : un abonné Premium est typiquement ancien, assidu et coaché. Une fois ces caractéristiques fixées, le fait d'être Premium n'apporte plus d'information, et le signe du coefficient devient instable.

C'est exactement le même mécanisme qui fait passer le **prix de -0,61 en bivarié à +0,094 en multivarié**, et c'est précisément ce qui réfute l'hypothèse du prix formulée par le comité.

La règle de lecture à retenir est la suivante : **un coefficient multivarié ne se lit jamais comme un taux observé.** Le taux de résiliation de 6,0 % des abonnés Premium reste parfaitement exact ; il décrit simplement un autre objet que le coefficient.

## 7. Conclusion générale de la phase 2

Les quatre questions ont été traitées avec des méthodes choisies pour la nature de la donnée et pour l'usage attendu du résultat, et non pour leur performance brute.

| Question | Réponse en une ligne | Mesure de confiance |
|---|---|---|
| Q1 — Qui part | Ancienneté faible, peu de visites, pas de coaching, réclamations | AUC 0,748 en validation croisée |
| Q2 — La distance | Facteur réel mais secondaire, 5e sur 12 | p = 0,000482, effet monotone |
| Q3 — Combien de visites | ± 2,3 visites par mois | R2 0,623 sur 200 abonnés non vus |
| Q4 — De quoi ça dépend | Le coaching, loin devant | Coefficient +2,354 pour un écart-type de 4,72 |

Les deux théories avancées par le comité — le créneau du soir et le prix — sont réfutées par les données. Le levier qui ressort des quatre questions est le **coaching**, qui agit simultanément sur la fréquentation et sur la rétention.

La phase 3 part de ces résultats pour passer de l'explication à la décision : quels abonnés appeler, et jusqu'où élargir l'équipe chargée de les appeler.
