import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_credit_request import CreateCreditRequest


@allure.feature("Credit")
@pytest.mark.api
class TestCreateCredit:

    @allure.title("Запрос на получение кредита")
    @allure.description(
        "Проверка: позитивный сценарий по получению кредита"
    )
    def test_create_credit_valid(self, db_session: Session, api_manager: ApiManager, create_user_credit_request: CreateCreditRequest):

        account_response = api_manager.user_steps.create_account(create_user_credit_request)

        create_credit_request = CreateCreditRequest(account_id=account_response.id, amount=5000, term_months=12)

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request,create_credit_request)

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db.id == get_credit_response.credit_id
        assert credit_from_db.amount == get_credit_response.amount





    @allure.title("Нельзя взять второй кредит на другой счёт")
    @allure.description(
        "Проверка: негативный сценарий - если у пользователя уже есть активный кредит на одном счёте, "
        "он не может оформить второй кредит на другом счёте."
    )
    def test_credit_cannot_be_taken_on_second_account(self, db_session: Session, api_manager: ApiManager,
                                                      create_user_credit_request: CreateCreditRequest):

        account_1 = api_manager.user_steps.create_account(create_user_credit_request)
        account_2 = api_manager.user_steps.create_account(create_user_credit_request)

        credit_1 = CreateCreditRequest(
            account_id=account_1.id,
            amount=10000,
            term_months=10
        )

        first_response = api_manager.user_steps.get_credit(create_user_credit_request, credit_1)

        assert first_response.amount == 10000

        credit_2 = CreateCreditRequest(
            account_id=account_2.id,
            amount=12000,
            term_months=6
        )

        second_response = api_manager.user_steps.get_credit_bad(create_user_credit_request, credit_2)

        second_credit_in_db = Credit.get_credit_id(db_session, account_2.id)

        assert second_credit_in_db is None,(
            f"Второй кредит не должен был создаться, но найден: {second_credit_in_db}")

        assert second_response.json()["error"]=="Only one active credit allowed per user"











































