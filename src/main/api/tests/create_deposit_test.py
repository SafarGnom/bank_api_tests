import allure
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest


@allure.feature("Deposit")
@pytest.mark.api
class TestCreateDeposit:

    @allure.title("Пополнение счета")
    @allure.description(
        "Проверка: позитивный сценарий пополнения счета"
    )
    def test_account_deposit(self, api_manager: ApiManager,
                             create_user_request: CreateUserRequest, db_session: Session):
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        assert create_account_response.balance == 0

        create_deposit_request = CreateDepositRequest(
            account_id=create_account_response.id,
            amount=1000.5
        )

        create_account_for_deposit = api_manager.user_steps.create_account_deposit(create_user_request,
                                                                                   create_deposit_request)

        assert create_account_response.id == create_account_for_deposit.account_id

        deposit_amount_from_db_transaction = Transaction.get_amount(db_session, create_account_for_deposit.balance)

        assert create_account_for_deposit.balance == deposit_amount_from_db_transaction.amount




    @allure.title("Нельзя пополнить счёт на сумму меньше 1000 и больше 9000")
    @allure.description(
        "Проверка граничных значений - мин и макс суммы пополнения: 999 и 9001"
    )
    @pytest.mark.parametrize(
        "amount", [999, 9001]
    )
    def test_account_deposit_min_max(self, api_manager: ApiManager,
                                     create_user_request: CreateUserRequest, db_session: Session, amount: float):
        create_account_response = api_manager.user_steps.create_account(create_user_request)

        assert create_account_response.balance == 0

        create_deposit_request = CreateDepositRequest(
            account_id=create_account_response.id,
            amount=amount
        )

        api_manager.user_steps.create_account_deposit_bad(create_user_request, create_deposit_request)

        deposit_transaction = Transaction.get_account_id(db_session, create_account_response.id)

        assert deposit_transaction is None
