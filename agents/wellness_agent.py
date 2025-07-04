import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import AsyncGenerator, Dict, List
import _asyncio as Async

# 1. Initialize OpenAI Client (Modern SDK)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Define Context Manager
class WellnessContext:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.conversation_history: List[Dict] = [
            {"role": "system", "content": "You're an AI Health Coach. Provide personalized fitness/nutrition advice."}
        ]
    
    def add_message(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

# 3. Streaming Agent
class WellnessAgent:
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_meal_plan",
                    "description": "Generate a personalized meal plan",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "dietary_preferences": {"type": "string"},
                            "calorie_target": {"type": "number"}
                        }
                    }
                }
            }
        ]

    async def stream_response(self, context: WellnessContext, user_input: str) -> AsyncGenerator[str, None]:
        context.add_message("user", user_input)
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context.conversation_history,
            tools=self.tools,
            stream=True
        )
        
        full_response = []
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response.append(content)
                yield content
        
        context.add_message("assistant", "".join(full_response))

# 4. Example Usage
async def main():
    agent = WellnessAgent()
    context = WellnessContext("user123")
    
    prompts = [
        "I want to lose 5kg in 2 months",
        "I'm vegetarian",
        "Suggest a meal plan for 1800 calories"
    ]
    
    for prompt in prompts:
        print(f"\nUser: {prompt}")
        print("AI:", end="")
        
        async for chunk in agent.stream_response(context, prompt):
            print(chunk, end="", flush=True)
        
        await Async.sleep(1)  # Pause between messages

if __name__ == "__main__":
    Async.run(main())