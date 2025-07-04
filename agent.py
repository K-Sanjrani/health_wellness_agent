from agent import Agent
from typing import Optional
from .context import UserSessionContext
from .tools.goal_analyzer import analyze_goal
from .tools.meal_planner import generate_meal_plan
from .tools.workout_recommender import recommend_workout
from .tools.scheduler import schedule_checkin
from .tools.tracker import track_progress
from .agents.escalation_agent import EscalationAgent
from .agents.nutrition_expert_agent import NutritionExpertAgent
from .agents.injury_support_agent import InjurySupportAgent
from datetime import datetime

class WellnessPlannerAgent(Agent):
    def __init__(self,name, instructions, model, tools=None, external_client=None):
        super().__init__(
            name="WellnessPlanner",
            description="AI health and wellness planner that creates personalized fitness and nutrition plans",
            tools=[analyze_goal, generate_meal_plan, recommend_workout, schedule_checkin, track_progress],
            external_client=external_client,
            model=model,
            handoffs={
                'human_coach': EscalationAgent(),
                'nutrition_expert': NutritionExpertAgent(),
                'injury_support': InjurySupportAgent()
            }
        )
    
    async def on_handoff(self, handoff_to: str, context: UserSessionContext):
        """Log handoff events"""
        note = f"Handed off to {handoff_to} at {datetime.now().isoformat()}"
        context.log_handoff(note)
        return note
    
    async def run(self, input: str, context: Optional[UserSessionContext] = None):
        # Check for handoff triggers
        if "talk to a human" in input.lower() or "real trainer" in input.lower():
            return await self.handoff('human_coach', input, context)
        
        if "diabet" in input.lower() or "allerg" in input.lower():
            return await self.handoff('nutrition_expert', input, context)
            
        if "pain" in input.lower() or "injur" in input.lower():
            return await self.handoff('injury_support', input, context)
        
        # Normal processing
        if "goal" in input.lower() or "want to" in input.lower():
            # Extract dietary preference if mentioned
            diet_keywords = ["vegetarian", "vegan", "keto", "pescatarian", "paleo"]
            diet_pref = next((kw for kw in diet_keywords if kw in input.lower()), None)
            
            return await analyze_goal(input, context, diet_pref)
        
        elif "meal" in input.lower() or "food" in input.lower() or "diet" in input.lower():
            if not context.goal:
                return "Please set your health goals first before generating a meal plan."
            return await generate_meal_plan(context=context)
        
        elif "workout" in input.lower() or "exercise" in input.lower():
            return await recommend_workout(context=context)
        
        elif "progress" in input.lower() or "update" in input.lower():
            return await track_progress(input, context)
        
        else:
            return "I can help you with health goals, meal plans, workout routines, and progress tracking. What would you like to focus on today?"