from typing import List, Any

from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, create_obj: List[Any]):
        self.admin_steps = AdminSteps(create_obj)
        self.user_steps = UserSteps(create_obj)
