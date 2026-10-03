# Fonction FaaS : reçoit une requête HTTP, convertit le montant, renvoie du JSON.
# Exemple d'appel : /api/convertir?montant=100&de=EUR&vers=CAD

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ajoute au chemin d'import de convertisseur.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from convertisseur import convertir


# Vercel cherche une classe nommée exactement "handler".
class handler(BaseHTTPRequestHandler):

    # Déclencher à chaque requête GET.
    def do_GET(self):

        # 1) Lit les paramètres de la requête HTTP
        params = parse_qs(urlparse(self.path).query)

        if not all(cle in params for cle in ("montant", "de", "vers")):
            return self._repondre(400, {"erreur": "Paramètres requis : montant, de, vers"})

        try:
            montant = float(params["montant"][0])
        except ValueError:
            return self._repondre(400, {"erreur": "Le montant doit être un nombre"})

        de = params["de"][0].upper()
        vers = params["vers"][0].upper()

        # 2) Appeler la logique métier du convertisseur
        try:
            resultat = convertir(montant, de, vers)
        except ValueError as erreur:
            return self._repondre(400, {"erreur": str(erreur)})

        # 3) Renvoyer le résultat
        self._repondre(200, {"montant": montant, "de": de, "vers": vers, "resultat": resultat})

    def _repondre(self, code, donnees):
        """Envoie une réponse HTTP au format JSON."""
        corps = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(corps)


# Bloc de test en local.
if __name__ == "__main__":
    print("Fonction disponible sur http://localhost:8000/?montant=100&de=EUR&vers=CAD")
    HTTPServer(("localhost", 8000), handler).serve_forever()