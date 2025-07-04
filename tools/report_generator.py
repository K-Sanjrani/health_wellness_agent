
from fpdf import FPDF #ignore[reportMissingModuleSource]

import os

def generate_pdf_report(name: str, meal_plan: list, workout_plan: dict) -> dict:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"{name}'s Health Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Meal Plan", ln=True)
    for day, meal in enumerate(meal_plan, 1):
        pdf.cell(200, 10, txt=f"Day {day}: {meal}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Workout Plan", ln=True)
    for day in workout_plan.get("days", []):
        pdf.cell(200, 10, txt=f"{day['day']}: {day['workout']}", ln=True)

    path = f"{name.replace(' ', '_').lower()}_health_report.pdf"
    pdf.output(path)
    return {"status": "PDF generated", "file_path": path}
