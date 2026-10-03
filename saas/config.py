import os


class Config:

    # Clé qui signe le cookie de session
    SECRET_KEY = os.environ.get("SECRET_KEY", "cle-de-developpement")

    # SQLite en local, PostgreSQL en ligne
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///saas.db").replace(
        "postgres://", "postgresql://", 1  # format attendu par SQLAlchemy
    )

    # Adresse de la fonction FaaS
    FAAS_URL = os.environ.get("FAAS_URL", "https://convertisseur-faas-paas-seven.vercel.app/api/convertir")
    DEVISES = ["EUR", "USD", "CAD", "JPY"]

