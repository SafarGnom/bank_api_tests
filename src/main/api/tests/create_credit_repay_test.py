import allure
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_credit_repay_request import CreateCreditRepayRequest
from src.main.api.models.create_credit_request import CreateCreditRequest

from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest


@allure.feature("Credit")
@pytest.mark.api
class TestCreateCreditRepayRequest:

    @allure.title("Погашение кредита")
    @allure.description(
        "Проверка: позитивный сценарий - погашение кредита"
    )
    def test_create_credit_valid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_credit_request: CreateCreditUserRequest,
            create_credit_account
    ):
        account_before_credit = Account.get_account_id(db_session, create_credit_account.id)

        assert account_before_credit is not None

        initial_balance = account_before_credit.balance

        create_credit_request = RandomModelGenerator.generate(CreateCreditRequest)

        create_credit_request.account_id = create_credit_account.id

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request, create_credit_request)

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db is not None
        assert credit_from_db.amount == get_credit_response.amount

        repay_request = CreateCreditRepayRequest(
            credit_id=get_credit_response.credit_id,
            account_id=get_credit_response.account_id,
            amount=get_credit_response.amount
        )

        repay_response = api_manager.user_steps.repay_credit(create_user_credit_request, repay_request)

        assert repay_response.amount_deposited == get_credit_response.amount

        account_after_repay = Account.get_account_id(db_session, get_credit_response.account_id)

        assert account_after_repay is not None
        assert account_after_repay.balance == initial_balance

    @allure.title("Погашение кредита")
    @allure.description(
        "Проверка: негативный сценарий - погашение кредита"
    )
    def test_create_credit_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_credit_request: CreateCreditUserRequest,
            create_credit_account
    ):
        assert create_credit_account.balance == 0

        create_credit_request = RandomModelGenerator.generate(CreateCreditRequest)

        create_credit_request.account_id = create_credit_account.id

        get_credit_response = api_manager.user_steps.get_credit(create_user_credit_request, create_credit_request)

        assert get_credit_response.amount == create_credit_request.amount

        credit_from_db = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_from_db is not None
        assert credit_from_db.amount == get_credit_response.amount

        repay_request = CreateCreditRepayRequest(
            credit_id=get_credit_response.credit_id,
            account_id=get_credit_response.account_id,
            amount=get_credit_response.amount / 2
        )

        api_manager.user_steps.repay_credit_bad(create_user_credit_request, repay_request)

        credit_after_repay = Credit.get_credit_id(db_session, get_credit_response.credit_id)

        assert credit_after_repay is not None
        assert credit_after_repay.amount == get_credit_response.amount

        account_after_repay = Account.get_account_id(db_session, get_credit_response.account_id)

        assert account_after_repay is not None
        assert account_after_repay.balance == get_credit_response.balance
