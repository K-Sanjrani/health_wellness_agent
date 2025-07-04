from agents import tool

@tool(name="CheckinSchedulerTool")
def schedule_checkin():
    return {"status": "Check-ins scheduled weekly"}
