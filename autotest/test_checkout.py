
import pytest
import allure

from playwright.sync_api import Page, expect

from core.config import USER_EMAIL, USER_PASSWORD
from ui.pages.login_page import LoginPage
from ui.pages.search_page import SearchPage
from ui.pages.product_page import ProductPage
from ui.pages.cart_page import CartPage
from ui.pages.checkout_page import CheckoutPage


@pytest.mark.skipif(
    not USER_EMAIL or not USER_PASSWORD,
    reason="Учётные данные не заданы в .env"
)
@allure.feature("Оформление заказа")
@allure.title("Проверка заполнения формы оформления заказа")
def test_order_form(page: Page):
    # 1. Авторизация
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(USER_EMAIL, USER_PASSWORD)

    page.wait_for_url("**/my-account/", timeout=60000)

    # 2. Подготовка корзины
    cart_page = CartPage(page)
    cart_page.open_cart()
    cart_page.clear_cart()

    # 3. Поиск и добавление товара
    search_page = SearchPage(page)
    search_page.open_home_page()
    search_page.wait_for_search_initialization()
    search_page.search_product("Ламинат")
    search_page.open_first_product()

    product_page = ProductPage(page)
    expect(product_page.product_title).to_be_visible()
    product_page.add_to_cart()

    # 4. Проверка корзины
    cart_page.open_cart()
    page.reload(wait_until="domcontentloaded")

    expect(cart_page.cart_product).to_have_count(1, timeout=15000)

    # 5. Переход к оформлению
    checkout_page = CheckoutPage(page)
    checkout_page.open_checkout()

    expect(checkout_page.checkout_title).to_be_visible()
    expect(checkout_page.comment).to_be_visible()

    # 6. Заполнение формы
    checkout_page.fill_authorized_order_form(
        comment="Тестовое оформление заказа"
    )

    # 7. Проверка заполнения
    expect(checkout_page.customer_firstname).not_to_have_value("")
    expect(checkout_page.customer_telephone).not_to_have_value("")

    expect(checkout_page.comment).to_have_value(
        "Тестовое оформление заказа"
    )
    expect(checkout_page.agreement).to_be_checked()
    expect(checkout_page.shipping_pickup).to_be_checked()
