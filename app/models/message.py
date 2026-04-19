from app.extensions import db, bcrypt
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    sender = db.Column(db.Enum("user", "agent"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
      return {
          "id": self.id,
          "conversation_id": self.conversation_id,
          "sender": self.sender,
          "content": self.content,
          "created_at": self.created_at.isoformat(),
          "updated_at": self.updated_at.isoformat() if self.updated_at else None
      }