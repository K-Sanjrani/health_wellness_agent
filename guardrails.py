from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel
from pydantic import BaseModel
from typing import List, Dict
import re   

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )


class GoalInput(BaseModel):
    quantity: float
    metric: str
    duration: str

    @validator('duration')
    def validate_duration(cls, v):
        if not re.match(r"\d+\s*(days|weeks|months|years)", v):
            raise ValueError("Duration must be like '2 months'")
        return v

class MealPlanOutput(BaseModel):
    meals: List[str]



class WorkoutPlanOutput(BaseModel):
    days: List[Dict[str, str]]
from typing import Optional
from pydantic import BaseModel, validator
import re

class GoalInput(BaseModel):
    quantity: float
    metric: str
    duration: str
    
    @validator('metric')
    def validate_metric(cls, v):
        valid_metrics = ['kg', 'lbs', 'cm', 'inches', '% body fat', 'bmi']
        if v.lower() not in [m.lower() for m in valid_metrics]:
            raise ValueError(f"Invalid metric. Must be one of: {', '.join(valid_metrics)}")
        return v.lower()
    
    @validator('duration')
    def validate_duration(cls, v):
        if not re.match(r'^\d+\s*(weeks?|months?|days?|years?)$', v.lower()):
            raise ValueError("Duration must be in format like '2 months' or '12 weeks'")
        return v.lower()

class DietaryInput(BaseModel):
    preference: str
    restrictions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    
    @validator('preference')
    def validate_preference(cls, v):
        valid_prefs = ['vegetarian', 'vegan', 'pescatarian', 'keto', 'paleo', 'mediterranean', 'none']
        if v.lower() not in [p.lower() for p in valid_prefs]:
            raise ValueError(f"Invalid dietary preference. Must be one of: {', '.join(valid_prefs)}")
        return v.lower()

def validate_goal_input(user_input: str) -> GoalInput:
    """Parse and validate goal input from user"""
    try:
        # Example parsing logic - in practice you'd use more sophisticated NLP
        parts = user_input.lower().split()
        quantity = float(parts[0])
        metric = ' '.join(parts[1:-2])
        duration = ' '.join(parts[-2:])
        return GoalInput(quantity=quantity, metric=metric, duration=duration)
    except Exception as e:
        raise ValueError(f"Could not parse goal input. Please use format like 'lose 5kg in 2 months'. Error: {str(e)}")