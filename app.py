from flask import Flask
from config import Config
from extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    # Importer les modèles pour SQLAlchemy
    from models.user import User
    from models.conversation import Conversation
    from models.message import Message

    # Importer et enregistrer les routes après init
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")
    from routes.ConversationRoutes import conversation_bp
    app.register_blueprint(conversation_bp, url_prefix="/api")
    from routes.MessageRoutes import message_bp
    app.register_blueprint(message_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas
    app.run(debug=True)