
import io
import logging

import pytest
import allure

from core.config import HEADLESS, TIMEOUT
from core.logger import get_logger

logger = get_logger()


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Настройки запуска браузера."""
    return {
        "headless": HEADLESS
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """Настройки контекста браузера."""
    return {
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }


@pytest.fixture(autouse=True)
def test_logging(request, page):
    """Логирование и прикрепление материалов к Allure."""

    log_stream = io.StringIO()

    log_handler = logging.StreamHandler(log_stream)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )

    logger.addHandler(log_handler)

    logger.info("Начало теста: %s", request.node.name)

    yield

    try:
        report = getattr(request.node, "rep_call", None)

        if report and report.failed:
            logger.error(
                "Тест завершился с ошибкой: %s",
                request.node.name
            )

            try:
                screenshot = page.screenshot(
                    full_page=True,
                    timeout=30000
                )

                allure.attach(
                    screenshot,
                    name="Скриншот при ошибке",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception:
                logger.exception("Не удалось сделать скриншот")

        else:
            logger.info(
                "Тест успешно завершён: %s",
                request.node.name
            )

        log_content = log_stream.getvalue()

        if log_content:
            allure.attach(
                log_content,
                name="Логи теста",
                attachment_type=allure.attachment_type.TEXT
            )

    finally:
        logger.removeHandler(log_handler)
        log_handler.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняем результат выполнения теста."""

    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def set_playwright_timeout(page):
    """Устанавливаем общий таймаут ожидания элементов."""
    page.set_default_timeout(TIMEOUT)
