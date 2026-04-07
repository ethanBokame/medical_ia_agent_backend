from extensions import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK vers users
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relations
    user = db.relationship("User", backref=db.backref("conversations", lazy=True))
    messages = db.relationship(
        "Message",
        backref="conversation",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }