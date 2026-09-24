from pydantic import ConfigDict, Field

from src.main.api.models.base_model import BaseModel


class TransferResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_account_id: int = Field(alias="fromAccountId")

    to_account_id: int = Field(alias="toAccountId")

    from_account_id_balance: float = Field(alias="fromAccountIdBalance")