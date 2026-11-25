
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
@allure.feature("Сквозной сценарий покупки")
@allure.title("Покупка товара от авторизации до оформления заказа")
def test_e2e_purchase(page: Page):
    # 1. Авторизация
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(USER_EMAIL, USER_PASSWORD)

    page.wait_for_url("**/my-account/", timeout=60000)

    # 2. Очистка корзины перед тестом
    cart_page = CartPage(page)
    cart_page.open_cart()
    cart_page.clear_cart()

    # 3. Поиск товара
    search_page = SearchPage(page)
    search_page.open_home_page()
    search_page.wait_for_search_initialization()
    search_page.search_product("Ламинат")
    search_page.open_first_product()

    # 4. Проверка карточки товара
    product_page = ProductPage(page)
    expect(product_page.product_title).to_be_visible()

    # 5. Добавление товара в корзину
    product_page.add_to_cart()

    # 6. Проверка корзины
    cart_page.open_cart()

    # Обновление страницы и проверка сохранения товара
    page.reload(wait_until="domcontentloaded")
    expect(cart_page.cart_product).to_have_count(1, timeout=15000)

    expect(cart_page.cart_title).to_be_visible()
    expect(cart_page.product_name).to_contain_text("Aberhof Prado")
    expect(cart_page.product_quantity).to_have_value("1")

    # 7. Переход к оформлению
    checkout_page = CheckoutPage(page)
    checkout_page.open_checkout()

    # 8. Заполнение формы авторизованного пользователя
    checkout_page.fill_authorized_order_form(
        comment="Тестовое оформление заказа"
    )

    # 9. Проверка заполнения формы
    expect(checkout_page.customer_firstname).to_have_value("Александр")
    expect(checkout_page.customer_telephone).to_have_value("89962000939")
    expect(checkout_page.comment).to_have_value(
        "Тестовое оформление заказа"
    )
    expect(checkout_page.agreement).to_be_checked()
    expect(checkout_page.shipping_pickup).to_be_checked()
