from pydantic import ConfigDict, Field

from src.main.api.models.base_model import BaseModel


class CreateDepositResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: int = Field(alias="id")
    balance: float
