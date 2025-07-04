import re
from context import UserSessionContext
from hooks import RunHooks

class GoalAnalyzerTool:
    def analyze_goal(self, user_input: str, context: UserSessionContext) -> dict:
        RunHooks.on_tool_start(context, "GoalAnalyzerTool")
        pattern = r"(?i)(?:i\s*want\s*to\s*)?(lose|gain)\s*(\d+)\s*(kg|lbs|pounds)(?:\s*weight)?\s*in\s*(\d+)\s*(month|week|months|weeks)"
        match = re.search(pattern, user_input.lower())
        if match:
            goal = {
                "description": match.group(1),
                "quantity": int(match.group(2)),
                "metric": match.group(3),
                "duration": f"{match.group(4)} {match.group(5)}"
            }
        else:
            goal = {"description": "unknown", "quantity": 0, "metric": "unknown", "duration": "unknown"}
        RunHooks.on_tool_end(context, "GoalAnalyzerTool")
        return goal