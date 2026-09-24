from pydantic import ConfigDict, Field
from src.main.api.models.base_model import BaseModel


class CreateCreditRepayResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    credit_id: int = Field(alias="creditId")
    amount_deposited: int = Field(alias="amountDeposited")