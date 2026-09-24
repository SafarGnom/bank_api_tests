import allure
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_deposit_request import CreateDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest


@allure.feature("Accounts")
@pytest.mark.api
class TestTransferBetweenAccounts:

    @allure.title("Перевод между счетами")
    @allure.description(
        "Проверка: позитивный сценарий перевод с акк1 на акк2"
    )
    def test_account_deposit(self, api_manager: ApiManager,
                             create_user_request: CreateUserRequest, db_session: Session):
        create_account_response_1 = api_manager.user_steps.create_account(create_user_request)
        create_account_response_2 = api_manager.user_steps.create_account(create_user_request)

        assert create_account_response_1.balance == 0
        assert create_account_response_2.balance == 0


        create_deposit_request = CreateDepositRequest(
            account_id=create_account_response_1.id,
            amount=9000
        )

        account_1_after_deposit = api_manager.user_steps.create_account_deposit(create_user_request,
                                                                                   create_deposit_request)

        assert account_1_after_deposit.balance == 9000

        transfer_request = TransferRequest(
            from_account_id=create_account_response_1.id,
            to_account_id=create_account_response_2.id,
            amount=1000
        )

        transfer_response = api_manager.user_steps.transfer_between_accounts(create_user_request,transfer_request)

        assert transfer_response.from_account_id == create_account_response_1.id
        assert transfer_response.to_account_id == create_account_response_2.id

        account_1_from_db = Account.get_account_id(db_session, create_account_response_1.id)
        account_2_from_db = Account.get_account_id(db_session, create_account_response_2.id)

        assert account_1_from_db.balance == 8000
        assert account_2_from_db.balance == 1000




    @allure.title("Перевод между счетами")
    @allure.description(
        "Проверка: негативный сценарий перевод с акк1 на акк2, перевод невозможен если недостаточно средств"
    )
    def test_account_deposit_invalid(self, api_manager: ApiManager,
                             create_user_request: CreateUserRequest, db_session: Session):

        create_account_response_1 = api_manager.user_steps.create_account(create_user_request)
        create_account_response_2 = api_manager.user_steps.create_account(create_user_request)

        assert create_account_response_1.balance == 0
        assert create_account_response_2.balance == 0


        create_deposit_request = CreateDepositRequest(
            account_id=create_account_response_1.id,
            amount=9000
        )

        account_1_after_deposit = api_manager.user_steps.create_account_deposit(create_user_request,
                                                                                   create_deposit_request)

        assert account_1_after_deposit.balance == 9000

        account_1_from_db = Account.get_account_id(db_session, create_account_response_1.id)
        account_2_from_db = Account.get_account_id(db_session, create_account_response_2.id)

        assert account_1_from_db.balance == 9000
        assert account_2_from_db.balance == 0

        transfer_request = TransferRequest(from_account_id=create_account_response_1.id,
                                           to_account_id=create_account_response_2.id,
                                            amount=10000)

        response_transfer_body = api_manager.user_steps.transfer_between_accounts_bad(create_user_request,transfer_request)


        account_1_from_db = Account.get_account_id(db_session, create_account_response_1.id)
        assert account_1_from_db.balance == 9000

        account_2_from_db = Account.get_account_id(db_session, create_account_response_2.id)
        assert account_2_from_db.balance == 0

        response_transfer_body_text = response_transfer_body.json()

        response_transfer_body_text["error"] = ("Insufficient funds. Current balance: 9000.00, required: 10000.00")


















