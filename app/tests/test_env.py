#!/usr/bin/env python
# test_openrouter.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.environ.get('API_KEY')
print(f"🔑 Clé API: {'✅ Présente' if API_KEY else '❌ MANQUANTE'}")

if not API_KEY:
    print("❌ Créez un fichier .env avec: API_KEY=votre_clé")
    exit(1)

try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
        timeout=30
    )
    
    print("🔄 Test de connexion à OpenRouter...")
    
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",  # Modèle stable
        messages=[{"role": "user", "content": "Dis 'Test réussi'"}],
        max_tokens=20
    )
    
    print(f"✅ Succès!")
    print(f"Réponse: {response.choices[0].message.content}")
    print(f"Response.choices: {response.choices}")  # Ne doit pas être None
    
except Exception as e:
    print(f"❌ Erreur: {type(e).__name__}: {e}")