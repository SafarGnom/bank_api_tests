import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixtures import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@allure.feature("Admin")
@pytest.mark.api
class TestCreateUser:

    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]

    )
    @allure.title("Создание пользователя")
    @allure.description(
        "Проверка: позитивный сценарий - создание пользователя"
    )
    def test_create_user_valid(self, api_manager: ApiManager,
                               create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в БД'




    @allure.title("Создание пользователя - невалидный пароль и логин")
    @allure.description(
        "Проверка: негативный сценарий - создание пользователя"
    )
    @pytest.mark.parametrize(
        "username,password",
        [pytest.param("абв", "Pas!sw0rd"),
         pytest.param("ab", "Pas!sw0rd"),
         pytest.param("abv!", "Pas!sw0rd"),
         pytest.param("Max11", "Pas!sw0rд"),
         pytest.param("Max12", "Pas!sw0"),
         pytest.param("Max13", "pas!sw0rd"),
         pytest.param("Max14", "PAS!SW0RD"),
         pytest.param("Max15", "PASSW0RD"),
         pytest.param("Max15", "PASSWRRD"), ]
    )
    def test_create_user_invalid(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Пользователь создан, ошибка'
