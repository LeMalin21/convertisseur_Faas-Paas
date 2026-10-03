from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Objet rattaché à l'application dans app.py
db = SQLAlchemy()


class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)

    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe, mot_de_passe)


class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), nullable=False)
    montant = db.Column(db.Float)
    de = db.Column(db.String(3))
    vers = db.Column(db.String(3))
    resultat = db.Column(db.Float)

    @staticmethod
    def historique(utilisateur_id, limite=10):
        return (Conversion.query
                .filter_by(utilisateur_id=utilisateur_id)
                .order_by(Conversion.id.desc())
                .limit(limite)
                .all())