import logging

from playwright.sync_api import Page

from core.config import BASE_URL

logger = logging.getLogger("autotests")


class BasePage:
    """Базовый класс для всех страниц сайта."""

    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = ""):
        """Открывает страницу сайта."""
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        logger.info("Открытие страницы: %s", path or "/")

        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

    def get_title(self):
        """Возвращает заголовок страницы."""
        return self.page.title()

    def take_screenshot(self, name: str):
        """Создаёт скриншот страницы."""
        self.page.screenshot(
            path=f"screenshots/{name}.png",
            full_page=True
        )
