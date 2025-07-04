import re
from pydantic import BaseModel, ValidationError

def validate_input(user_input: str) -> bool:
    # Check for empty or overly short input
    if not user_input or len(user_input.strip()) < 3:
        print(f"Input failed: Empty or too short: {user_input}")
        return False
    
    # Validate goal format (e.g., "I want to lose 5kg in 2 months")
    goal_pattern = r"(?i)(?:i\s*want\s*to\s*)?(lose|gain)\s*(\d+)\s*(kg|lbs|pounds)(?:\s*weight)?\s*in\s*(\d+)\s*(month|week|months|weeks)"
    if "lose" in user_input.lower() or "gain" in user_input.lower():
        match = re.search(goal_pattern, user_input.lower())
        if not match:
            print(f"Input failed regex: {user_input}, Pattern: {goal_pattern}")
            return False
        print(f"Input matched: {match.groups()}")
    return True

def validate_output(response: str) -> bool:
    # Ensure response is not empty and has valid content
    try:
        if not response or len(response.strip()) < 10:
            print(f"Output failed: Empty or too short: {response}")
            return False
        return True
    except Exception as e:
        print(f"Output validation error: {e}")
        return False