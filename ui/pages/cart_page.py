from ui.base_page import BasePage
from playwright.sync_api import Page, expect

class CartPage(BasePage):
    """Страница корзины покупок."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_title = page.locator("#content h1")

        self.cart_product = page.locator(
            "#content .table-responsive tbody tr"
        )

        self.product_name = self.cart_product.locator(
            "td:nth-child(2) a"
        )

        self.product_quantity = self.cart_product.locator(
            'input[name^="quantity"]'
        )

        self.product_price = self.cart_product.locator(
            "td:nth-child(5)"
        )

        self.product_total = self.cart_product.locator(
            "td:nth-child(6)"
        )

    def open_cart(self):
        self.page.goto(
            "https://полдела24.рф/cart/",
            wait_until="commit",
            timeout=30000
        )
        self.cart_title.wait_for(state="visible", timeout=30000)

    def clear_cart(self):
        while self.cart_product.count() > 0:
            row = self.cart_product.first

            row.locator("button.btn-danger").click()

            self.page.wait_for_timeout(1500)

            if self.cart_product.count() > 0:
                self.cart_product.first.locator(
                    "button.btn-primary"
                ).click()

                self.page.wait_for_timeout(1500)