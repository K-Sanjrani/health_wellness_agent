from openai.agents import tool
from guardrails import WorkoutPlanOutput

@tool(name="WorkoutRecommenderTool")
def recommend_workouts(goal: dict) -> WorkoutPlanOutput:
    return WorkoutPlanOutput(days=[{"day": "Monday", "workout": "Strength training"}])
