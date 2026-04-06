from app import create_app
from extensions import db
from models.user import User

app = create_app()

with app.app_context():
    email_admin = "kouahodavid007@gmail.com"

    existing_user = User.query.filter_by(email=email_admin).first()
    if not existing_user:
        admin = User(nom="Kouaho David", email=email_admin)
        admin.set_password("Kouahodavid@007")
        db.session.add(admin)
        db.session.commit()
        print("Utilisateur admin créé !")
    else:
        print("Utilisateur admin déjà présent en BDD")