from agents import Agent
from typing import Optional
from ..context import UserSessionContext

class NutritionExpertAgent(Agent):
    def __init__(self):
        super().__init__(
            name="NutritionExpert",
            description="Specialized agent for complex dietary needs and nutrition planning",
            tools=[]  # Could add specialized tools here
        )
    
    async def run(self, input: str, context: Optional[UserSessionContext] = None):
        if "diabet" in input.lower():
            return "As a nutrition expert, I recommend focusing on low glycemic index foods and consistent meal timing to manage blood sugar levels. Would you like me to create a specialized diabetes-friendly meal plan?"
        
        if "allerg" in input.lower():
            return "I can help adjust your meal plan to accommodate allergies. Please tell me which foods you're allergic to."
        
        return "As your nutrition specialist, I can help with complex dietary needs. What specific concerns would you like to discuss?"