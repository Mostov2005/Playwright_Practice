from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )

    page = context.new_page()
    page.goto(
        "https://полдела24.рф/",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Браузер открыт. Пользуйся им.")
    input("Нажми Enter в консоли, когда захочешь закрыть браузер...")
