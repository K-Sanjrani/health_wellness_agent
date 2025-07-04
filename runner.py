# runner.py
import openai
from typing import AsyncGenerator
from agents import Runner
from agents import triage_agent  
from agents import UserSessionContext  

async def main():
    result = await Runner.run(triage_agent, "What is the capital of France?")
    print(result.final_output)

class Runner:
    def __init__(self, api_key: str = None):
        if api_key:
            openai.api_key = api_key
        
    async def stream(self, starting_agent, input: str, context: UserSessionContext) -> AsyncGenerator:
        """Simulate streaming conversation"""
        agent = starting_agent()
        response = await agent.run(input, context)
        
        # Simulate streaming by yielding chunks
        for chunk in self._chunk_response(response):
            yield chunk
    
    def _chunk_response(self, response: str, chunk_size: int = 20):
        """Split response into chunks for streaming effect"""
        for i in range(0, len(response), chunk_size):
            yield {
                "content": response[i:i+chunk_size],
                "pretty_output": response[i:i+chunk_size]
            }