import os
from dotenv import load_dotenv

# Загружаем настройки из .env
load_dotenv()

# Адрес тестируемого сайта
BASE_URL = os.getenv("BASE_URL", "https://полдела24.рф")

# Настройки браузера
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Таймаут ожидания элементов на странице (мс)
TIMEOUT = int(os.getenv("TIMEOUT", "10000"))

USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
