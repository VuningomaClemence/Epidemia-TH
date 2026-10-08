import unicodedata


COULEURS_PROVINCES_RDC = {
    "sud-kivu": {"couleur": "#2563eb", "nom": "Sud-Kivu", "nom_couleur": "Bleu Royal"},
    "nord-kivu": {"couleur": "#16a34a", "nom": "Nord-Kivu", "nom_couleur": "Vert Émeraude"},
    "kinshasa": {"couleur": "#7c3aed", "nom": "Kinshasa", "nom_couleur": "Violet Impérial"},
    "kongo-central": {"couleur": "#0891b2", "nom": "Kongo-Central", "nom_couleur": "Cyan Océan"},
    "haut-katanga": {"couleur": "#d97706", "nom": "Haut-Katanga", "nom_couleur": "Ambre Doré"},
    "lualaba": {"couleur": "#b45309", "nom": "Lualaba", "nom_couleur": "Bronze Cuivré"},
    "ituri": {"couleur": "#047857", "nom": "Ituri", "nom_couleur": "Vert Forêt"},
    "kasai": {"couleur": "#db2777", "nom": "Kasaï", "nom_couleur": "Rose Magenta"},
    "kasai-central": {"couleur": "#9333ea", "nom": "Kasaï-Central", "nom_couleur": "Pourpre Vif"},
    "kasai-oriental": {"couleur": "#e11d48", "nom": "Kasaï-Oriental", "nom_couleur": "Rouge Rubis"},
    "kwilu": {"couleur": "#65a30d", "nom": "Kwilu", "nom_couleur": "Vert Lime"},
    "kwango": {"couleur": "#0d9488", "nom": "Kwango", "nom_couleur": "Sarcelle / Teal"},
    "mai-ndombe": {"couleur": "#1e40af", "nom": "Maï-Ndombe", "nom_couleur": "Bleu Nuit"},
    "maniema": {"couleur": "#a16207", "nom": "Maniema", "nom_couleur": "Ocre Brun"},
    "tshopo": {"couleur": "#0284c7", "nom": "Tshopo", "nom_couleur": "Bleu Ciel"},
    "haut-uele": {"couleur": "#ea580c", "nom": "Haut-Uele", "nom_couleur": "Orange Corail"},
    "bas-uele": {"couleur": "#2563eb", "nom": "Bas-Uele", "nom_couleur": "Bleu Royal"},
    "mongala": {"couleur": "#059669", "nom": "Mongala", "nom_couleur": "Vert Menthe"},
    "nord-ubangi": {"couleur": "#8b5cf6", "nom": "Nord-Ubangi", "nom_couleur": "Lilas / Mauve"},
    "sud-ubangi": {"couleur": "#15803d", "nom": "Sud-Ubangi", "nom_couleur": "Vert Prairie"},
    "tanganyika": {"couleur": "#4338ca", "nom": "Tanganyika", "nom_couleur": "Indigo Lacustre"},
    "lomami": {"couleur": "#c026d3", "nom": "Lomami", "nom_couleur": "Fuchsia"},
    "sankuru": {"couleur": "#4d7c0f", "nom": "Sankuru", "nom_couleur": "Vert Olive"},
    "haut-lomami": {"couleur": "#c2410c", "nom": "Haut-Lomami", "nom_couleur": "Terre Cuite"},
    "tshuapa": {"couleur": "#166534", "nom": "Tshuapa", "nom_couleur": "Vert Mousse"},
    "equateur": {"couleur": "#0e7490", "nom": "Équateur", "nom_couleur": "Cyan Profond"},
}


def normaliser_nom_province(texte):
    """Normalise le nom de la province (minuscule, sans accents, sans tirets/espaces hétérogènes)."""
    if not texte:
        return ""
    texte_str = str(texte).strip()
    norm = unicodedata.normalize("NFKD", texte_str).encode("ASCII", "ignore").decode("utf-8")
    return norm.strip().lower().replace("_", "-").replace(" ", "-")


def obtenir_couleur_province(nom_province):
    """Retourne la couleur hexadécimale distinctive propre aux symboles de chaque province."""
    cle = normaliser_nom_province(nom_province)
    if cle in COULEURS_PROVINCES_RDC:
        return COULEURS_PROVINCES_RDC[cle]["couleur"]
    for k, v in COULEURS_PROVINCES_RDC.items():
        if k in cle or cle in k:
            return v["couleur"]
    palette_fallback = ["#2563eb", "#16a34a", "#7c3aed", "#d97706", "#0891b2", "#db2777", "#ea580c", "#059669"]
    h = sum(ord(c) for c in str(nom_province))
    return palette_fallback[h % len(palette_fallback)]


def obtenir_nom_couleur_province(nom_province):
    """Retourne le libellé de la couleur de la province."""
    cle = normaliser_nom_province(nom_province)
    if cle in COULEURS_PROVINCES_RDC:
        return COULEURS_PROVINCES_RDC[cle]["nom_couleur"]
    for k, v in COULEURS_PROVINCES_RDC.items():
        if k in cle or cle in k:
            return v["nom_couleur"]
    return "Couleur Thématique"
