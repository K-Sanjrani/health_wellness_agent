from agents import tool

@tool(name="ProgressTrackerTool")
def update_progress(log: str):
    return {"log": log, "status": "Progress updated"}
