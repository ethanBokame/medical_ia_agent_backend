# routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
import jwt
from config import Config
from datetime import datetime, timedelta
from utils.token_required import token_required
from models.conversation import Conversation
from classes.agent import Agent
from models.message import Message

message_bp = Blueprint("message", __name__)


@message_bp.route("/message", methods=["POST"])
@token_required
def get_messages(current_user):
    data = request.get_json()
    message = Message(conversation_id=data["conversation_id"], sender="user", content=data["content"])
    db.session.add(message)
    db.session.commit()

    # 1. Récupérer l'historique des messages de cette conversation
    historique = Message.query.filter_by(
        conversation_id=data["conversation_id"]
    ).order_by(Message.created_at).all()
    
    # 2. Créer l'agent avec l'historique chargé
    agent = Agent(conversation_id=data["conversation_id"])  # ← Passer l'ID
    agent.load_history(historique)  # ← Charger l'historique
    
    # 3. Envoyer le message
    agent_response = agent.chat(data["content"])

    message = Message(conversation_id=data["conversation_id"], sender="agent", content=agent_response.choices[0].message.content)
    db.session.add(message)

    db.session.commit()
    return jsonify({
        "success": True,
        "data": message.to_dict(),
        "message": "Message envoyé avec succès"
    })