import allure
from playwright.sync_api import Page, expect

from ui.pages.search_page import SearchPage


@allure.feature("Поиск товаров")
@allure.title("Поиск товара по названию")
def test_search_product(page: Page):
    search_page = SearchPage(page)

    # 1. Открываем главную страницу
    search_page.open_home_page()

    # 2. Проверяем доступность поля поиска
    expect(search_page.search_input).to_be_visible()
    expect(search_page.search_input).to_be_enabled()

    # 3. Ждём инициализации JavaScript-поиска
    search_page.wait_for_search_initialization()

    # 3. Вводим поисковый запрос
    search_page.search_product("Ламинат")

    # 4. Проверяем появление рекомендаций
    expect(search_page.product_items.first).to_be_visible(
        timeout=15000
    )

    # 5. Проверяем, что найден хотя бы один товар
    expect(search_page.product_items).not_to_have_count(0)

    # 6. Проверяем наличие названия первого товара
    first_product_name = search_page.product_items.first.locator(
        ".iSearchItem h3"
    )

    product_url = search_page.get_first_product_link()
    print("Ссылка на первый товар:", product_url)

    expect(first_product_name).to_be_visible()
    expect(first_product_name).not_to_be_empty()


@allure.feature("Поиск товаров")
@allure.title("Поиск товара без результатов")
def test_search_product_not_found(page: Page):
    search_page = SearchPage(page)

    search_page.open_home_page()

    expect(search_page.search_input).to_be_visible()
    search_page.wait_for_search_initialization()

    search_page.search_product("НесуществующийТовар12345")

    expect(search_page.search_results).to_be_visible(timeout=15000)
    expect(search_page.search_results).to_contain_text("Нет результатов")