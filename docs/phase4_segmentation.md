# Phase 4 : Segmentation et détection des anomalies

## 7. Combien de types d'abonnés, et à quoi ressemble chacun ?

### Méthode
Il n'existe pas de colonne « type d'abonné » à prédire : les groupes doivent être découverts dans les données. C'est un problème d'apprentissage **non supervisé**, traité avec l'algorithme **k-means** :
1. on choisit un nombre de groupes k ;
2. l'algorithme place k centres ;
3. chaque abonné rejoint le centre le plus proche ;
4. chaque centre se déplace au milieu de son groupe ;
5. les étapes 3 et 4 sont répétées jusqu'à stabilisation.

### Variables utilisées
- **Variables de regroupement** : `anciennete_mois`, `prix_mensuel_eur`, `distance_domicile_m`, `visites_par_mois`, `seances_coaching`, `reclamations`.
- **Standardisation** (`StandardScaler`) : k-means regroupe les abonnés selon la distance qui les sépare. Sans standardisation, un écart de 500 mètres pèserait 125 fois plus qu'un écart de 4 réclamations, et les groupes seraient formés presque uniquement selon la distance.
- **Variables exclues du regroupement** :
  - `formule` : redondante avec le prix ;
  - `creneau_habituel` et `salle` : observées après coup dans chaque groupe ;
  - `a_resilie` : les groupes doivent décrire des abonnés actuels, dont on ignore s'ils vont partir. La résiliation est observée **après** la formation des groupes, pour découvrir si certains profils partent plus que d'autres.

### Choix du nombre de groupes
Le marketing souhaite quatre messages, mais le nombre de groupes a été vérifié dans les données, pour k allant de 2 à 8 (`n_init=10`, `random_state=42`) :
- **l'inertie** mesure à quel point les groupes sont serrés (plus elle est basse, mieux c'est, mais elle baisse toujours quand on ajoute des groupes) ;
- **le score de silhouette** (de −1 à 1) mesure à quel point les groupes sont bien séparés.

| k | Inertie | Silhouette |
|---|---|---|
| 2 | 2 983 | **0,429** |
| 3 | 2 483 | 0,276 |
| 4 | 2 180 | 0,268 |
| 5 | 1 946 | 0,253 |
| 6 | 1 802 | 0,216 |
| 7 | 1 695 | 0,221 |
| 8 | 1 574 | 0,223 |

- La silhouette est nettement plus élevée pour **k = 2** : la base se sépare clairement en deux grands blocs.
- Pour k = 3 à 5, la silhouette reste proche (0,25 à 0,28) : des sous-groupes existent, mais ils se chevauchent en partie.
- L'inertie ne présente pas de coude net ; ses baisses diminuent nettement au-delà de 5 groupes.

**Avec k = 2**, les deux blocs sont les **Premium** (183 abonnés, dont 178 Premium) et **tous les autres** (614 abonnés, Essentiel et Confort). Les Premium paient deux fois plus, sont inscrits depuis trois fois plus longtemps, viennent plus souvent et font davantage de coaching. La distance et les réclamations sont identiques dans les deux blocs.

**Choix retenu : k = 4.** Sa silhouette est presque équivalente à celle de k = 3 (0,268 contre 0,276), et il correspond au besoin du marketing. Les frontières entre les trois groupes non-Premium restent cependant moins nettes que la séparation Premium / non-Premium.

### Les quatre profils

| Groupe | Effectif | Caractéristiques | Résiliation |
|---|---|---|---|
| **Les réguliers de proximité** | 307 (39 %) | aucune réclamation, habitent près (2,1 km), 15 visites/mois, Essentiel et Confort | 18 % |
| **Les fidèles Premium** | 170 (21 %) | formule Premium (62 €), 5 ans d'ancienneté, 22 visites/mois, 2,4 séances de coaching | **6 %** |
| **Les insatisfaits** | 192 (24 %) | 1,3 réclamation en moyenne, 14 visites/mois, Essentiel et Confort | **39 %** |
| **Les éloignés** | 128 (16 %) | habitent loin (6,4 km), 13 visites/mois, Essentiel et Confort | **38 %** |

### Réponse
La base se divise d'abord en deux grands types : les **Premium** et **les autres**. Parmi les non-Premium, trois profils se distinguent par la distance et les réclamations, les deux facteurs de résiliation identifiés en phase 2.

Les insatisfaits et les éloignés partent deux fois plus que la moyenne, mais pour des **raisons différentes** : ils appellent donc des messages différents. Aux insatisfaits, une réponse sur la qualité du service ; aux éloignés, une réponse sur l'accessibilité (horaires, parking, transfert vers une salle plus proche).

---

## 8. Quel groupe rapporte le plus, lequel coûte le plus ?

### Méthode
Pour chaque groupe :
- **chiffre d'affaires mensuel** : somme des prix mensuels des abonnés du groupe ;
- **chiffre d'affaires perdu** : somme des prix mensuels des abonnés ayant résilié (prix × `a_resilie`).

### Résultats

| Groupe | Effectif | Prix moyen | Résiliation | CA mensuel | Part du CA | CA perdu | Part des pertes |
|---|---|---|---|---|---|---|---|
| Réguliers de proximité | 307 | 30,49 € | 18 % | 9 361 € | 31 % | 1 605 € | 28 % |
| **Fidèles Premium** | 170 | 61,85 € | 6 % | **10 515 €** | **35 %** | 622 € | 11 % |
| **Insatisfaits** | 192 | 29,77 € | 39 % | 5 716 € | 19 % | **2 052 €** | **36 %** |
| Éloignés | 128 | 32,57 € | 38 % | 4 169 € | 14 % | 1 405 € | 25 % |

### Réponse
- **Le groupe qui rapporte le plus** : les **fidèles Premium**. Ils représentent 21 % des abonnés mais **35 % du chiffre d'affaires**, et résilient très peu.
- **Le groupe qui coûte le plus** : les **insatisfaits**. Ils représentent 19 % du chiffre d'affaires mais **36 % des pertes** dues aux résiliations. C'est le groupe où une action de fidélisation a le plus de potentiel.
- **Le groupe où une campagne de rétention ne vaut pas la dépense** : les **fidèles Premium**. Ils partent déjà très peu (6 %) : une campagne pour les retenir ne récupérerait presque rien. Il faut continuer à bien les servir, mais les budgets de fidélisation sont mieux utilisés sur les insatisfaits et les éloignés.

---

## 9. Les abonnés atypiques

### Méthode : Isolation Forest
L'algorithme cherche à isoler chaque abonné en découpant la base au hasard, de nombreuses fois. Un abonné ordinaire, entouré d'abonnés qui lui ressemblent, demande beaucoup de découpes pour être isolé ; un abonné atypique est isolé en quelques découpes. Contrairement au repérage de la phase 1, colonne par colonne, cette méthode détecte des **combinaisons** de valeurs inhabituelles.

- Mêmes six variables standardisées que pour k-means.
- **Part d'atypiques fixée à 5 %** (`contamination=0.05`) : c'est un choix, pas un résultat de l'algorithme. 5 % est une valeur couramment utilisée.

### Combien et qui ?
**40 abonnés** atypiques, dont **35 Premium**.

| | Atypiques (40) | Autres abonnés (757) |
|---|---|---|
| Séances de coaching par mois | **3,6** | 0,65 |
| Visites par mois | **22,6** | 15,6 |
| Réclamations | **1,25** | 0,39 |
| Ancienneté | 57 mois | 27 mois |
| Distance | 4,5 km | 3,0 km |
| Résiliation | **8 %** | 25 % |

Les atypiques sont des **super-utilisateurs Premium** : ils viennent presque tous les jours, font cinq fois plus de coaching que la moyenne (et deux fois plus que les autres Premium : 4,0 séances contre 1,9), sont fidèles depuis longtemps, et se plaignent trois fois plus. Ce sont des clients très engagés et très exigeants. Les 5 atypiques non-Premium sont des cas isolés, sans profil commun.

### Est-ce qu'on perd de l'argent avec eux ?
Le sujet ne précise ni si le coaching est inclus dans l'abonnement, ni son coût. Hypothèses retenues :
- le coaching est **inclus** dans l'abonnement Premium ;
- une séance coûte **25 €** à FitZone (une heure de coach, charges comprises).

Marge mensuelle = prix mensuel − séances de coaching × 25 €.

| Abonnés Premium | Effectif | Prix moyen | Coaching | Marge moyenne | Marge totale |
|---|---|---|---|---|---|
| **Atypiques** | 35 | 64,31 € | 4,0 séances | **−35,69 €** | **−1 249 €** |
| Autres | 149 | 61,59 € | 1,9 séance | +14,78 € | +2 202 € |

Sur l'ensemble des 40 atypiques, la marge totale est de **−1 176 € par mois**, soit environ **14 000 € par an**. Ils deviennent déficitaires dès qu'une séance coûte plus de **16,78 €** à FitZone.

### Réponse
FitZone compte **40 abonnés atypiques** (5 % de la base), presque tous Premium. Ce sont ses clients les plus fidèles, mais très probablement **déficitaires** : leur consommation de coaching coûte plus que leur abonnement. Le problème ne vient pas de ces clients mais de l'**offre** : un abonnement à prix fixe avec coaching inclus sans limite attire inévitablement quelques très gros consommateurs.

**Piste de décision :** plafonner le nombre de séances de coaching incluses dans l'abonnement Premium (par exemple 2 par mois, la consommation habituelle des Premium) et facturer les séances supplémentaires.

---

## Limites de la phase 4
- **Segmentation** : la séparation en quatre groupes est moins nette que la séparation Premium / non-Premium (silhouette de 0,27 contre 0,43). Les frontières entre réguliers, insatisfaits et éloignés sont en partie floues.
- **Numérotation des groupes** : k-means numérote les groupes dans un ordre arbitraire. Les noms doivent être vérifiés si les données ou les variables changent.
- **Part d'atypiques** : fixée à 5 % par choix. Une autre valeur donnerait un nombre différent d'atypiques.
- **Coût du coaching** : la conclusion de la question 9 dépend de deux hypothèses (coaching inclus dans le Premium, 25 € par séance). Le calcul de marge n'a de sens que pour les abonnés Premium : pour les formules Essentiel et Confort, le coaching est probablement payant.
- **Coût des réclamations** : les atypiques se plaignent trois fois plus, ce qui représente aussi un coût de traitement, non chiffré ici.