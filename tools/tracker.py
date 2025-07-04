from context import UserSessionContext
from hooks import RunHooks

class TrackerTool:
    def track_progress(self, context: UserSessionContext, progress_input: str) -> str:
        RunHooks.on_tool_start(context, "TrackerTool")
        context.progress_logs.append({"progress": progress_input})
        RunHooks.on_tool_end(context, "TrackerTool")
        return f"Progress logged: {progress_input}"