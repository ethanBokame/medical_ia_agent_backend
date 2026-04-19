# routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
import jwt
from config import Config
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint("auth", __name__)


# --- LOGIN ---
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email et mot de passe requis"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Email ou mot de passe incorrect"}), 401

    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
        Config.SECRET_KEY,
        algorithm="HS256",
    )

    # Mettre le token à l'intérieur de "data"
    user_data = user.to_dict()
    user_data["token"] = token

    return jsonify({"success": True, "data": user_data, "message": "Connexion réussie"})


# --- register ---
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nom = data.get("nom")
    email = data.get("email")
    password = data.get("password")

    user = User(nom=nom, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
        Config.SECRET_KEY,
        algorithm="HS256",
    )

    # Mettre le token à l'intérieur de "data"
    user_data = user.to_dict()
    user_data["token"] = token

    return jsonify(
        {"success": True, "data": user_data, "message": "Inscription réussie"}
    )


# --- DÉCORATEUR POUR TOKEN ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token manquant"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expiré"}), 401
        except (jwt.InvalidTokenError, Exception):
            return jsonify({"message": "Token invalide"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# --- PROFILE ---
@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(current_user):
    return jsonify(
        {
            "success": True,
            "data": current_user.to_dict(),
            "message": "Infos de l'utilisateur connecté",
        }
    )
