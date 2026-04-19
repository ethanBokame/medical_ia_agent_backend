# routes/message.py - Version complète corrigée
from flask import Blueprint, request, jsonify
from app.models.message import Message
from app.services.agent import Agent
from app.extensions import db
from utils.token_required import token_required

message_bp = Blueprint('message', __name__)

@message_bp.route("/message", methods=["POST"])
@token_required
def chat(current_user):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Aucune donnée"}), 400
        
        conversation_id = data.get("conversation_id")
        content = data.get("content")
        
        if not content:
            return jsonify({"error": "Message vide"}), 400
        
        # Sauvegarder message utilisateur
        user_msg = Message(
            conversation_id=conversation_id,
            sender="user",
            content=content
        )
        db.session.add(user_msg)
        db.session.commit()
        
        # Récupérer historique
        historique = Message.query.filter_by(
            conversation_id=conversation_id
        ).order_by(Message.created_at).all()
        
        # Créer agent et charger historique
        agent = Agent(conversation_id=conversation_id)
        agent.load_history(historique)
        
        # Obtenir réponse (c'est une string !)
        agent_response = agent.chat(content)
        
        # Vérifier que la réponse est valide
        if not agent_response or agent_response is None:
            agent_response = "Je n'ai pas pu générer de réponse."
        
        # Sauvegarder réponse agent
        agent_msg = Message(
            conversation_id=conversation_id,
            sender="agent",
            content=agent_response  # ← Directement la string
        )
        db.session.add(agent_msg)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": agent_response,
            "message": "Reponse envoyée"
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500