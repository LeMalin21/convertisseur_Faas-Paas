from flask import Blueprint, render_template, request, session, current_app
from models_BDD import db, Conversion
from faas_client import convertir, ErreurConversion
from routes.auth import connexion_requise

convertisseur_bp = Blueprint("convertisseur", __name__)


@convertisseur_bp.route("/", methods=["GET", "POST"])
@connexion_requise
def accueil():
    resultat = None
    erreur = None

    if request.method == "POST":
        try:
            resultat = convertir(request.form["montant"], request.form["de"], request.form["vers"])
        except ErreurConversion as e:
            erreur = str(e)
        else:
            db.session.add(Conversion(
                utilisateur_id=session["utilisateur_id"],
                montant=resultat["montant"],
                de=resultat["de"],
                vers=resultat["vers"],
                resultat=resultat["resultat"],
            ))
            db.session.commit()

    return render_template(
        "index.html",
        devises=current_app.config["DEVISES"],
        resultat=resultat,
        erreur=erreur,
        historique=Conversion.historique(session["utilisateur_id"]),
        nom=session["nom"],
    )