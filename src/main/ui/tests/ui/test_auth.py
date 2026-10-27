import pytest

from ui.steps.catalog_steps import CatalogSteps
from ui.steps.login_steps import LoginSteps
from utils.constants import Urls

@pytest.mark.ui
class TestAuth:

    def test_auth(self,page):
        steps = LoginSteps(page)
        steps.open_login_page().login("standard_user", "secret_sauce")
        assert page.url == "https://www.saucedemo.com/inventory.html"

    def test_login_locked_out_user(self,page):
        steps = LoginSteps(page)
        steps.open_login_page().login("locked_out_user", "secret_sauce")
        assert page.url == "https://www.saucedemo.com/"
        error_text = steps.get_error_text()
        assert "locked out" in error_text

    def test_logout(self,page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login("standard_user", "secret_sauce")
        assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

        catalog.logout()
        assert page.url.rstrip("/") == Urls.BASE.rstrip("/"), \
            "Ожидаем возврат на страницу логина"

    def test_logout_visual_user(self,page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login("visual_user", "secret_sauce")
        assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

        catalog.logout()
        assert page.url.rstrip("/") == Urls.BASE.rstrip("/"), \
            "Ожидаем возврат на страницу логина"

