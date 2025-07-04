from context import UserSessionContext
from hooks import RunHooks

class EscalationAgent:
    def handle_escalation(self, user_input: str, context: UserSessionContext) -> str:
        RunHooks.on_agent_start(context, "EscalationAgent")
        response = "Your request has been escalated to a human trainer. You will be contacted soon."
        RunHooks.on_agent_end(context, "EscalationAgent")
        return response