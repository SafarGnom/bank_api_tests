from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.main.api.generators.creation_rule import CreationRule


class CreateDepositRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: int = Field(alias="accountId")

    amount: Annotated[
        float,
        CreationRule(regex=r'[1-8][0-9]{3}|9000|1000')
    ]

