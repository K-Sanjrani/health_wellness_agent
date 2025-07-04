from openai import Agent
from context import UserSessionContext

escalation_agent = Agent(
    name="EscalationAgent",
    instructions="Escalate to human support when requested.",
    context=UserSessionContext()
)
class EscalationAgent(Agent):
    def __init__(self, name="EscalationAgent", instructions="Handle escalations to human support."):
        super().__init__(name=name, instructions=instructions)

    async def run(self, input: str, context: UserSessionContext):
        """Handle escalation requests"""
        if "talk to a human" in input.lower() or "real trainer" in input.lower():
            note = f"Escalated to human support at {context.timestamp()}"
            context.log_handoff(note)
            return "Connecting you to a human support agent. Please hold on."
        return "No escalation needed at this time."