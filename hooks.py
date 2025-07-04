from context import UserSessionContext

class RunHooks:
    @staticmethod
    def on_agent_start(context: UserSessionContext, agent_name: str):
        context.handoff_logs.append(f"Agent {agent_name} started")

    @staticmethod
    def on_agent_end(context: UserSessionContext, agent_name: str):
        context.handoff_logs.append(f"Agent {agent_name} ended")

    @staticmethod
    def on_tool_start(context: UserSessionContext, tool_name: str):
        context.handoff_logs.append(f"Tool {tool_name} started")

    @staticmethod
    def on_tool_end(context: UserSessionContext, tool_name: str):
        context.handoff_logs.append(f"Tool {tool_name} ended")

    @staticmethod
    def on_handoff(context: UserSessionContext, target_agent: str):
        context.handoff_logs.append(f"Handoff to {target_agent}")