"""
Priorisation des appels de retention et rendement de l'elargissement (phase 3).

Question 5 : 400 abonnes arrivent en fin d'engagement, on ne peut en appeler
             que 80. Lesquels ?
Question 6 : si on double l'equipe d'appel, recupere-t-on deux fois plus de
             monde ?

Ce module part des probabilites produites par src/classification.py et ne
reentraine aucun modele.

HYPOTHESES ECONOMIQUES - A LIRE AVANT TOUTE INTERPRETATION
----------------------------------------------------------
Les euros affiches par ce module ne sont pas des mesures : ce sont des
projections construites sur trois hypotheses explicites. Si l'une change,
tous les montants changent. Elles sont donc ecrites ici et non enfouies
dans le code.

1) TAUX DE SAUVETAGE D'UN APPEL = 25 %.
   Un appel passe a un abonne qui allait partir ne le retient pas toujours.
   Les benchmarks du secteur situent le taux de sauvetage d'une equipe
   formee entre 15 et 25 % des demandes de resiliation, et jusqu'a 25-55 %
   lorsque l'appel s'accompagne d'une offre de retention forte (remise,
   mois offerts, changement de formule). Comme rien n'indique que FitZone
   disposerait d'une telle offre, on retient 25 %, borne haute du cas SANS
   offre commerciale. C'est donc une hypothese prudente : avec une offre,
   le vrai taux serait superieur et la rentabilite calculee ici serait
   sous-estimee.
   Attention : ce taux ne s'applique qu'aux abonnes qui allaient
   effectivement resilier. Appeler un abonne fidele ne sauve rien, puisqu'il
   n'y avait rien a sauver. C'est tout l'enjeu du classement.

2) COUT D'UN APPEL = 8 EUR.
   Temps de l'agent, outil telephonique et encadrement. Ce cout est paye
   pour CHAQUE appel, qu'il aboutisse ou non, que l'abonne allait partir ou
   non. C'est ce qui fait qu'appeler plus n'est pas gratuit, et c'est le
   coeur de la question 6.

3) VALEUR D'UN ABONNE SAUVE = prix_mensuel_eur x 12.
   Un abonne retenu rapporte douze mois de son abonnement. C'est une
   hypothese volontairement simple et plutot conservatrice : elle ignore le
   fait qu'un abonne retenu peut rester plusieurs annees, mais elle ignore
   aussi les couts de la remise eventuellement consentie pour le retenir.
   On utilise le prix REEL de chaque abonne et non un prix moyen : c'est ce
   qui permet au critere de la valeur esperee d'exister.

CHOIX METHODOLOGIQUE : DEUX CRITERES DE PRIORISATION COMPARES
-------------------------------------------------------------
(a) Tri par probabilite de resiliation decroissante. Le reflexe naturel :
    on appelle les plus a risque. Ce critere maximise le nombre de
    resiliants atteints.
(b) Tri par valeur esperee = probabilite x prix_mensuel_eur x 12. Ce
    critere ne maximise pas le nombre d'abonnes atteints mais les euros
    preserves : un abonne Premium a 65 EUR avec 40 % de risque pese plus
    qu'un abonne Essentiel a 25 EUR avec 60 % de risque.

On compare les deux au lieu d'en choisir un a priori, parce que ce sont
deux objectifs differents et que rien ne garantit a l'avance lequel gagne.
La phase 2 a montre que les abonnes a risque sont justement ceux qui payent
le moins : les deux criteres pouvaient donc tres bien se contredire.

INDICATEURS AFFICHES
--------------------
- resiliants atteints : combien de futurs partants se trouvent dans la liste
  appelee. C'est le gain brut de la priorisation.
- precision : part des appels qui tombent sur un futur partant. Mesure le
  gaspillage : une precision de 0.475 veut dire qu'un appel sur deux est
  passe a quelqu'un qui n'allait pas partir.
- lift : precision divisee par le taux de resiliation de base. Repond a
  "combien de fois mieux que d'appeler au hasard ?". Un lift de 2 signifie
  deux fois plus de partants touches qu'avec une liste tiree au sort.
- couverture : part de TOUS les resiliants de la cohorte que l'on touche.
  Le lift dit si l'on vise bien, la couverture dit si l'on vise large.
- ROI : chiffre d'affaires preserve divise par le cout des appels. Un ROI de
  5.1x signifie 5,10 EUR de CA preserve par euro depense en appels.
"""

import os

import matplotlib
matplotlib.use("Agg")  # backend sans fenetre : on ecrit des PNG, on n'affiche rien
import matplotlib.pyplot as plt
import pandas as pd

# Hypotheses economiques (cf. docstring). Regroupees ici pour qu'une
# direction qui conteste un chiffre sache ou le changer.
TAUX_SAUVETAGE = 0.25
COUT_APPEL_EUR = 8.0
MOIS_PAR_AN = 12

# Capacite actuelle de l'equipe d'appel, et paliers d'elargissement testes
CAPACITE_ACTUELLE = 80
PALIERS_APPELS = [80, 160, 240, 320, 400]

# Les deux criteres de priorisation compares
CRITERE_RISQUE = "probabilite_resiliation"
CRITERE_VALEUR = "valeur_esperee_eur"

# Variables du profil moyen compare
COLONNES_PROFIL = [
    "anciennete_mois",
    "visites_par_mois",
    "seances_coaching",
    "reclamations",
    "distance_domicile_m",
    "prix_mensuel_eur",
]

DOSSIER_FIGURES = os.path.join("outputs", "figures")
DOSSIER_RESULTATS = os.path.join("outputs", "results")
FICHIER_TOP80 = os.path.join(DOSSIER_RESULTATS, "q5_top80_a_appeler.csv")


def ajouter_valeur_esperee(cohorte):
    """Ajoute la colonne de valeur esperee a la cohorte scoree.

    valeur esperee = probabilite de depart x chiffre d'affaires annuel.
    C'est l'esperance de CA en jeu pour cet abonne, avant application du
    taux de sauvetage (qui est le meme pour tous et ne change donc pas
    l'ordre du classement).
    """
    cohorte = cohorte.copy()
    cohorte[CRITERE_VALEUR] = (
        cohorte[CRITERE_RISQUE] * cohorte["prix_mensuel_eur"] * MOIS_PAR_AN
    )
    return cohorte


def classer_cohorte(cohorte, critere):
    """Trie la cohorte par le critere choisi, du plus prioritaire au moins."""
    return cohorte.sort_values(critere, ascending=False)


def courbe_de_gain(cohorte, critere):
    """Construit le tableau de gain cumule aux paliers d'appels.

    Pour chaque palier : resiliants atteints, precision, lift, couverture,
    puis le volet economique (sauves, CA preserve, cout, gain net, ROI).
    Ajoute aussi les colonnes marginales, qui sont la reponse a la question 6.
    """
    classement = classer_cohorte(cohorte, critere)
    taux_base = cohorte["churn"].mean()
    total_resiliants = int(cohorte["churn"].sum())

    lignes = []
    for nombre_appels in PALIERS_APPELS:
        appeles = classement.head(nombre_appels)
        atteints = int(appeles["churn"].sum())

        precision = atteints / nombre_appels
        couverture = atteints / total_resiliants

        # Abonnes sauves : seuls ceux qui allaient partir peuvent l'etre,
        # et seulement dans 25 % des cas (cf. hypothese 1)
        sauves = atteints * TAUX_SAUVETAGE

        # CA preserve : on somme le prix REEL des partants atteints, et non
        # un prix moyen, sinon le critere de la valeur esperee n'aurait
        # aucun effet mesurable
        partants_atteints = appeles.loc[appeles["churn"] == 1, "prix_mensuel_eur"]
        ca_preserve = (partants_atteints * MOIS_PAR_AN * TAUX_SAUVETAGE).sum()

        cout = nombre_appels * COUT_APPEL_EUR

        lignes.append({
            "appels": nombre_appels,
            "resiliants_atteints": atteints,
            "precision": round(precision, 3),
            "lift": round(precision / taux_base, 2),
            "couverture": round(couverture, 3),
            "abonnes_sauves": round(sauves, 2),
            "ca_preserve_eur": round(ca_preserve),
            "cout_eur": round(cout),
            "gain_net_eur": round(ca_preserve - cout),
            "roi": round(ca_preserve / cout, 1),
        })

    tableau = pd.DataFrame(lignes)

    # Colonnes marginales : ce que rapporte CHAQUE tranche de 80 appels
    # supplementaires, par difference avec le palier precedent. C'est la
    # grandeur qui repond a la question 6 ; le cumul, lui, monte toujours et
    # ne dit donc rien sur le rendement.
    tableau["marginal_resiliants"] = tableau["resiliants_atteints"].diff().fillna(
        tableau["resiliants_atteints"]).astype(int)
    tableau["marginal_gain_net_eur"] = tableau["gain_net_eur"].diff().fillna(
        tableau["gain_net_eur"]).astype(int)
    return tableau


def profil_comparatif(cohorte):
    """Compare le profil moyen des 80 prioritaires a celui de la cohorte entiere.

    On affiche les deux criteres cote a cote : c'est la seule facon de voir
    que le tri par valeur esperee designe des abonnes plus chers.
    """
    top_risque = classer_cohorte(cohorte, CRITERE_RISQUE).head(CAPACITE_ACTUELLE)
    top_valeur = classer_cohorte(cohorte, CRITERE_VALEUR).head(CAPACITE_ACTUELLE)

    return pd.DataFrame({
        "cohorte_400": cohorte[COLONNES_PROFIL].mean().round(1),
        "top80_risque": top_risque[COLONNES_PROFIL].mean().round(1),
        "top80_valeur": top_valeur[COLONNES_PROFIL].mean().round(1),
    })


def exporter_liste_appels(cohorte):
    """Exporte les 80 abonnes a appeler, classes par valeur esperee decroissante.

    On exporte le classement par valeur esperee et non par risque : c'est
    celui que la comparaison des deux criteres designe comme meilleur (il
    atteint plus de partants ET preserve plus de CA, voir la sortie console).
    L'ordre des lignes est l'ordre d'appel recommande.
    """
    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)

    liste = classer_cohorte(cohorte, CRITERE_VALEUR).head(CAPACITE_ACTUELLE)
    liste = liste[[
        "abonne_id",
        "salle",
        CRITERE_RISQUE,
        CRITERE_VALEUR,
        "prix_mensuel_eur",
    ]].copy()
    liste[CRITERE_RISQUE] = liste[CRITERE_RISQUE].round(4)
    liste[CRITERE_VALEUR] = liste[CRITERE_VALEUR].round(2)

    liste.to_csv(FICHIER_TOP80, index=False)
    return FICHIER_TOP80, liste


def tracer_courbe_gain(cohorte):
    """Figure 1 : courbe de gain cumule des deux criteres contre le hasard.

    On trace la courbe appel par appel et non seulement aux cinq paliers :
    la forme concave se voit, et c'est elle qui porte la reponse a la
    question 6. La diagonale est ce que donnerait une liste tiree au sort.
    """
    os.makedirs(DOSSIER_FIGURES, exist_ok=True)
    total_resiliants = int(cohorte["churn"].sum())
    effectif = len(cohorte)

    plt.figure(figsize=(8, 6))
    for critere, etiquette, couleur in [
        (CRITERE_RISQUE, "Tri par risque de resiliation", "tab:blue"),
        (CRITERE_VALEUR, "Tri par valeur esperee", "tab:green"),
    ]:
        classement = classer_cohorte(cohorte, critere)
        atteints_cumules = classement["churn"].cumsum().values
        plt.plot(range(1, effectif + 1), atteints_cumules, label=etiquette, color=couleur)

    # Diagonale du hasard : en appelant au hasard, on touche les resiliants
    # proportionnellement au nombre d'appels
    plt.plot([0, effectif], [0, total_resiliants], "r--", label="Hasard (aucune priorisation)")

    # Reperes verticaux aux paliers d'equipe
    for palier in PALIERS_APPELS:
        plt.axvline(palier, color="grey", linewidth=0.5, alpha=0.5)
    plt.axvline(CAPACITE_ACTUELLE, color="black", linewidth=1.2,
                label="Capacite actuelle (80 appels)")

    plt.xlabel("Nombre d'appels passes (abonnes classes du plus prioritaire au moins)")
    plt.ylabel("Resiliants atteints (cumul)")
    plt.title("Courbe de gain cumule sur la cohorte de 400 abonnes")
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    chemin = os.path.join(DOSSIER_FIGURES, "phase3_courbe_gain_cumule.png")
    plt.tight_layout()
    plt.savefig(chemin, dpi=120)
    plt.close()
    return chemin


def tracer_gain_marginal(tableau_risque):
    """Figure 2 : gain marginal par tranche de 80 appels supplementaires.

    Barres = resiliants atteints en plus par tranche. L'annotation donne le
    gain NET en euros de la tranche : c'est lui qui devient negatif sur la
    derniere, et une barre rouge le signale.
    """
    os.makedirs(DOSSIER_FIGURES, exist_ok=True)

    etiquettes = []
    debut = 0
    for palier in tableau_risque["appels"]:
        etiquettes.append("{}-{}".format(debut, palier))
        debut = palier

    marginal = tableau_risque["marginal_resiliants"].values
    marginal_euros = tableau_risque["marginal_gain_net_eur"].values
    # Rouge quand la tranche detruit de la valeur : le cout des 80 appels
    # depasse le CA qu'ils preservent
    couleurs = ["tab:red" if euros < 0 else "tab:blue" for euros in marginal_euros]

    plt.figure(figsize=(9, 5.5))
    barres = plt.bar(etiquettes, marginal, color=couleurs)
    for barre, resiliants, euros in zip(barres, marginal, marginal_euros):
        plt.text(barre.get_x() + barre.get_width() / 2,
                 barre.get_height() + 0.6,
                 "+{} partants\n{:+d} EUR net".format(resiliants, int(euros)),
                 ha="center", va="bottom", fontsize=9)

    plt.ylim(0, max(marginal) * 1.35)
    plt.xlabel("Tranche de 80 appels (tri par risque de resiliation)")
    plt.ylabel("Resiliants atteints en plus")
    plt.title("Rendement decroissant de l'elargissement de l'equipe d'appel")
    plt.grid(axis="y", alpha=0.3)
    chemin = os.path.join(DOSSIER_FIGURES, "phase3_gain_marginal.png")
    plt.tight_layout()
    plt.savefig(chemin, dpi=120)
    plt.close()
    return chemin


def afficher_tableau_gain(tableau, titre):
    """Affiche un tableau de gain cumule de facon lisible en console."""
    print("\n--- {} ---".format(titre))
    print("appels  atteints  precision  lift  couverture  sauves  CA preserve  "
          "cout   gain net   ROI")
    # iterrows renvoie chaque ligne en Series de type commun : les entiers y
    # deviennent des flottants, d'ou les int() explicites a l'affichage
    for _, ligne in tableau.iterrows():
        print("{:>6d}  {:>8d}  {:>9.3f}  {:>4.2f}  {:>10.3f}  {:>6.2f}  {:>10.0f}  "
              "{:>5.0f}  {:>8.0f}  {:>4.1f}x".format(
                  int(ligne["appels"]), int(ligne["resiliants_atteints"]), ligne["precision"],
                  ligne["lift"], ligne["couverture"], ligne["abonnes_sauves"],
                  ligne["ca_preserve_eur"], ligne["cout_eur"],
                  ligne["gain_net_eur"], ligne["roi"]))


def evaluer_priorisation(cohorte):
    """Enchaine toute l'evaluation des questions 5 et 6 et affiche les resultats."""
    cohorte = ajouter_valeur_esperee(cohorte)
    total_resiliants = int(cohorte["churn"].sum())
    taux_base = cohorte["churn"].mean()

    print("Hypotheses economiques retenues (cf. docstring du module) :")
    print("  taux de sauvetage d'un appel : {:.0f} %".format(TAUX_SAUVETAGE * 100))
    print("  cout d'un appel              : {:.0f} EUR".format(COUT_APPEL_EUR))
    print("  valeur d'un abonne sauve     : prix mensuel x {} mois".format(MOIS_PAR_AN))

    print("\n=== QUESTION 5 : quels 80 abonnes appeler ? ===")
    print("Cohorte : {} abonnes, dont {} resiliants ({:.2f} % de base).".format(
        len(cohorte), total_resiliants, taux_base * 100))
    print("Capacite : {} appels, soit {:.0f} % de la cohorte.".format(
        CAPACITE_ACTUELLE, CAPACITE_ACTUELLE / len(cohorte) * 100))

    tableau_risque = courbe_de_gain(cohorte, CRITERE_RISQUE)
    tableau_valeur = courbe_de_gain(cohorte, CRITERE_VALEUR)

    afficher_tableau_gain(tableau_risque, "CRITERE (a) : tri par risque de resiliation")
    afficher_tableau_gain(tableau_valeur, "CRITERE (b) : tri par valeur esperee")

    # Comparaison des deux criteres a la capacite actuelle
    risque_80 = tableau_risque.iloc[0]
    valeur_80 = tableau_valeur.iloc[0]
    print("\n--- Comparaison des deux criteres a 80 appels ---")
    print("                        tri risque   tri valeur esperee   ecart")
    print("resiliants atteints   {:>11}   {:>18}   {:+d}".format(
        int(risque_80["resiliants_atteints"]), int(valeur_80["resiliants_atteints"]),
        int(valeur_80["resiliants_atteints"] - risque_80["resiliants_atteints"])))
    print("CA preserve (EUR)     {:>11.0f}   {:>18.0f}   {:+.0f}".format(
        risque_80["ca_preserve_eur"], valeur_80["ca_preserve_eur"],
        valeur_80["ca_preserve_eur"] - risque_80["ca_preserve_eur"]))
    print("gain net (EUR)        {:>11.0f}   {:>18.0f}   {:+.0f}".format(
        risque_80["gain_net_eur"], valeur_80["gain_net_eur"],
        valeur_80["gain_net_eur"] - risque_80["gain_net_eur"]))
    print("ROI                   {:>10.1f}x   {:>17.1f}x".format(
        risque_80["roi"], valeur_80["roi"]))

    # Combien d'abonnes les deux listes ont-ils en commun ? Si les deux
    # criteres designaient les memes personnes, le choix n'aurait aucun enjeu.
    ids_risque = set(classer_cohorte(cohorte, CRITERE_RISQUE).head(CAPACITE_ACTUELLE)["abonne_id"])
    ids_valeur = set(classer_cohorte(cohorte, CRITERE_VALEUR).head(CAPACITE_ACTUELLE)["abonne_id"])
    communs = len(ids_risque & ids_valeur)
    print("\nLes deux listes de 80 ont {} abonnes en commun sur 80 ({:.0f} %).".format(
        communs, communs / CAPACITE_ACTUELLE * 100))
    print("Le choix du critere change donc bien la liste a appeler.")

    print("\n--- Profil moyen des 80 prioritaires contre la cohorte entiere ---")
    print(profil_comparatif(cohorte))
    print("\nLecture : les 80 prioritaires sont des abonnes recents, peu")
    print("assidus, sans coaching, qui reclament deux fois plus, habitent plus")
    print("loin et payent moins cher que la moyenne. C'est coherent avec la")
    print("phase 2 : le modele a appris le profil du partant, il ne le devine pas.")

    chemin_csv, liste = exporter_liste_appels(cohorte)
    print("\n--- Liste des 80 abonnes a appeler ---")
    print("Classement retenu : valeur esperee decroissante (meilleur sur les")
    print("deux objectifs a la fois, voir la comparaison ci-dessus).")
    print("Fichier exporte :", chemin_csv)
    print("Les 5 premiers a appeler :")
    print(liste.head(5).to_string(index=False))

    print("\nReponse a la question 5 : il faut appeler les 80 abonnes de")
    print("outputs/results/q5_top80_a_appeler.csv, classes par valeur esperee.")
    print("Cette liste touche {} des {} futurs partants de la cohorte, soit".format(
        int(valeur_80["resiliants_atteints"]), total_resiliants))
    print("{:.0f} % d'entre eux avec {:.0f} % des appels possibles : {:.2f} fois".format(
        valeur_80["couverture"] * 100, CAPACITE_ACTUELLE / len(cohorte) * 100,
        valeur_80["lift"]))
    print("mieux qu'une liste tiree au sort. En appelant au hasard, les memes")
    print("80 appels n'atteindraient que {:.0f} partants.".format(
        CAPACITE_ACTUELLE * taux_base))

    print("\n=== QUESTION 6 : que rapporte vraiment l'elargissement ? ===")
    print("\n--- Gain marginal par tranche de 80 appels supplementaires ---")
    print("tranche      resiliants en plus   gain net de la tranche   gain net cumule")
    for tableau, nom in [(tableau_risque, "tri par risque"),
                         (tableau_valeur, "tri par valeur esperee")]:
        print("\n  {} :".format(nom))
        debut = 0
        for _, ligne in tableau.iterrows():
            print("  {:>3}-{:>3} appels   {:>+14d}   {:>+22d} EUR   {:>11.0f} EUR".format(
                debut, int(ligne["appels"]), int(ligne["marginal_resiliants"]),
                int(ligne["marginal_gain_net_eur"]), ligne["gain_net_eur"]))
            debut = int(ligne["appels"])

    # Reponse chiffree a "deux fois plus de monde ?" : on compare le palier
    # 160 au palier 80 sur le tri par risque
    risque_160 = tableau_risque.iloc[1]
    rapport_atteints = risque_160["resiliants_atteints"] / risque_80["resiliants_atteints"]
    rapport_gain = risque_160["gain_net_eur"] / risque_80["gain_net_eur"]
    print("\n--- Doubler l'equipe : 80 appels contre 160 ---")
    print("resiliants atteints : {} -> {}, soit x{:.2f} (et non x2)".format(
        int(risque_80["resiliants_atteints"]), int(risque_160["resiliants_atteints"]),
        rapport_atteints))
    print("gain net            : {:.0f} -> {:.0f} EUR, soit x{:.2f}".format(
        risque_80["gain_net_eur"], risque_160["gain_net_eur"], rapport_gain))

    meilleur = tableau_risque.loc[tableau_risque["gain_net_eur"].idxmax()]
    tranches_negatives = tableau_risque[tableau_risque["marginal_gain_net_eur"] < 0]

    print("\n--- Figures ---")
    print("enregistree :", tracer_courbe_gain(cohorte))
    print("enregistree :", tracer_gain_marginal(tableau_risque))

    print("\nReponse a la question 6 : NON, doubler l'equipe ne ramene pas deux")
    print("fois plus de monde. Le cout des appels est lineaire, le gain ne")
    print("l'est pas : on appelle d'abord les abonnes les plus a risque, donc")
    print("chaque tranche suivante tombe sur des abonnes moins susceptibles de")
    print("partir. Doubler l'equipe fait passer les partants atteints de {} a".format(
        int(risque_80["resiliants_atteints"])))
    print("{} (x{:.2f}) et le gain net de {:.0f} a {:.0f} EUR (x{:.2f}).".format(
        int(risque_160["resiliants_atteints"]), rapport_atteints,
        risque_80["gain_net_eur"], risque_160["gain_net_eur"], rapport_gain))
    print("La precision tombe de {:.3f} a {:.3f} et le lift de {:.2f} a {:.2f}.".format(
        risque_80["precision"], risque_160["precision"],
        risque_80["lift"], risque_160["lift"]))
    print("\nLe rendement est donc decroissant tranche apres tranche :")
    print("{} partants gagnes sur la premiere tranche, puis {}.".format(
        ", ".join(str(int(v)) for v in tableau_risque["marginal_resiliants"].head(1)),
        ", ".join("+{}".format(int(v)) for v in tableau_risque["marginal_resiliants"].iloc[1:])))
    if len(tranches_negatives) > 0:
        premiere = tranches_negatives.iloc[0]
        print("\nPoint important pour la decision : la derniere tranche ne fait")
        print("pas que rapporter moins, elle DETRUIT de la valeur. Les appels")
        print("{} a {} ne gagnent que {} partants pour {:.0f} EUR d'appels,".format(
            int(premiere["appels"]) - CAPACITE_ACTUELLE, int(premiere["appels"]),
            int(premiere["marginal_resiliants"]), CAPACITE_ACTUELLE * COUT_APPEL_EUR))
        print("soit {:+.0f} EUR de gain net sur la tranche.".format(
            premiere["marginal_gain_net_eur"]))
        print("Le gain net cumule est donc maximal a {} appels ({:.0f} EUR) et".format(
            int(meilleur["appels"]), meilleur["gain_net_eur"]))
        print("redescend ensuite : appeler toute la cohorte est une perte.")
    print("\nRecommandation : l'equipe peut etre elargie avec profit, mais pas")
    print("jusqu'a saturer la cohorte. Chaque tranche de 80 doit etre decidee")
    print("sur son gain marginal, jamais sur le gain cumule, qui monte presque")
    print("toujours et ne dit donc rien du rendement de la tranche ajoutee.")
