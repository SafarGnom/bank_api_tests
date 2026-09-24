from pydantic import Field, ConfigDict
from src.main.api.models.base_model import BaseModel

class CreateCreditResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: int = Field(alias="id")
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")

