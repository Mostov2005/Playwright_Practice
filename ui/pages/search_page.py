from playwright.sync_api import Page, expect
from ui.base_page import BasePage


class SearchPage(BasePage):
    """Страница поиска товаров."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.search_input = page.locator(
            '#search input[name="search"]'
        )
        self.search_button = page.locator("#search button")

        # Выпадающие рекомендации
        self.search_results = page.locator(".iSearchBox")
        self.product_items = page.locator(
            ".isearchProducts > li:not(.iSearchHeading):not(.iSearchViewAllResults)"
        )
        self.no_results_message = page.locator(".isearchProducts")

    def open_home_page(self):
        self.open()

    def search_product(self, product_name: str):
        self.search_input.fill(product_name)

        # Принудительно вызываем событие изменения текста
        self.search_input.press("End")
        self.search_input.press("Backspace")
        self.search_input.press_sequentially(
            product_name[-1],
            delay=200
        )

    def get_search_results_count(self) -> int:
        return self.product_items.count()

    def wait_for_search_initialization(self):
        self.page.wait_for_function("""
            () => {
                const input = document.querySelector('#search input');
                const $ = window.jQuery;

                if (!input || !$) {
                    return false;
                }

                const events = $._data(input, 'events') || {};

                return events.keyup && events.keyup.length > 0;
            }
        """, timeout=15000)

    def get_first_product_link(self) -> str:
        onclick = self.product_items.first.get_attribute("onclick")

        return onclick.split("'")[1]

    def open_first_product(self):
        self.product_items.first.click()
