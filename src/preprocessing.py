
# Supprimer les lignes en double
def supprimer_doublons(abonnes):
    print("\n--- Suppression des doublons ---")

    nb_avant = len(abonnes)

    abonnes = abonnes.drop_duplicates().copy()

    nb_apres = len(abonnes)

    print("Nombre de lignes avant :", nb_avant)
    print("Nombre de lignes après :", nb_apres)
    print("Doublons supprimés :", nb_avant - nb_apres)

    return abonnes


# Remplacer les séances de coaching manquantes par la médiane de chaque formule
def traiter_coaching_manquant(abonnes):
    print("\n--- Traitement des séances de coaching manquantes ---")

    nb_avant = abonnes["seances_coaching"].isna().sum()

    medianes = abonnes.groupby("formule")["seances_coaching"].transform("median")

    abonnes["seances_coaching"] = abonnes["seances_coaching"].fillna(medianes)

    nb_apres = abonnes["seances_coaching"].isna().sum()

    print("Valeurs manquantes avant :", nb_avant)
    print("Valeurs manquantes après :", nb_apres)

    return abonnes


# Remplacer les créneaux manquants par Inconnu
def traiter_creneau_manquant(abonnes):
    print("\n--- Traitement des créneaux habituels manquants ---")

    nb_avant = abonnes["creneau_habituel"].isna().sum()

    abonnes["creneau_habituel"] = abonnes["creneau_habituel"].fillna("Inconnu")

    nb_apres = abonnes["creneau_habituel"].isna().sum()

    print("Valeurs manquantes avant :", nb_avant)
    print("Valeurs manquantes après :", nb_apres)

    return abonnes


# Corriger les anciennetés négatives avec la médiane des abonnés Essentiel
def corriger_anciennetes(abonnes):
    print("\n--- Correction des anciennetés négatives ---")

    nb_avant = (abonnes["anciennete_mois"] < 0).sum()

    essentiel = abonnes[abonnes["formule"] == "Essentiel"]
    anciennetes_valides = essentiel[essentiel["anciennete_mois"] >= 0]

    mediane = anciennetes_valides["anciennete_mois"].median()

    abonnes.loc[
        abonnes["anciennete_mois"] < 0,
        "anciennete_mois"
    ] = mediane

    nb_apres = (abonnes["anciennete_mois"] < 0).sum()

    print("Anciennetés négatives avant :", nb_avant)
    print("Anciennetés négatives après :", nb_apres)

    return abonnes


# Corriger les prix nuls avec la médiane de chaque formule
def corriger_prix(abonnes):
    print("\n--- Correction des prix mensuels nuls ---")

    nb_avant = (abonnes["prix_mensuel_eur"] == 0).sum()

    prix_valides = abonnes[abonnes["prix_mensuel_eur"] > 0]

    medianes = prix_valides.groupby("formule")["prix_mensuel_eur"].median()
    prix_remplacement = abonnes["formule"].map(medianes).round(2)

    abonnes.loc[
        abonnes["prix_mensuel_eur"] == 0,
        "prix_mensuel_eur"
    ] = prix_remplacement

    nb_apres = (abonnes["prix_mensuel_eur"] == 0).sum()

    print("Prix nuls avant :", nb_avant)
    print("Prix nuls après :", nb_apres)

    return abonnes