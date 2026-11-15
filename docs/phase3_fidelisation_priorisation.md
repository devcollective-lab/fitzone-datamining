# Phase 3 — Fidélisation et priorisation des appels de rétention

## 1. Objectif

Cette troisième phase répond aux deux dernières questions de la direction. Elle marque un changement de nature : les phases 1 et 2 expliquaient, celle-ci **décide**.

- **Question 5** : chaque mois, 400 abonnés arrivent en fin d'engagement et l'équipe ne peut en appeler que 80. Lesquels ?
- **Question 6** : si l'équipe d'appel est doublée le mois prochain, récupère-t-on deux fois plus de monde ?

Le traitement est exécuté par `phase3.py`, qui appelle deux modules aux rôles volontairement séparés :

- `src/classification.py` attribue un risque de résiliation à chaque abonné de la cohorte. Il ne décide rien.
- `src/evaluation.py` transforme ces risques en ordre d'appels, en euros et en gain marginal. Il ne modélise rien.

Cette séparation est voulue : le jour où le modèle de score change, la partie économique n'a pas à être rouverte, et le jour où la direction conteste le coût d'un appel, le modèle n'a pas à être réentraîné.

## 2. Hypothèses de travail

Les montants en euros présentés dans cette phase ne sont pas des mesures : ce sont des **projections construites sur quatre hypothèses explicites**. Si l'une change, tous les montants changent. Elles sont donc énoncées ici, avant tout résultat.

### 2.1. La cohorte de 400 abonnés est simulée

Le fichier nettoyé **ne contient aucune date de fin d'engagement**. Il est donc impossible de reconstituer la véritable cohorte mensuelle décrite par la direction.

Nous la simulons par un **tirage stratifié de 400 abonnés**, le reste servant à l'entraînement du modèle. La stratification garantit que la cohorte simulée présente le même taux de résiliation que la population totale : sans elle, le tirage pourrait produire une cohorte anormalement saine ou anormalement à risque, et toute la rentabilité calculée dépendrait de ce hasard.

Cette simulation suppose que la cohorte d'un mois donné est un échantillon représentatif de l'ensemble des abonnés. C'est défendable, rien n'indiquant que les fins d'engagement se concentrent sur un profil particulier, mais **cela reste à vérifier le jour où une date d'engagement sera disponible**. Si les fins d'engagement étaient saisonnières, ou concentrées sur les abonnés entrés en promotion, les résultats de cette phase seraient optimistes.

### 2.2. Le taux de sauvetage d'un appel est de 25 %

Un appel passé à un abonné qui allait partir ne le retient pas toujours. Les benchmarks du secteur situent le taux de sauvetage d'une équipe formée **entre 15 et 25 % des demandes de résiliation**, et **jusqu'à 25 à 55 %** lorsque l'appel s'accompagne d'une offre de rétention forte (remise, mois offerts, changement de formule).

Rien n'indiquant que FitZone dispose d'une telle offre, nous retenons **25 %, borne haute du cas sans offre commerciale**. C'est donc une hypothèse prudente : avec une offre de rétention, le taux réel serait supérieur et la rentabilité calculée ici serait sous-estimée.

Ce taux ne s'applique qu'aux abonnés **qui allaient effectivement résilier**. Appeler un abonné fidèle ne sauve rien, puisqu'il n'y avait rien à sauver. C'est tout l'enjeu du classement.

### 2.3. Le coût d'un appel est de 8 €

Temps de l'agent, outil téléphonique et encadrement. Ce coût est payé pour **chaque appel**, qu'il aboutisse ou non, et que l'abonné soit à risque ou non. C'est ce qui fait qu'appeler davantage n'est pas gratuit, et c'est le cœur de la question 6.

### 2.4. Un abonné sauvé vaut son prix mensuel multiplié par 12

Hypothèse volontairement simple et plutôt conservatrice : elle ignore qu'un abonné retenu peut rester plusieurs années, mais elle ignore aussi le coût de la remise éventuellement consentie pour le retenir.

Nous utilisons le **prix réel de chaque abonné** et non un prix moyen : c'est ce qui permet au second critère de priorisation d'exister.

## 3. Question 5 — Quels 80 abonnés appeler parmi 400

### 3.1. Méthode retenue

Une **régression logistique** produit la probabilité de résiliation de chaque abonné de la cohorte. Cette probabilité sert ensuite à classer les 400 abonnés selon **deux critères comparés** :

- **Critère (a), tri par risque** : probabilité de résiliation décroissante.
- **Critère (b), tri par valeur espérée** : probabilité × prix mensuel × 12.

Les 80 premiers du classement retenu constituent la liste d'appels.

### 3.2. Pourquoi celle-là

**Pourquoi une régression logistique plutôt qu'un arbre de décision ou une forêt aléatoire**, pour trois raisons liées à l'usage réel :

1. **Nous avons besoin d'un classement, pas d'une décision binaire.** La question n'est pas « cet abonné va-t-il résilier ? » mais « parmi 400 abonnés, lesquels sont les 80 plus prioritaires ? ». Il faut donc une probabilité continue, qui se trie. Un arbre de décision range les abonnés dans un petit nombre de feuilles et attribue la même probabilité à tous les abonnés d'une même feuille : il produirait des paquets d'ex æquo qu'il faudrait départager au hasard.

2. **La probabilité doit être calibrée**, c'est-à-dire utilisable comme un véritable pourcentage, puisque nous la multiplions ensuite par un chiffre d'affaires pour calculer une valeur espérée. La régression logistique optimise directement la vraisemblance et produit des probabilités proches des fréquences observées. Une forêt aléatoire, qui moyenne des votes d'arbres, a tendance à tasser ses probabilités vers le centre : le classement resterait correct mais les euros calculés dessus seraient faux.

3. **Le modèle doit être explicable au comité.** Chaque coefficient se lit comme un effet, et la phase 2 a déjà établi lesquels pèsent. Il faut pouvoir dire à un responsable de salle pourquoi tel abonné figure dans la liste des 80. Une forêt de centaines d'arbres ne se raconte pas.

**Pourquoi comparer deux critères** plutôt que d'en choisir un d'emblée : ce sont deux objectifs différents, et rien ne garantissait à l'avance lequel l'emporterait. La phase 2 a montré que les abonnés à risque sont justement ceux qui payent le moins ; les deux critères pouvaient donc parfaitement se contredire.

### 3.3. Ce qui a été vérifié

**Le StandardScaler est ajusté uniquement sur le jeu d'entraînement**, puis appliqué à la cohorte. L'ajuster sur l'ensemble des données ferait entrer dans l'entraînement les moyennes et écarts-types de la cohorte, soit une information dont on ne dispose pas le jour où l'on score de vrais abonnés à venir. La performance mesurée serait alors meilleure que celle obtenue en situation réelle.

| Contrôle | Valeur |
|---|---|
| AUC sur la cohorte | **0,745** |
| Taux de résiliation de base | **23,75 %** |
| Résiliants dans la cohorte | **95 sur 400** |
| Abonnés d'entraînement | 397 |

L'AUC de 0,745 sur la cohorte est cohérente avec les 0,748 obtenus en validation croisée en phase 2 : le modèle ne s'effondre pas sur des abonnés qu'il n'a jamais vus.

Le risque prédit s'étale de 0,001 à 0,844, avec une médiane à 0,160. Cet étalement est ce qui rend un classement utile : si tous les abonnés présentaient le même risque, aucune priorisation ne serait possible et l'équipe d'appel vaudrait un tirage au sort.

### 3.4. Comparaison des deux critères au top 80

| Indicateur | Tri par risque | Tri par valeur espérée | Écart |
|---|---|---|---|
| Partants atteints | 38 | **39** | +1 |
| Précision | 0,475 | **0,487** | +0,012 |
| Lift contre le hasard | 2,00 | **2,05** | +0,05 |
| Couverture des partants | 40,0 % | **41,1 %** | +1,1 pt |
| CA préservé | 2 950 € | **3 292 €** | +342 € |
| Coût des appels | 640 € | 640 € | — |
| **Gain net** | **2 310 €** | **2 652 €** | **+342 €** |
| ROI | 4,6x | **5,1x** | +0,5 |

Le tri par valeur espérée l'emporte **sur les deux objectifs à la fois** : il atteint un partant de plus *et* préserve 342 € de chiffre d'affaires supplémentaire. Il n'y avait donc aucun arbitrage à faire entre nombre d'abonnés retenus et euros préservés.

**Les deux listes n'ont que 65 abonnés communs sur 80**, soit 81 %. Le choix du critère n'est pas cosmétique : il change effectivement quinze personnes à appeler.

### 3.5. Profil des 80 prioritaires

| Variable | Top 80 prioritaires | Cohorte entière |
|---|---|---|
| Ancienneté | **10,8 mois** | 29,4 mois |
| Visites par mois | **11,3** | 16,3 |
| Séances de coaching | **0,2** | 0,9 |
| Réclamations | **0,8** | 0,4 |
| Distance domicile-salle | **3 868 m** | 3 127 m |
| Prix mensuel | **25,8 €** | 37,7 € |

Autrement dit : des abonnés **récents, peu assidus, sans coaching, qui se plaignent, éloignés et sur la formule la moins chère**.

Le chiffre du coaching mérite d'être lu en valeur absolue : les 80 abonnés prioritaires totalisent **12 séances de coaching à eux tous**. Ce n'est pas une moyenne faible, c'est une quasi-absence.

Ce profil est strictement cohérent avec les conclusions de la phase 2. Le modèle n'a rien deviné : il a appris le profil du partant établi à la question 1, et il l'applique abonné par abonné. C'est une vérification utile, car un profil des prioritaires qui aurait contredit la phase 2 aurait signalé une erreur dans la chaîne de traitement.

### 3.6. Conclusion et recommandation

**Recommandation : appeler les 80 abonnés listés dans `outputs/results/q5_top80_a_appeler.csv`, triés par valeur espérée décroissante.** L'ordre des lignes du fichier est l'ordre d'appel recommandé.

Cette liste touche **39 des 95 futurs partants de la cohorte**, soit 41 % d'entre eux avec seulement 20 % des appels possibles. C'est **deux fois mieux qu'une liste tirée au sort**, qui n'atteindrait que 19 partants pour le même budget de **640 €**.

Deux précisions opérationnelles :

- **Appeler dans l'ordre du fichier, et non dans un ordre choisi par les salles.** L'intérêt du classement disparaît si les 80 appels sont passés dans un ordre arbitraire ; en cas d'interruption à mi-parcours, seuls les premiers appels auront été les plus rentables.
- **Ne pas utiliser ce score pour refuser un service ou cibler une hausse de prix.** Il identifie des abonnés à retenir, pas des abonnés à faible valeur. Son usage doit rester la rétention.

## 4. Question 6 — Doubler l'équipe d'appel rapporte-t-il deux fois plus

### 4.1. Méthode retenue

Une **courbe de gain cumulé** sur l'ensemble de la cohorte, et le calcul du **gain marginal par tranche de 80 appels supplémentaires**, aux paliers 80, 160, 240, 320 et 400.

Les deux figures correspondantes sont `outputs/figures/phase3_courbe_gain_cumule.png` et `outputs/figures/phase3_gain_marginal.png`.

### 4.2. Pourquoi celle-là

La question porte sur un **rendement marginal**, et non sur une performance globale. Une métrique moyenne y répondrait faux.

C'est le point méthodologique central de cette question : le gain **cumulé** monte presque toujours quand on appelle davantage, et ne dit donc rien du rendement de la tranche ajoutée. Seule la **différence entre deux paliers** permet de répondre à « est-ce que la tranche suivante vaut son coût ? ». Présenter le cumul à la direction conduirait mécaniquement à recommander d'appeler toute la cohorte, ce que les chiffres contredisent.

### 4.3. Réponse directe : non

| Capacité | Partants atteints | Précision | Gain net |
|---|---|---|---|
| 80 appels | 38 | 0,475 | 2 310 € |
| 160 appels | 63 | 0,394 | 3 770 € |
| Rapport | **× 1,66** | -0,081 | **× 1,63** |

Doubler l'équipe fait passer les partants atteints de 38 à 63, soit **× 1,66 et non × 2**, et le gain net de 2 310 € à 3 770 €, soit **× 1,63**. La précision tombe de 0,475 à 0,394.

La raison est simple : **le coût des appels est linéaire, le gain ne l'est pas.** Les abonnés les plus à risque sont appelés en premier ; chaque tranche suivante tombe donc sur des abonnés de moins en moins susceptibles de partir, pendant que les 8 € par appel restent dus.

### 4.4. Gain marginal par tranche de 80 appels

| Tranche | Partants en plus | Gain net de la tranche | Gain net cumulé |
|---|---|---|---|
| 0 à 80 | +38 | +2 310 € | 2 310 € |
| 80 à 160 | +25 | +1 460 € | 3 770 € |
| 160 à 240 | +17 | +1 120 € | 4 890 € |
| 240 à 320 | +12 | +1 060 € | 5 950 € |
| 320 à 400 | +3 | **-261 €** | 5 689 € |

### 4.5. Le résultat le plus important : la 5e tranche détruit de la valeur

Le rendement n'est pas seulement décroissant, il devient **négatif**.

Les appels 320 à 400 ne touchent que **3 partants supplémentaires** pour **640 € de coût**, soit **-261 € de gain net** sur la tranche. Le gain net cumulé **culmine à 320 appels (5 950 €) et redescend à 5 689 €** si l'on appelle toute la cohorte.

Autrement dit, la réponse à la question 6 n'est pas « on récupère moins du double » : c'est **« il existe un optimum, et il se situe avant la saturation de la cohorte »**. Les 80 derniers appels coûtent plus cher que ce qu'ils rapportent, parce qu'à ce stade il ne reste presque plus de partants à trouver.

### 4.6. Un point à connaître sur le choix du critère

Le critère optimal **dépend de la capacité d'appel**, ce qui n'allait pas de soi.

| Capacité | Gain net, tri par risque | Gain net, tri par valeur espérée |
|---|---|---|
| 80 | 2 310 € | **2 652 €** |
| 160 | 3 770 € | **4 396 €** |
| 240 | 4 890 € | **5 254 €** |
| 320 | **5 950 €** | 5 842 € |
| 400 | 5 689 € | 5 689 € |

Le tri par valeur espérée domine jusqu'à 240 appels, mais le tri par risque reprend l'avantage à 320. L'explication tient à ce que chaque critère optimise : la valeur espérée privilégie les abonnés chers et capte donc le chiffre d'affaires le plus vite, tandis que le tri par risque finit par atteindre davantage de partants au total (92 contre 91 à 320 appels). À capacité élevée, c'est le nombre qui l'emporte sur le prix unitaire.

Les deux critères convergent nécessairement à 400 appels, puisque toute la cohorte est alors appelée quel que soit l'ordre.

### 4.7. Conclusion et recommandation

**Recommandation : élargir l'équipe d'appel, mais ne pas dépasser 320 appels par mois.**

L'optimum économique se situe à **320 appels pour 5 950 € de gain net mensuel**, soit environ **71 400 € par an** si la direction confirme l'hypothèse d'une cohorte de 400 abonnés en fin d'engagement chaque mois.

Trois précisions qui conditionnent cette recommandation :

- **Décider chaque tranche de 80 sur son gain marginal, jamais sur le gain cumulé.** Le cumul monte presque toujours et conduirait à appeler toute la cohorte, ce qui coûterait 261 € par mois.
- **Au-delà de 240 appels, basculer du tri par valeur espérée au tri par risque** (section 4.6). À 80 appels, le critère recommandé reste la valeur espérée.
- **Réexaminer ces seuils si le taux de sauvetage réel s'écarte de 25 %.** L'optimum dépend directement de cette hypothèse : un taux plus faible rapprocherait le point de retournement, un taux plus élevé, obtenu avec une offre de rétention, le repousserait. Mesurer le taux de sauvetage effectif dès le premier mois d'application est la vérification la plus rentable à mettre en place.

## 5. Conclusion générale de la phase 3

| Question | Réponse en une ligne | Chiffre à retenir |
|---|---|---|
| Q5 — Qui appeler | Les 80 abonnés du fichier, triés par valeur espérée | 39 partants sur 95 touchés, 2 652 € net, ROI 5,1x |
| Q6 — Doubler l'équipe | Non : × 1,63 et non × 2, avec un optimum à 320 appels | 5 950 € net mensuel au maximum |

La phase 3 convertit les conclusions explicatives de la phase 2 en décisions chiffrées. Le modèle ne remplace pas le jugement de l'équipe : avec une AUC de 0,745, il se trompe encore, et une précision de 0,475 signifie qu'**un appel sur deux est passé à un abonné qui n'allait pas partir**. Sa valeur n'est pas d'être exact, mais d'être **deux fois meilleur que le hasard** pour un coût nul, puisque toutes les données nécessaires sont déjà dans le système d'information.

La limite principale reste celle énoncée en section 2.1 : tant qu'aucune date de fin d'engagement ne figure dans les données, la cohorte mensuelle est une hypothèse et non une observation. C'est la première donnée à collecter pour consolider l'ensemble de cette phase.
