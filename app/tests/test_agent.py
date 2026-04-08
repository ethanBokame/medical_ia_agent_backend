from app.services.agent import Agent

agent = Agent()

while True:

  # first message of agent
  if len(agent.messages) == 2:
    print("Agent: " + agent.messages[1]['content'])
  
  # user input
  user_input = input("Vous: ")
  response = agent.chat(user_input)

  # agent response
  print(response.choices[0].message.content)