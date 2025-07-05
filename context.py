from pydantic import BaseModel
from typing import List, Dict, Optional

class UserSessionContext(BaseModel):
    name: str
    uid: int
    age: Optional[int] = None
    height: Optional[float] = None  # Height in cm (e.g., 165.5)
    weight: Optional[float] = None  # Weight in kg (e.g., 70.0)
    handoff_logs: List[Dict] = []
    progress_logs: List[Dict] = []

    def update_user_details(self, name: str = None, age: int = None, height: float = None, weight: float = None):
        """Update user details if provided."""
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if height is not None:
            self.height = height
        if weight is not None:
            self.weight = weight