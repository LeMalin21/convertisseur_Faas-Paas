import requests
from flask import current_app


class ErreurConversion(Exception):
    """Levée quand la conversion échoue (FaaS injoignable ou données refusées)."""


def convertir(montant, de, vers):
    """Appelle la fonction FaaS et renvoie son résultat sous forme de dictionnaire."""
    try:
        reponse = requests.get(
            current_app.config["FAAS_URL"],
            params={"montant": montant, "de": de, "vers": vers},
            timeout=10,
        )
        donnees = reponse.json()
    except (requests.RequestException, ValueError):
        raise ErreurConversion("Le service de conversion est injoignable")

    if reponse.status_code != 200:
        raise ErreurConversion(donnees.get("erreur", "Erreur inconnue"))

    return donnees