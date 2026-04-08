from openai import OpenAI
from .patient import Patient
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')

if not API_KEY:
    print("⚠️ API_KEY non trouvée")

patient = Patient(14, "male", 40, 1.75)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_patient_data",
            "description": "Get patient data including age, gender, weight, and size",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def get_patient_data():
    return patient.getPatientData()

TOOL_MAPPING = {
    "get_patient_data": get_patient_data,
}

class Agent:
    def __init__(self, conversation_id=None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
            timeout=30.0,
        )
        self.model = "openai/gpt-3.5-turbo"
        self.messages = [
            {
                "role": "system",
                "content": """
                      Tu es un médecin expert pour assistant vocal. RÈGLES STRICTES :
                      
                      1. PHRASES TRÈS COURTES : Maximum 15 mots par phrase
                      2. PAS DE CARACTÈRES SPÉCIAUX : Jamais de *, -, |, #, →, **
                      3. PAS DE TABLEAUX : Les listes uniquement avec "premier", "deuxième"
                      4. UNE IDÉE PAR PHRASE : Fais des pauses naturelles
                      5. VOCABULAIRE ORAL : "je pense que" au lieu de "hypothèse diagnostique"
                      
                      EXEMPLE DE STYLE :
                      ❌ Mauvais: "**Diagnostic différentiel principal (adolescent de 14 ans)** : \n| Pathologie | Arguments |"
                      ✅ Bon: "Je pense que vous avez peut être une angine. Deux autres possibilités existent. La première est une grippe. La deuxième est un simple rhume."
                      
                      PROCESSUS OBLIGATOIRE (toujours en phrases courtes) :
                      1. D'abord, utilise OBLIGATOIREMENT get_patient_data (sans argument) pour obtenir l'âge, poids, taille, son genre
                      2. Ensuite, pose UNE SEULE question à la fois pour recueillir les symptômes
                      3. Continue à poser des questions une par une jusqu'à avoir suffisamment d'informations
                      4. Voici mon avis médical.
                      5. Enfin, propose un diagnostic
                      
                      # RÈGLES IMPORTANTES
                      - Ne pose JAMAIS plus d'une question par message
                      - N'utilise PAS get_patient_data si tu l'as déjà utilisé dans la conversation
                      - Ne donne JAMAIS de diagnostic avant d'avoir posé au moins 5
                       questions sur les symptômes
                      - Attends d'avoir reçu les données de get_patient_data avant de continuer

                      RÈGLES D'URGENCE :
                      Si vous entendez "difficultés à respirer" ou "douleur dans la poitrine", dites immédiatement :
                      "Je vous conseille d'appeler le 15 maintenant. Ce message est urgent. "
                """
            },
        ]
        self.tools = tools
        self.tool_used = False

    def load_history(self, messages):
        """Charge l'historique depuis la base de données"""
        self.messages = [
            {
                "role": "system",
                "content": """
                      Tu es un médecin expert pour assistant vocal. RÈGLES STRICTES :
                      
                      1. PHRASES TRÈS COURTES : Maximum 15 mots par phrase
                      2. PAS DE CARACTÈRES SPÉCIAUX : Jamais de *, -, |, #, →, **
                      3. PAS DE TABLEAUX : Les listes uniquement avec "premier", "deuxième"
                      4. UNE IDÉE PAR PHRASE : Fais des pauses naturelles
                      5. VOCABULAIRE ORAL : "je pense que" au lieu de "hypothèse diagnostique"
                      
                      EXEMPLE DE STYLE :
                      ❌ Mauvais: "**Diagnostic différentiel principal (adolescent de 14 ans)** : \n| Pathologie | Arguments |"
                      ✅ Bon: "Je pense que vous avez peut être une angine. Deux autres possibilités existent. La première est une grippe. La deuxième est un simple rhume."
                      
                      PROCESSUS OBLIGATOIRE (toujours en phrases courtes) :
                      1. D'abord, utilise OBLIGATOIREMENT get_patient_data (sans argument) pour obtenir l'âge, poids, taille, son genre
                      2. Ensuite, pose UNE SEULE question à la fois pour recueillir les symptômes
                      3. Continue à poser des questions une par une jusqu'à avoir suffisamment d'informations
                      4. Voici mon avis médical.
                      5. Enfin, propose un diagnostic
                      
                      # RÈGLES IMPORTANTES
                      - Ne pose JAMAIS plus d'une question par message
                      - N'utilise PAS get_patient_data si tu l'as déjà utilisé dans la conversation
                      - Ne donne JAMAIS de diagnostic avant d'avoir posé au moins 5
                       questions sur les symptômes
                      - Attends d'avoir reçu les données de get_patient_data avant de continuer

                      RÈGLES D'URGENCE :
                      Si vous entendez "difficultés à respirer" ou "douleur dans la poitrine", dites immédiatement :
                      "Je vous conseille d'appeler le 15 maintenant. Ce message est urgent. "
                """
            },
        ]
        
        for msg in messages:
            role = "assistant" if msg.sender == "agent" else "user"
            self.messages.append({
                "role": role,
                "content": msg.content
            })
        
        print(f"📚 Historique chargé: {len(messages)} messages")

    def chat(self, message):
        try:
            self.messages.append({"role": "user", "content": message})
            print(f"🔄 Appel API... (tool_used={self.tool_used})")
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=self.tools if not self.tool_used else [],
                )
            except Exception as api_error:
                print(f"❌ Erreur API: {api_error}")
                return "Désolé, je n'arrive pas à répondre pour le moment."

            if response is None:
                print("❌ Response est None")
                return "Je n'ai pas pu générer de réponse."
            
            if not hasattr(response, 'choices') or response.choices is None:
                print("❌ Response.choices est None")
                return "Erreur technique: pas de réponse de l'API."
            
            if len(response.choices) == 0:
                print("❌ Aucun choix")
                return "Aucune réponse générée."

            choice = response.choices[0]
            
            # Gestion des tool calls
            if hasattr(choice, 'finish_reason') and choice.finish_reason == 'tool_calls':
                print("🔧 Tool call détecté!")
                self.tool_used = True
                
                # ✅ ÉTAPE 1: Ajouter le message assistant avec les tool_calls
                self.messages.append(choice.message)
                
                # ✅ ÉTAPE 2: Traiter chaque tool call
                if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
                    for tool_call in choice.message.tool_calls:
                        tool_name = tool_call.function.name
                        try:
                            tool_args = json.loads(tool_call.function.arguments)
                        except:
                            tool_args = {}
                        
                        if tool_name in TOOL_MAPPING:
                            tool_response = TOOL_MAPPING[tool_name](**tool_args)
                            
                            # ✅ ÉTAPE 3: Ajouter la réponse de l'outil avec le bon ID
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_response),
                            })
                            print(f"✅ Outil {tool_name} exécuté (id: {tool_call.id})")
                
                # ✅ ÉTAPE 4: Deuxième appel pour la réponse finale
                try:
                    final_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                    )
                    
                    if final_response and final_response.choices:
                        assistant_message = final_response.choices[0].message.content
                        self.messages.append({"role": "assistant", "content": assistant_message})
                        return assistant_message
                    else:
                        return "J'ai récupéré vos données, mais je n'ai pas pu continuer."
                        
                except Exception as final_error:
                    print(f"❌ Erreur second appel: {final_error}")
                    return "J'ai récupéré vos données mais je ne peux pas continuer pour le moment."
            
            # Réponse normale (pas de tool call)
            assistant_message = choice.message.content
            if assistant_message:
                self.messages.append({"role": "assistant", "content": assistant_message})
                return assistant_message
            else:
                return "Je n'ai pas de réponse à vous donner."
            
        except Exception as e:
            print(f"❌ Erreur générale: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return f"Désolé, une erreur technique est survenue."

    def clear_history(self):
        """Réinitialiser l'historique"""
        self.messages = [
            {
                "role": "system",
                "content": "Tu es un médecin expert. Réponds en phrases courtes."
            },
        ]
        self.tool_used = False