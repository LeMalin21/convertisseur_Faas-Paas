from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session
from models_BDD import db, Utilisateur

auth_bp = Blueprint("auth", __name__)


def connexion_requise(vue):
    """Décorateur : redirige vers la connexion si personne n'est connecté."""
    @wraps(vue)
    def verifier(*args, **kwargs):
        if "utilisateur_id" not in session:
            return redirect(url_for("auth.connexion"))
        return vue(*args, **kwargs)
    return verifier


@auth_bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    erreur = None

    if request.method == "POST":
        nom = request.form["nom"].strip()
        mot_de_passe = request.form["mot_de_passe"]
        utilisateur = Utilisateur.query.filter_by(nom=nom).first()

        if request.form["action"] == "inscription":
            if utilisateur:
                erreur = "Ce nom est déjà pris"
            else:
                utilisateur = Utilisateur(nom=nom)
                utilisateur.definir_mot_de_passe(mot_de_passe)
                db.session.add(utilisateur)
                db.session.commit()
        elif not utilisateur or not utilisateur.verifier_mot_de_passe(mot_de_passe):
            erreur = "Nom ou mot de passe incorrect"

        # Pas d'erreur : on retient l'utilisateur dans la session
        if not erreur:
            session["utilisateur_id"] = utilisateur.id
            session["nom"] = utilisateur.nom
            return redirect(url_for("convertisseur.accueil"))

    return render_template("connexion.html", erreur=erreur)


@auth_bp.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect(url_for("auth.connexion"))