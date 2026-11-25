from playwright.sync_api import Page
from ui.base_page import BasePage


class CheckoutPage(BasePage):
    """Страница оформления заказа."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.checkout_title = page.locator("#content h1")

        # Данные покупателя
        self.customer_firstname = page.locator("#customer_firstname")
        self.customer_email = page.locator("#customer_email")
        self.customer_telephone = page.locator("#customer_telephone")

        # Способ доставки
        self.shipping_pickup = page.locator("#filterit0\\.filterit0")
        self.shipping_city = page.locator("#filterit0\\.filterit1")
        self.shipping_terminal = page.locator("#filterit0\\.filterit3")

        # Дополнительные элементы
        self.comment = page.locator("#comment")
        self.agreement = page.locator('input[name="agreements[]"]')
        self.confirm_button = page.locator("#simplecheckout_button_confirm")

    def open_checkout(self):
        self.page.goto(
            "https://полдела24.рф/simplecheckout/",
            wait_until="domcontentloaded",
            timeout=30000
        )

    def select_shipping(self, shipping_option):
        shipping_option.check()

    def fill_order_form(
            self,
            firstname: str,
            email: str,
            telephone: str,
            comment: str
    ):
        self.customer_firstname.fill(firstname)
        self.customer_email.fill(email)
        self.customer_telephone.fill(telephone)
        self.comment.fill(comment)

        if not self.agreement.is_checked():
            self.agreement.check()

    def fill_authorized_order_form(self, comment: str):
        self.comment.fill(comment)

        if not self.agreement.is_checked():
            self.agreement.check()
