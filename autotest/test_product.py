import allure
from playwright.sync_api import Page, expect

from ui.pages.search_page import SearchPage
from ui.pages.product_page import ProductPage
from ui.pages.cart_page import CartPage


@allure.feature("Карточка товара")
@allure.title("Проверка основных данных товара")
def test_product_information(page: Page):
    search_page = SearchPage(page)

    search_page.open_home_page()
    search_page.wait_for_search_initialization()
    search_page.search_product("Ламинат")

    expect(search_page.product_items.first).to_be_visible(
        timeout=15000
    )

    search_page.open_first_product()

    product_page = ProductPage(page)

    expect(product_page.product_title).to_be_visible()
    expect(product_page.product_title).not_to_be_empty()

    expect(product_page.price_per_square).to_be_visible()
    expect(product_page.price_per_square).not_to_be_empty()

    expect(product_page.price_per_package).to_be_visible()
    expect(product_page.price_per_package).not_to_be_empty()

    expect(product_page.package_info).to_contain_text(
        "упаковке"
    )


@allure.feature("Корзина")
@allure.title("Добавление товара в корзину")
def test_add_product_to_cart(page: Page):
    search_page = SearchPage(page)
    search_page.open_home_page()

    search_page.wait_for_search_initialization()
    search_page.search_product("Ламинат")
    search_page.open_first_product()

    product_page = ProductPage(page)
    expect(product_page.product_title).to_be_visible()

    product_page.add_to_cart()

    cart_page = CartPage(page)
    cart_page.open_cart()

    expect(cart_page.cart_title).to_be_visible()
    expect(cart_page.cart_product).to_have_count(1)
    expect(cart_page.product_name).to_contain_text("Aberhof Prado")
