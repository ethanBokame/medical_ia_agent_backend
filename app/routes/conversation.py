# routes/auth.py
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
import jwt
from utils.token_required import token_required
from app.models.conversation import Conversation

# Blueprint for conversation routes
conversation_bp = Blueprint("conversation", __name__)


# Get all conversations for a user
@conversation_bp.route("/conversations", methods=["GET"])
@token_required
def get_conversations(current_user):
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    return jsonify(
        {
            "success": True,
            "data": [conversation.to_dict() for conversation in conversations],
            "message": "Conversations récupérées avec succès",
        }
    )


# Get a specific conversation with its messages
@conversation_bp.route("/conversation/<int:conversation_id>", methods=["GET"])
@token_required
def get_conversation(current_user, conversation_id):
    conversation = Conversation.query.filter_by(
        id=conversation_id, user_id=current_user.id
    ).first()

    if not conversation:
        return jsonify({"success": False, "message": "Conversation non trouvée"}), 404
    return jsonify(
        {
            "success": True,
            "data": conversation.to_dict(),
            "message": "Conversation récupérée avec succès",
        }
    )


# Create a new conversation
@conversation_bp.route("/conversation", methods=["POST"])
@token_required
def create_conversation(current_user):
    data = request.get_json()
    conversation = Conversation(user_id=current_user.id)
    db.session.add(conversation)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": conversation.to_dict(),
            "message": "Conversation créée avec succès",
        }
    )
