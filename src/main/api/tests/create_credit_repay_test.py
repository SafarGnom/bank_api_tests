import allure
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_credit_repay_request import CreateCreditRepayRequest
from src.main.api.models.create_credit_request import CreateCreditRequest

from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@allure.feature("Credit")
@pytest.mark.api
class TestCreateCreditRepayRequest:

    @allure.title("Погашение кредита")
    @allure.description(
        "Проверка: позитивный сценарий - погашение кредита"
    )
    def test_create_credit_valid(self, db_session: Session, api_manager: ApiManager,
                                 create_user_credit_request: CreateCreditRequest):
        account_response = api_manager.user_steps.create_account(create_user_credit_request)

        create_credit_request = CreateCreditRequest(account_id=account_response.id, amount=10000, term_months=12)

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request, create_credit_request)

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db.amount == get_credit_response.amount

        repay_request = CreateCreditRepayRequest(credit_id=get_credit_response.credit_id,
                                                 account_id=get_credit_response.account_id,
                                                 amount=get_credit_response.amount)

        repay_response = api_manager.user_steps.repay_credit(create_user_credit_request, repay_request)

        assert repay_response.amount_deposited == get_credit_response.amount

        credit_after_repay = Account.get_account_id(db_session, get_credit_response.account_id)

        assert credit_after_repay.balance == 0

    @allure.title("Погашение кредита")
    @allure.description(
        "Проверка: негативный сценарий - погашение кредита"
    )
    def test_create_credit_invalid(self, db_session: Session, api_manager: ApiManager,
                                   create_user_credit_request: CreateCreditRequest):
        account_response = api_manager.user_steps.create_account(create_user_credit_request)

        assert account_response.balance == 0

        create_credit_request = CreateCreditRequest(
            account_id=account_response.id,
            amount=10000,
            term_months=12
        )

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request, create_credit_request)

        assert get_credit_response.amount == 10000

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db.amount == 10000

        repay_request = CreateCreditRepayRequest(
            credit_id=get_credit_response.credit_id,
            account_id=get_credit_response.account_id,
            amount=5000
        )

        repay_response = api_manager.user_steps.repay_credit_bad(create_user_credit_request, repay_request)

        repay_response.json()["error"] == ("Repayment amount exceeds remaining debt")

        credit_after_repay = Credit.get_credit_id(db_session,get_credit_response.credit_id)

        assert credit_after_repay.amount == 10000

        account_after_repay = Account.get_account_id(db_session, get_credit_response.account_id)

        assert account_after_repay.balance == 10000
