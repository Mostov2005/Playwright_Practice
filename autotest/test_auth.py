import pytest

from core.config import USER_EMAIL, USER_PASSWORD
from ui.pages.login_page import LoginPage




@pytest.mark.skipif(
    not USER_EMAIL or not USER_PASSWORD,
    reason="Учётные данные не заданы в .env"
)
def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.login(USER_EMAIL, USER_PASSWORD)

    # После авторизации должна открыться страница личного кабинета.
    page.wait_for_url("**/my-account/", timeout=60000)

    # Проверяем, что форма авторизации больше не отображается.
    assert not login_page.login_button.is_visible()


@pytest.mark.skipif(
    not USER_EMAIL,
    reason="Email не задан в .env"
)
def test_login_with_wrong_password(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.login(USER_EMAIL, "WrongPassword123!")

    assert login_page.is_error_message_visible()


def test_login_with_unknown_email(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.login("nonexistent_user_12345@example.com", "TestPassword123!")

    assert login_page.is_error_message_visible()


def test_login_with_empty_email(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.password_input.fill("TestPassword123!")
    login_page.login_button.click()

    page.wait_for_load_state("domcontentloaded")

    assert login_page.is_error_message_visible()


def test_login_with_empty_password(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.email_input.fill("nonexistent_user_12345@example.com")
    login_page.login_button.click()

    page.wait_for_load_state("domcontentloaded")

    assert login_page.is_error_message_visible()


def test_login_with_invalid_email(page):
    login_page = LoginPage(page)
    login_page.open_login_page()

    login_page.login("invalid-email", "TestPassword123!")

    page.wait_for_load_state("domcontentloaded")

    assert login_page.is_error_message_visible()
