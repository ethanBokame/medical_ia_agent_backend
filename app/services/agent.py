from openai import OpenAI
from .patient import Patient
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis .env
API_KEY = os.environ.get('API_KEY')

patient = Patient(14, "male", 40, 1.75) # Création d'une instance patient

# Définition des outils pour l'API
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

# Mapping des noms d'outils vers les fonctions
def get_patient_data():
    return patient.getPatientData()

TOOL_MAPPING = {
    "get_patient_data": get_patient_data,
}

class Agent:
    """A simple AI agent that can answer questions"""

    def __init__(self, conversation_id=None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        self.model = "openai/gpt-oss-120b"
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
                      "Je vous conseille d'appeler le 15 maintenant. Ce message est urgent."

                      """

          },
          # {
          #   "role": "assistant", 
          #   "content": "Bonjour, je suis votre assistant médical. Pour commencer, pourriez-vous me décrire vos symptômes ?"
          # }
        ]
        self.tools = tools


    def load_history(self, messages):
        """Load conversation history"""
        for message in messages:
            self.messages.append({
                "role": message.sender,
                "content": message.content
            })
      
    def chat(self, message):
        """Process a user message and return a response"""

        # Store user input in short-term memory
        self.messages.append({"role": "user", "content": message})

        # First response from the model
        response = self.client.chat.completions.create(
            model=self.model,
            tools=tools,
            messages=self.messages
        )

        # Check if the model wants to call a tool
        if response.choices[0].finish_reason == 'tool_calls':
            print("Tool call détecté!")
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_response = TOOL_MAPPING[tool_name](**tool_args)
                self.messages.append({
                  "role": "tool",
                  "tool_call_id": tool_call.id,
                  "content": json.dumps(tool_response),
                })

        # Second response from the model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        # Store assistant response in short-term memory
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response

