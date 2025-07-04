from context import UserSessionContext
from hooks import RunHooks

class SchedulerTool:
    def schedule_reminders(self, context: UserSessionContext) -> str:
        RunHooks.on_tool_start(context, "SchedulerTool")
        reminders = []
        if context.meal_plan:
            reminders.append("Daily meal reminders set for breakfast, lunch, and dinner.")
        if context.workout_plan:
            reminders.append("Workout reminders set for scheduled exercise times.")
        RunHooks.on_tool_end(context, "SchedulerTool")
        return "\n".join(reminders) or "No reminders scheduled."