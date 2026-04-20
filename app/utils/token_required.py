# utils/token_required.py
from functools import wraps
from flask import request, jsonify  # ← AJOUTER request ici
import jwt
from app.config import Config
from app.models.user import User

# --- DÉCORATEUR POUR TOKEN ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token manquant"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expiré"}), 401
        except (jwt.InvalidTokenError, Exception):
            return jsonify({"message": "Token invalide"}), 401

        return f(current_user, *args, **kwargs)
    return decorated