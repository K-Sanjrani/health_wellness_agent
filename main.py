from dotenv import load_dotenv
import os
from agent import wellness_agent
from agent import Agent, InputGuardrail, GuardrailFunctionOutput, ChatCompilations,AsysncOpenAI, Runner, RunConfig
from openai import OpenAI
from pydantic import BaseModel
import asyncio

# Initialize environment variables FIRST
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY in environment variables is not set.")

external_client = AsysncOpenAI(
api_key=gemini_api_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

  
model = {
    "model": "gemini-1.5-pro",
    "messages": [{"role": "user", "content": "Hello!"}],
    "description": "A powerful AI model for health and wellness planning.",
    "instructions": "You are a health and wellness planner. Provide personalized fitness and nutrition advice based on user input.",
    "tools": [
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
}


from agent import RunConfig

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_diabled=True,
)

# Now import components that depend on OpenAI
from agents.wellness_agent import WellnessAgent 
from guardrails import homework_guardrail, GoalInput, MealPlanOutput, WorkoutPlanOutput
import _asyncio as Async

async def main():
    agent = WellnessAgent(
        name="Health Planner",
        instructions="Provide health advice"
    )
    response = await agent.run("Suggest a meal plan")
    print(response)

from agents import Agent, Runner, AsyncOpenAI


# Import UserSessionContext
from agents.wellness_agent import UserSessionContext



async def main():
    print("Welcome to the Health Wellness Planner!")
    user_question = input("How may I help you?")

    messages = [
        "I want to lose 5kg in 2 months",
        "I'm vegetarian",
        "Suggest a meal plan",
        "I have knee pain"
    ]

    def generate_meal_plan(dietary_preferences: str, calorie_target: float):
        return {"meal_plan": f"Sample meal plan for {dietary_preferences} with {calorie_target} calories."}

    agent = Agent(
        name="health Wellness Planner",
        instructions="We make sure to provide you best plans suggested by doctors and nutritionists. We will also help you in tracking your progress and making adjustments to your plans as needed.",
        model=model,
        tools=[generate_meal_plan],
        input_guardrail=InputGuardrail(
            input_type="text",
            guardrail_functions=[
                GuardrailFunctionOutput( 
                    name="generate_meal_plan",
                    description="Generate a personalized meal plan based on dietary preferences and calorie target.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "dietary_preferences": {"type": "string", "description": "User's dietary preferences"},
                            "calorie_target": {"type": "number", "description": "Target daily calorie intake"}
                        },
                        "required": ["dietary_preferences", "calorie_target"]
                    }
                )
            ]
        )
    )

    # Example: Run the agent and print the final output
    result = await Runner.run(agent, "How may I help you?")
    print("AI Response:", result.final_output) 

if __name__ == "__main__":
    asyncio.run(main())