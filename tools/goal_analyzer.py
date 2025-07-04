from agent import Tool
from ..context import UserSessionContext
from ..guardrails import GoalInput
from typing import Dict
from ..context import RunContextWrapper

class GoalAnalyzerTool(Tool):
    name = "GoalAnalyzerTool"
    description = "Analyzes user fitness goals and extracts structured information"

    async def run(self, input: str, context: RunContextWrapper[UserSessionContext]) -> Dict:
        goal_input = GoalInput(text=input)
        goal_parts = goal_input.text.lower().split()
        goal_type = goal_parts[0]  # lose/gain
        amount = goal_parts[1]     # 5
        unit = goal_parts[2]       # kg/lbs
        time_frame = f"{goal_parts[4]} {goal_parts[3]}"  # 2 months
        
        structured_goal = {
            "type": goal_type,
            "target": f"{amount}{unit}",
            "time_frame": time_frame
        }
        
        # Update context
        context.current.goal = structured_goal
        return structured_goal
