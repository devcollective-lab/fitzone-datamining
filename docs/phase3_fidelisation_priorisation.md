# Phase 3 : Fidélisation et priorisation des appels

## 5. Quels abonnés appeler en priorité ?

### Le problème
Chaque mois, 400 abonnés arrivent en fin d'engagement, et l'équipe ne peut en appeler que 80. Appeler au hasard reviendrait à contacter surtout des abonnés qui seraient restés de toute façon. Il faut donc estimer le **risque de résiliation** de chaque abonné, puis appeler les 80 plus risqués.

### Choix de la méthode
- Un modèle qui répond seulement « va partir » ou « va rester » ne permet pas de choisir exactement 80 abonnés : tous ceux classés « va partir » seraient à égalité. Il faut un modèle qui donne une **probabilité** de résiliation, pour **trier** les abonnés.
- La **régression logistique** répond à ce besoin : c'est un modèle de classification qui calcule une formule à partir des variables, puis la transforme en probabilité entre 0 et 1.
- Le modèle est intégré dans une chaîne (`make_pipeline`) avec une standardisation (`StandardScaler`), pour que toutes les variables soient à la même échelle. La standardisation est calculée uniquement sur les données d'entraînement, ce qui évite qu'une information du test ne fuie dans l'entraînement.

### Variables utilisées
- Cible : `a_resilie`.
- Entrées : toutes les informations connues pour un abonné en fin d'engagement, y compris son historique (`visites_par_mois`, `seances_coaching`, `reclamations`, `anciennete_mois`), ainsi que la formule, le prix, la distance, le créneau et la salle (one-hot encoding, comme en phase 2).
- Exclus : `abonne_id` (simple étiquette) et les colonnes créées pendant l'analyse.

### Pourquoi le taux de bonnes réponses ne suffit pas
Un modèle qui répondrait « va rester » pour tout le monde aurait raison dans 76 % des cas, sans repérer un seul abonné sur le départ. Quand une catégorie est minoritaire (23,7 % de résiliés), le pourcentage de bonnes réponses est trompeur. Le modèle est donc évalué sur la question réelle : **parmi les abonnés désignés comme les plus risqués, combien partent vraiment ?**

Deux mesures sont utilisées :
- **la précision** : parmi les abonnés appelés, quelle part allait vraiment partir ?
- **le rappel** : parmi tous les abonnés qui allaient partir, quelle part a été appelée ?

### Évaluation
**Premier test** (découpage 80/20 avec `stratify=y`, pour garder 23,7 % de résiliés dans chaque partie) : parmi les 32 abonnés les plus risqués du test (20 % de 160), **15** ont réellement résilié, contre environ 8 si on les avait choisis au hasard.

**Validation croisée.** Pour ne pas dépendre d'un seul découpage, le risque de chaque abonné a été estimé par validation croisée en 5 plis (`StratifiedKFold` et `cross_val_predict`) : chacun des 797 abonnés reçoit un risque calculé par un modèle qui ne l'a pas vu pendant son entraînement.

| Abonnés appelés (les plus risqués) | Résiliés atteints | Rappel | Précision |
|---|---|---|---|
| 10 % (80) | 44 | 23 % | 55 % |
| **20 % (159)** | **78** | **41 %** | **49 %** |
| 30 % (239) | 104 | 55 % | 44 % |
| **40 % (319)** | **130** | **69 %** | **41 %** |
| 50 % (398) | 148 | 78 % | 37 % |
| 60 % (478) | 157 | 83 % | 33 % |
| 80 % (638) | 178 | 94 % | 28 % |
| 100 % (797) | 189 | 100 % | 24 % |

Ces résultats confirment ceux du premier test (rappel de 39 % et précision de 47 % à 20 %).

### Réponse
En appelant les 20 % d'abonnés les plus risqués, FitZone atteint **41 % des futurs résiliés**, au lieu de 20 % en appelant au hasard : le modèle rend les appels environ **deux fois plus efficaces**. Près d'**un appel sur deux** (49 %) tombe sur un abonné qui allait réellement partir.

Concrètement, chaque mois : appliquer le modèle aux 400 abonnés en fin d'engagement, les trier par risque décroissant, et appeler les 80 premiers. Sur 400 abonnés, environ 95 s'apprêtent à partir (23,7 %) ; les 80 appels en atteignent environ **39**.

---

## 6. Faut-il doubler l'équipe d'appel ?

### Résiliés atteints
| Équipe | Appels sur 400 | Futurs résiliés atteints |
|---|---|---|
| Actuelle | 80 (20 %) | 39 |
| Doublée | 160 (40 %) | 65 |
| **Les 80 appels supplémentaires** | +80 | **+26** |

Doubler l'équipe ne double pas les résultats : on passe de 39 à 65 résiliés atteints (× 1,67). Les appels supplémentaires vont à des abonnés **moins risqués** que les premiers : la précision passe de 49 % pour les 80 premiers appels à environ 33 % pour les 80 suivants. C'est un phénomène de **rendements décroissants** : chaque appel supplémentaire rapporte un peu moins que le précédent.

### Hypothèses économiques
Le sujet ne fournit pas ces chiffres : ils ont été estimés, et la conclusion est testée sous plusieurs scénarios.

| Hypothèse | Valeur | Justification |
|---|---|---|
| Taux de succès d'un appel | 1/3 (testé à 15 % et 50 %) | estimation, à condition de proposer une offre adaptée à l'abonné |
| Prix mensuel d'un abonné retenu | 30,07 € | prix moyen observé chez les résiliés, majoritairement en formule Essentiel (et non le prix moyen de tous les abonnés, 37 €) |
| Durée supplémentaire d'abonnement | 3 mois | hypothèse prudente : un abonné retenu reste fragile |
| Coût d'un appel | 5 € | 10 à 15 minutes de travail d'un salarié, à 25-30 € de l'heure charges comprises |

Formule : **gain net = (résiliés atteints × taux de succès × prix mensuel × durée) − (nombre d'appels × coût d'un appel)**

### Résultats

| Taux de succès | Gain net, 80 appels | Gain net, 160 appels | Les 80 appels supplémentaires |
|---|---|---|---|
| Prudent (15 %) | + 130 € | + 83 € | **− 47 €** |
| **Principal (1/3)** | **+ 777 €** | **+ 1 162 €** | **+ 385 €** |
| Optimiste (50 %) | + 1 366 € | + 2 143 € | + 777 € |

**Seuils de rentabilité :**
- la campagne actuelle (80 appels) est rentable dès que **11 %** des futurs résiliés appelés acceptent de rester ;
- les 80 appels supplémentaires ne sont rentables qu'à partir de **17 %**.

### Réponse
Doubler l'équipe d'appel ne permet pas de récupérer deux fois plus d'abonnés. Les 80 appels supplémentaires atteignent 26 futurs résiliés, contre 39 pour les 80 premiers. Dans le scénario principal, la campagne actuelle rapporte environ **780 € par mois**, et l'élargissement n'ajoute qu'environ **385 €**, soit deux fois moins pour le même coût. Dans le scénario prudent, il fait même perdre de l'argent.

La campagne actuelle est rentable dans tous les scénarios. L'élargissement ne l'est que si plus de 17 % des abonnés appelés acceptent de rester.

**Recommandation :** avant de doubler l'équipe, mesurer pendant un ou deux mois le taux de succès réel des 80 appels actuels. S'il dépasse 17 %, l'élargissement est rentable ; sinon, il vaut mieux garder l'équipe actuelle et cibler ses appels avec le modèle.

### Limites
- **Les hypothèses économiques sont des estimations**, en particulier le taux de succès d'un appel, qui détermine la rentabilité de l'élargissement.
- **Le coût de l'offre** proposée pendant l'appel (mois offert, séance gratuite…) n'est pas inclus. Il réduirait les gains.
- **Le modèle est entraîné sur l'ensemble des abonnés**, pas uniquement sur des abonnés en fin d'engagement. On suppose que les 400 abonnés du mois ressemblent au reste de la base, avec le même taux de résiliation (23,7 %).
- **L'ancienneté est en partie biaisée** (le compteur s'arrête au départ d'un résilié, voir phase 2). Le modèle peut en partie s'appuyer sur ce biais.
- **Le gain est estimé à court terme** (3 mois). Un abonné retenu plus longtemps rapporterait davantage.
