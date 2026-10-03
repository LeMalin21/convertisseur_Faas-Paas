TAUX_PAR_EURO = {
    "EUR": 1.0,
    "USD": 1.16,
    "CAD": 1.62,
    "JPY": 172.0,
}


def convertir(montant, devise_source, devise_cible):
    devise_source = devise_source.upper()
    devise_cible = devise_cible.upper()

    # Exceptions pour les devises inconnues et les montants négatifs
    if devise_source not in TAUX_PAR_EURO:
        raise ValueError(f"Devise inconnue : {devise_source}")
    if devise_cible not in TAUX_PAR_EURO:
        raise ValueError(f"Devise inconnue : {devise_cible}")
    if montant < 0:
        raise ValueError("Le montant doit être positif")

    # On ramène le montant en euros puis on le convertit dans la devise cible.
    montant_en_euros = montant / TAUX_PAR_EURO[devise_source]
    resultat = montant_en_euros * TAUX_PAR_EURO[devise_cible]

    # Le yen n'a pas de centimes donc on arrondit à l'unité. 
    decimales = 0 if devise_cible == "JPY" else 2
    return round(resultat, decimales)

if __name__ == "__main__":
    print("100 EUR -> CAD :", convertir(100, "EUR", "CAD"))
    print("100 CAD -> EUR :", convertir(100, "CAD", "EUR"))
    print("1000 JPY -> USD :", convertir(1000, "JPY", "USD"))
    print("50 USD -> JPY :", convertir(50, "USD", "JPY"))

    try:
        convertir(10, "EUR", "GBP")
    except ValueError as erreur:
        print("Erreur attendue :", erreur)