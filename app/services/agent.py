from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv()
API_KEY = os.environ.get('API_KEY')

if not API_KEY:
    print("API_KEY non trouvée")

tools = []

class Agent:
    def __init__(self, conversation_id=None):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
            timeout=30.0,
        )
        self.model = "openai/gpt-oss-120b:free"
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
                      1. Pose UNE SEULE question à la fois pour recueillir les symptômes
                      2. Continue à poser des questions une par une jusqu'à avoir suffisamment d'informations
                      3. Voici mon avis médical.
                      4. Enfin, propose un diagnostic
                      
                      # RÈGLES IMPORTANTES
                      - Ne pose JAMAIS plus d'une question par message
                      - N'utilise PAS get_patient_data si tu l'as déjà utilisé dans la conversation
                      - Ne donne JAMAIS de diagnostic avant d'avoir posé au moins 5 questions sur les symptômes
                      - Attends d'avoir reçu les données de get_patient_data avant de continuer

                      RÈGLES D'URGENCE :
                      Si vous entendez "difficultés à respirer" ou "douleur dans la poitrine", dites immédiatement :
                      "Je vous conseille d'appeler le 112 maintenant. Ce message est urgent. "
                """
            },
            {
              "role": "assistant",
              "content": "Bonjour, je suis JARVIS, votre agent ia spécialisé en diagnostics médicaux. Quels sont vos symptômes ?"
            }
        ]
        # self.tools = tools

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
                      2. Présente le patient avec ses informations récupérées
                      3. Ensuite, pose UNE SEULE question à la fois pour recueillir les symptômes
                      4. Continue à poser des questions une par une jusqu'à avoir suffisamment d'informations
                      5. Voici mon avis médical.
                      6. Enfin, propose un diagnostic
                      
                      # RÈGLES IMPORTANTES
                      - Ne pose JAMAIS plus d'une question par message
                      - N'utilise PAS get_patient_data si tu l'as déjà utilisé dans la conversation
                      - Ne donne JAMAIS de diagnostic avant d'avoir posé au moins 5
                       questions sur les symptômes
                      - Attends d'avoir reçu les données de get_patient_data avant de continuer

                      RÈGLES D'URGENCE :
                      Si vous entendez "difficultés à respirer" ou "douleur dans la poitrine", dites immédiatement :
                      "Je vous conseille d'appeler le 112 maintenant. Ce message est urgent. "
                """
            },
            {
                "role": "assistant",
                "content": "Bonjour, je suis JARVIS, votre agent ia spécialisé en diagnostics médicaux. Décrivez moi vos symptômes afin que je puisse vous aider"
            }
        ]
        
        for msg in messages:
            role = "assistant" if msg.sender == "agent" else "user"
            self.messages.append({
                "role": role,
                "content": msg.content
            })
        
        print(f"Historique chargé: {len(messages)} messages")

    def chat(self, message):
      # add user message to history
      self.messages.append({"role": "user", "content": message})
          
      # get response from agent
      response1 = self.client.chat.completions.create(
          model=self.model,
          messages=self.messages,
          tools=tools
      ).choices[0].message

      # check if agent want to use a tool
      if response1.tool_calls:
        tool_name = response1.tool_calls[0].function.name
        tools_args = json.loads(response1.tool_calls[0].function.arguments)
        tool_response = TOOL_MAPPING[tool_name](**tools_args)
        print("Le LLM a choisis l'outil : ", tool_name)
        self.messages.append({
            "role": "tool",
            "tool_call_id": response1.tool_calls[0].id,
            "content": json.dumps(tool_response),
        })

        response2 = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=tools
        ).choices[0].message

        return response2.content

      print("Le LLM n'a pas utilisé d'outil et a répondu directement")
      return response1.content

    def clear_history(self):
        """Réinitialiser l'historique"""
        self.messages = [
            {
                "role": "system",
                "content": "Tu es un médecin expert. Réponds en phrases courtes."
            },
        ]
        self.tool_used = False