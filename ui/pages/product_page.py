from playwright.sync_api import Page
from ui.base_page import BasePage


class ProductPage(BasePage):
    """Страница карточки товара."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.product_title = page.locator("h1")

        self.price_per_square = page.locator(
            ".price-calc li:first-child .raw-price"
        )

        self.price_per_package = page.locator(
            ".price-calc li:nth-child(2) .raw-price"
        )

        self.package_info = page.locator("#units-block")

        self.add_to_cart_button = page.locator("#button-cart")

    def add_to_cart(self):
        self.add_to_cart_button.click()
