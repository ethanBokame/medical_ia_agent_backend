# test_db.py
from app import app
from extensions import db
from sqlalchemy import inspect

# IMPORTANT: Importer les modèles APRÈS db mais AVANT create_all
from models.user import User  # ← Ajoutez cette ligne
# from models.conversation import Conversation  # Si vous avez d'autres modèles

with app.app_context():
    print("🔗 URI de connexion:", db.engine.url)
    
    # Créer les tables (si elles n'existent pas)
    print("📊 Création des tables...")
    db.create_all()
    
    # Vérifier les tables après création
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"📋 Tables trouvées: {tables}")
    
    if tables:
        print("✅ Tables créées avec succès !")
    else:
        print("❌ Aucune table créée - vérifiez vos modèles")