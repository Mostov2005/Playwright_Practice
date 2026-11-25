from playwright.sync_api import Page

from ui.base_page import BasePage
from core.logger import get_logger

logger = get_logger()


class LoginPage(BasePage):
    """Страница авторизации."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Форма авторизации
        self.login_form = page.locator('form[action*="/login/"]')

        # Поле электронной почты
        self.email_input = self.login_form.locator("#input-email")

        # Поле пароля
        self.password_input = self.login_form.locator("#input-password")

        # Кнопка входа
        self.login_button = self.login_form.locator(
            'input[type="submit"][value="Войти"]'
        )

        self.error_message = page.get_by_text(
            "Неправильно заполнены поля E-Mail и/или пароль!",
            exact=True
        )

    def open_login_page(self):
        """Открывает страницу авторизации."""
        self.open("my-account/")

    def login(self, email: str, password: str):
        """Выполняет авторизацию."""
        logger.info("Ввод учётных данных для авторизации")

        self.email_input.fill(email)
        self.password_input.fill(password)

        logger.info("Нажатие кнопки входа")
        self.login_button.click()

    def is_error_message_visible(self) -> bool:
        return self.error_message.is_visible()
