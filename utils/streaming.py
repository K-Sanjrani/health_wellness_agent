from agents import Runner
from agents import wellness_agent as starting_agent

try:
    from agents import Runner
except ImportError:
    # Fallback: define or import Runner from a local module if available
    pass  # Runner fallback not available; handle ImportError as needed

async def stream_response(agent, user_input, context):
    async for step in Runner.stream(starting_agent=agent, input=user_input, context=context):
        print(step.pretty_output)
