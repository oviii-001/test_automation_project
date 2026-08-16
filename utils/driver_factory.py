from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
from utils.logger import logger

class DriverFactory:
    """Factory class to create and configure Selenium WebDriver instances."""

    @staticmethod
    def get_driver(browser_name: str = None, headless: bool = None) -> webdriver.Remote:
        browser = (browser_name or Config.BROWSER).lower()
        is_headless = Config.HEADLESS if headless is None else headless

        logger.info(f"Initializing WebDriver for '{browser}' (Headless={is_headless})...")

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if is_headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

            try:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.warning(f"WebDriverManager failed ({e}), falling back to native Selenium Manager...")
                driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            if is_headless:
                options.add_argument("--headless")
            try:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                logger.warning(f"GeckoDriverManager failed ({e}), falling back to native Selenium Manager...")
                driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: '{browser}'")

        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(2)  # Low implicit wait; explicit waits are preferred in POM
        if not is_headless:
            driver.maximize_window()
        else:
            driver.set_window_size(1920, 1080)

        logger.info(f"WebDriver for '{browser}' initialized successfully.")
        return driver
