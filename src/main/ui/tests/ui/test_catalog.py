import pytest

from ui.steps.catalog_steps import CatalogSteps

@pytest.mark.ui
class TestCatalog:

    def test_count_catalog(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")
        assert steps.get_products_count() == 6

    def test_sorted_by_name(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        steps.sort_items("az")
        assert steps.get_product_names() == sorted(steps.get_product_names())

        steps.sort_items("za")
        assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True)

    def test_sort_by_price(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        steps.sort_items("lohi")
        assert steps.get_product_prices() == sorted(steps.get_product_prices())

        steps.sort_items("hilo")
        assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True)

    def test_add_to_cart(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        steps.add_to_cart("Sauce Labs Bike Light")
        assert steps.get_cart_count() == 1

    def test_add_and_remove_onesie(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        steps.add_to_cart("Sauce Labs Onesie")
        assert steps.get_cart_count() == 1

        steps.remove_from_cart("Sauce Labs Onesie")
        assert steps.get_cart_count() == 0

    def test_product_details_onesie(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")
        assert name == detail_name
        assert price == detail_price

    def test_product_details_fleece_jacket(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Fleece Jacket")
        assert name == detail_name
        assert price == detail_price

    def test_remove_item_from_catalog(self,page):
        steps = CatalogSteps(page)
        steps.login("standard_user", "secret_sauce")

        steps.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
