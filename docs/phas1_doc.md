# Problèmes trouvés et solutions apportées

## 1. Doublons
40 doublons ont été trouvés dans le fichier csv des abonnés. Il y a 40 lignes entièrement identiques et 40 identifiants répétés, donc tous les identifiants répétés sont des copies exactes et aucun abonné réel n’est perdu. On supprime les doublons et on passe donc de 840 lignes à 800 lignes.

## 2. Valeurs manquantes
### a- Séances de coaching
Les séances de coaching manquantes (20 au total) ont été remplacées par la médiane de la formule (0 pour les formules Essentiel et Confort et 2 pour les formules Premium). Remplacer toutes les cases par 0 serait mensonger surtout pour les membres avec un abonnement premium qui ont en général 2 séances de coaching par mois.

### b- Créneaux 
Les créneaux manquants (22 au total, dont 2 étaient des doublons qui ont été supprimés) ont été remplacés par la valeur 'inconnu' pour éviter d'inventer des valeurs et de fausser la prédiction

## 3. Valeurs erronées
### a- L'ancienneté inférieure à 0
Les clients dont l'ancienneté est inférieure à 0 ont été supprimés. Étant au nombre de 3 et tous les 3 ayant la valeur de -1, cela ressemble plus à un code pour indiquer que l'on ne connait pas cette valeur. Ils ne représentent qu'une minorité dont la conséquence liée à leur perte n'est pas considérable. Nous avons fait le choix de les supprimer pour également éviter de remplir par des valeurs inventées qui peuvent s’avérer erronées

### b- Le prix de l'abonnement inférieur à 0
Le prix des abonnés à 0 euros a été remplacé par la médiane de la formule associée parce qu'ils ont une ancienneté allant de 7 à 29 mois. C'est donc impossible qu'ils soient en période d'essai durant tout ce temps.

## 4. Ancienneté d'un membre supérieure à celle de la salle de sport à laquelle il appartient
Ce cas touche 106 abonnés. Nous avons fait le choix de laisser les valeurs telles quelles parce que la majorité des cas qui ont été trouvés se concentrent sur les nouvelles salles de sport (la salle S06 est la plus touchée avec 55 cas pour 9 mois d'ancienneté). Ça pourrait être expliqué par un changement de salle de sport durant l'abonnement. Nous considérons que l’ancienneté est comptée dans la chaîne FitZone, et non dans la salle actuelle.

Cette hypothèse ne peut pas être vérifiée avec les données, faute de colonne indiquant la salle précédente. Point à discuter en groupe.

## 5. Distance salle de sport-maison
9 abonnés habitent à plus de 10km de leur salle de sport dont l'un à 16km. Nous avons décidé de laisser les informations telles quelles parce qu'il peut y avoir plusieurs explications possibles : comme le fait qu'il puisse habiter dans une campagne, ou qu'il ait choisi une salle proche de son lieu de travail et non de sa maison. Aussi les supprimer ne nous permettrait pas d'étudier les cas atypiques et déduire si une longue distance induit obligatoirement ou le plus souvent une résiliation.

## 6. Encodage des variables
Les colonnes a_resilie dans le fichier des abonnés et parking dans le fichier des salles ont été remplacés par des nombres : 0 pour non et 1 pour oui. Nous avons pris cette décision pour que le modèle puisse mieux manipuler ces valeurs lors de sa prédiction (multiplication, addition, etc)

## 7. Bilan
Au départ nous avions :
- 840 lignes
- 800 abonnés
- 14 salles
- 40 doublons (lignes entièrement identiques)
- 22 valeurs manquantes (creneau_habituel)
- 20 séances de coaching manquantes
- 3 prix à 0 euro
- 3 ancienneté à -1

Après nettoyage : 
- 797 lignes
- 797 clients (après suppression des doublons et des trois clients dont l'ancienneté était inconnue)
- 0 doublons
- Créneaux manquants remplacés par ` inconnu ` (20 au total après suppression des doublons )
- Les séances de coaching manquantes ont été remplacées par la médiane de la formule (0 pour les formules Essentiel et Confort, et 2 pour les formules Premium)

Les données nettoyées ont été enregistrées dans ` data/processed/abonnes_clean.csv ` et ` data/processed/salles_clean.csv `. Les données sont intactes et dans le dossier ` data/raw `

## 8. Premières observations
- Le taux de résiliation global (23,7 %) 
- Le taux de résiliation par formule (Essentiel : 35,5 % / Confort : 19,3 % / Premium : 6,0 %)

Ces écarts sont une corrélation et pas une preuve de causalité : les abonnés les plus motivés choisissent peut-être Premium, et c’est leur motivation qui les fait rester. Reste à être étudié en phase 2.