import allure
from playwright.sync_api import Page, expect

from core.config import BASE_URL


@allure.feature("Проверка отчётов")
@allure.title("Проверка создания скриншота при ошибке")
def test_failure_screenshot(page: Page):
    page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    with allure.step("Проверка заголовка страницы"):
        expect(page.locator("h1").first).to_have_text(
            "Несуществующий заголовок"
        )