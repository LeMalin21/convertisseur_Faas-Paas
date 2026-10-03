from flask import Flask
from config import Config
from models_BDD import db
from routes.auth import auth_bp
from routes.convertisseur import convertisseur_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)          

    db.init_app(app)                       
    with app.app_context():
        db.create_all()                    

    app.register_blueprint(auth_bp)        
    app.register_blueprint(convertisseur_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)