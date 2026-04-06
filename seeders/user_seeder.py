from app import create_app
from extensions import db
from models.user import User

app = create_app()

# seeders/user_seeder.py
from app import create_app
from extensions import db
from models.user import User

app = create_app()

with app.app_context():
    email_user = "usertest@gmail.com"

    # Crée le nouvel utilisateur
    existing_user = User.query.filter_by(email=email_user).first()
    if not existing_user:
        user = User(nom="User Test", email=email_user)
        user.set_password("user1234")
        db.session.add(user)
        db.session.commit()
        print("Utilisateur fictif créé !")
    else:
        print("Utilisateur déjà présent en BDD")