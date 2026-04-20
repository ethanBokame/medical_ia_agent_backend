from services.agent import Agent
from pprint import pprint
from rich import print as rprint

agent = Agent()

while True:

    # first message of agent
    if len(agent.messages) == 2:
        print("Agent: " + agent.messages[1]["content"])

    # user input
    user_input = input("Vous: ")
    response = agent.chat(user_input)

    # agent response
    rprint(response)
