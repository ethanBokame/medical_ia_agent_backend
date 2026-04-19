from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt
from app.seeders.user import seedUsers 
from flask_cors import CORS

def create_app():

    # create flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # import models
    from models.user import User
    from models.conversation import Conversation
    from models.message import Message

    # import routes
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")
    from routes.conversation import conversation_bp
    app.register_blueprint(conversation_bp, url_prefix="/api")
    from routes.message import message_bp
    app.register_blueprint(message_bp, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if not exits
        seedUsers(app)  # Create a fake user
    app.run(debug=True)