from agent import Agent 

class Agent:
	def __init__(self, name, instructions):
		self.name = name
		self.instructions = instructions

injury_support_agent = Agent(name="InjurySupportAgent", instructions="Handle injuries and physical limitations.")
