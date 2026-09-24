from pydantic import ConfigDict, Field
from src.main.api.models.base_model import BaseModel


class CreateDepositRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: int = Field(alias="accountId")
    amount: float
