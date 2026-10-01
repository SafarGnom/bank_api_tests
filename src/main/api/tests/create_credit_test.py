import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest


@allure.feature("Credit")
@pytest.mark.api
class TestCreateCredit:

    @allure.title("Запрос на получение кредита")
    @allure.description(
        "Проверка: позитивный сценарий по получению кредита"
    )
    def test_create_credit_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_credit_request: CreateCreditUserRequest,
            create_credit_account
    ):
        generated_credit = RandomModelGenerator.generate(CreateCreditRequest)

        create_credit_request = CreateCreditRequest(
            account_id=create_credit_account.id,
            amount=generated_credit.amount,
            term_months=generated_credit.term_months
        )

        account_from_db = Account.get_account_id(db_session, create_credit_account.id)

        assert account_from_db is not None

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request, create_credit_request)

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db is not None
        assert credit_from_db.id == get_credit_response.credit_id
        assert credit_from_db.amount == get_credit_response.amount


    @allure.title("Нельзя взять второй кредит на другой счёт")
    @allure.description(
        "Проверка: негативный сценарий - если у пользователя уже есть активный "
        "кредит на одном счёте, он не может оформить второй кредит на другом счёте."
    )
    def test_credit_cannot_be_taken_on_second_account(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_credit_request: CreateCreditUserRequest,
            create_two_credit_accounts
    ):
        account_1, account_2 = create_two_credit_accounts

        generated_credit_1 = RandomModelGenerator.generate(CreateCreditRequest)

        credit_1 = CreateCreditRequest(
            account_id=account_1.id,
            amount=generated_credit_1.amount,
            term_months=generated_credit_1.term_months
        )

        first_response = api_manager.user_steps.get_credit(create_user_credit_request, credit_1)

        assert first_response.amount == credit_1.amount

        generated_credit_2 = RandomModelGenerator.generate(CreateCreditRequest)

        credit_2 = CreateCreditRequest(
            account_id=account_2.id,
            amount=generated_credit_2.amount,
            term_months=generated_credit_2.term_months
        )

        second_response = api_manager.user_steps.get_credit_bad(create_user_credit_request, credit_2)

        second_credit_in_db = Credit.get_credit_id(db_session, account_2.id)

        assert second_credit_in_db is None

        assert second_response.json()["error"] == (
            "Only one active credit allowed per user")
