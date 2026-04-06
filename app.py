from flask import Flask
from config import Config
from extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    # Importer et enregistrer les routes après init
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)