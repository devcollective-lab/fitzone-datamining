def apercu(df, id_col=None):
    """
    Affiche un aperçu du DataFrame : dimensions, premières lignes, types,
    valeurs manquantes, doublons, statistiques descriptives et
    répartition des valeurs des colonnes texte.

    Args:
        df (pd.DataFrame): le DataFrame à explorer.
        id_col (str, optionnel): nom de la colonne identifiant, pour
            vérifier les doublons d'identifiants et l'exclure des comptages.
    """
    print("Dimensions ")
    print(df.shape)

    print("\nPremières lignes ")
    print(df.head(10))

    print("\nTypes des colonnes ")
    print(df.dtypes)

    print("\nValeurs manquantes ")
    print(df.isna().sum())

    print("\nDoublons ")
    print("Lignes entièrement identiques :", df.duplicated().sum())
    if id_col is not None:
        print(f"Identifiants '{id_col}' répétés :", df[id_col].duplicated().sum())

    print("\nStatistiques descriptives ")
    print(df.describe())

    print("\nRépartition des colonnes texte ")
    colonnes_texte = df.select_dtypes(exclude="number").columns
    for col in colonnes_texte:
        if col == id_col:
            continue
        print(f"\n--- {col} ---")
        print(df[col].value_counts(dropna=False))


def vu_clients(df):
    # Les abonnés qui ont la case seances_coaching manquante et quel valeur médiane pour chaque formule à laquelle 
    #ils appartiennent

    #Dans quelles formules sont les 20 abonnés sans valeur ?
    manquants = df[df["seances_coaching"].isna()]
    print(manquants["formule"].value_counts())

    #Combien de séances font les autres, selon leur formule ?
    print("\n", df.groupby("formule")["seances_coaching"].median())

def valeurs_incoherentes(df):

    # Abonnés avec une ancienneté négative
    anciennete_negative = df[df["anciennete_mois"] < 0]
    print(anciennete_negative)
    
    # Abonnés qui paient 0 €
    prix_nul = df[df["prix_mensuel_eur"] == 0]
    print(prix_nul)

def f(df, salles_df):
    # Pourquoi certains abonnés ont une ancienneté supérieure à l'âge de leur salle ?

    # 1. Fusionner : chaque abonné récupère les infos de sa salle
    fusion = df.merge(salles_df, on="salle")

    # 2. Filtrer : les abonnés "plus anciens" que leur salle
    incoherents = fusion[fusion["anciennete_mois"] > fusion["ouverte_depuis_mois"]]
    print("Nombre d'abonnés concernés :", len(incoherents))

    # 3. Dans quelles salles sont-ils ?
    print(incoherents["salle"].value_counts())

    # 4. Pour comparer : l'âge de chaque salle
    print(salles_df[["salle", "ouverte_depuis_mois"]].sort_values("ouverte_depuis_mois"))