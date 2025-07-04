from agent import tool
from typing import List
from ..context import UserSessionContext
import random

@tool
async def generate_meal_plan(
    context: UserSessionContext,
    days: int = 7
) -> List[str]:
    """
    Generates a personalized meal plan based on user's dietary preferences and goals.
    
    Args:
        days: Number of days to plan for (default 7)
        context: User session context
        
    Returns:
        List of daily meal plans
    """
    if not context.diet_preferences:
        raise ValueError("No dietary preferences set. Please set preferences first.")
    
    if not context.goal:
        raise ValueError("No goal set. Please set a goal first.")
    
    # Sample meal data - in practice you'd use a more sophisticated system
    meal_templates = {
        'vegetarian': [
            "Breakfast: Greek yogurt with berries and granola\nLunch: Quinoa salad with chickpeas and veggies\nDinner: Lentil curry with brown rice",
            "Breakfast: Avocado toast with eggs\nLunch: Caprese sandwich with side salad\nDinner: Stuffed bell peppers with quinoa",
        ],
        'vegan': [
            "Breakfast: Smoothie bowl with almond butter and chia seeds\nLunch: Buddha bowl with tahini dressing\nDinner: Vegan chili with cornbread",
        ],
        'keto': [
            "Breakfast: Scrambled eggs with avocado\nLunch: Chicken Caesar salad (no croutons)\nDinner: Salmon with asparagus and hollandaise",
        ]
    }
    
    # Select appropriate meals based on preference
    base_meals = meal_templates.get(context.diet_preferences.split()[0].lower(), meal_templates['vegetarian'])
    
    # Generate plan
    plan = []
    for day in range(1, days+1):
        selected_meal = random.choice(base_meals)
        plan.append(f"Day {day}:\n{selected_meal}")
    
    context.meal_plan = plan
    return plan