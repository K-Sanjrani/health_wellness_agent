from agents import RunHooks

hooks = RunHooks()

@hooks.on_tool_start
def log_tool_start(tool_call):
    print(f"Starting tool: {tool_call.tool.name}")

@hooks.on_handoff
def log_handoff(event):
    print(f"Handoff triggered to: {event.target_agent.name}")
