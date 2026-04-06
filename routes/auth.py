from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
import jwt
from config import Config
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

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
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "success": True,
        "message": "Connexion réussie",
        "data": user.to_dict(),
        "token": token
    })