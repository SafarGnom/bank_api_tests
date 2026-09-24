import allure
import pytest
from requests import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest

@allure.feature("Accounts")
@pytest.mark.api
class TestCreateAccount:

    @allure.title("Создание банковского счета")
    @allure.description(
        "Проверка: позитивный сценарий - открытие счета"
    )
    def test_account_creation(self, db_session: Session, api_manager: ApiManager,
                              create_user_request: CreateUserRequest):

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_id(db_session, response.id)
        assert account_from_db.id == response.id, 'aкк не создан, акк нет в бд'
        assert account_from_db.balance is not None, 'Поле баланса для созданного пользака отсутсвует в бд'




    @allure.title("Нельзя создать больше двух банковских счетов")
    @allure.description(
        "Проверка: негативный сценарий - пользователь не может создать "
        "более двух банковских счетов"
    )
    def test_account_creation_invalid(self,db_session: Session,api_manager: ApiManager,
            create_user_request: CreateUserRequest):


        account_1 = api_manager.user_steps.create_account(create_user_request)

        assert account_1.balance == 0

        account_1_from_db = Account.get_account_id(db_session,account_1.id)

        assert account_1_from_db is not None
        assert account_1_from_db.id == account_1.id

        account_2 = api_manager.user_steps.create_account(create_user_request)

        assert account_2.balance == 0

        account_2_from_db = Account.get_account_id(db_session,account_2.id)

        assert account_2_from_db is not None
        assert account_2_from_db.id == account_2.id

        third_response = api_manager.user_steps.create_account_bad(create_user_request)

        assert third_response.json()["error"] == ("User already has maximum number of accounts(2)")









