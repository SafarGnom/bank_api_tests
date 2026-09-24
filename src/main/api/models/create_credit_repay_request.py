from pydantic import ConfigDict, Field
from src.main.api.models.base_model import BaseModel


class CreateCreditRepayRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: float
