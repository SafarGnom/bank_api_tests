from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.main.api.generators.creation_rule import CreationRule


class CreateCreditRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_id: int = Field(alias="accountId")

    amount: Annotated[
        float,
        CreationRule(regex=r'(5000|[5-9][0-9]{3}|1[0-4][0-9]{3}|15000)')]

    term_months: Annotated[
        int,
        CreationRule(regex=r'[1-9]|1[0-2]')] = Field(alias="termMonths")
