from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage
from utils.constants import Urls


class CatalogPage(BasePage):
    URL = Urls.BASE

    def __init__(self, page: Page):
        super().__init__(page)

        self.product_cards = page.locator(".inventory_item")
        self.sort_select = page.locator(".product_sort_container")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

        expect(self.page).to_have_url(Urls.INVENTORY)
        self.product_cards.first.wait_for(state="visible")

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

    def sort_items(self, option: str):
        self.sort_select.select_option(option)

    def add_to_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")

        if button.inner_text() == "Add to cart":
            button.click()

        return button

    def remove_from_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")

        if button.inner_text() == "Remove":
            button.click()
            expect(button).to_have_text("Add to cart")

        return button

    def get_products_count(self) -> int:
        expect(self.product_cards.first).to_be_visible()
        return self.product_cards.count()

    def get_product_names(self) -> list[str]:
        return self.product_cards.locator(
            ".inventory_item_name"
        ).all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices = self.product_cards.locator(
            ".inventory_item_price"
        ).all_text_contents()

        return [float(price.replace("$", "")) for price in prices]

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())

        return 0

    def open_product_details(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)

        name = card.locator(".inventory_item_name").inner_text()
        price_text = card.locator(".inventory_item_price").inner_text()
        price = float(price_text.replace("$", ""))

        card.locator(".inventory_item_name").click()

        detail_name = self.page.locator(
            ".inventory_details_name"
        ).inner_text()

        detail_price_text = self.page.locator(
            ".inventory_details_price"
        ).inner_text()

        detail_price = float(detail_price_text.replace("$", ""))

        self.page.go_back()

        return name, price, detail_name, detail_price