import os
import time
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from config.config import Config
from utils.logger import logger

class BasePage:
    """Base Page Object containing reusable WebDriver interactions, explicit waits, and utility methods."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = Config.DEFAULT_TIMEOUT

    def open_url(self, url: str) -> None:
        """Navigates to the specified URL."""
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Explicitly waits for an element to be present in DOM and visible."""
        t = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element with locator {locator} was not visible after {t} seconds.")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Explicitly waits for elements to be present in DOM."""
        t = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            logger.warning(f"No elements found with locator {locator} after {t} seconds.")
            return []

    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """Waits for an element to be clickable and performs a click operation."""
        t = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, t).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Clicked element: {locator}")
        except ElementClickInterceptedException:
            logger.warning(f"Click intercepted for {locator}, retrying with JavaScript click...")
            self.click_js(locator)
        except TimeoutException:
            logger.error(f"Element {locator} was not clickable after {t} seconds.")
            raise

    def click_js(self, locator: Tuple[str, str]) -> None:
        """Performs a click using JavaScript execution."""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"Clicked element via JS: {locator}")

    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """Enters text into an input field after ensuring visibility."""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Entered text '{text}' into locator {locator}")

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """Retrieves text from a visible element."""
        element = self.find_element(locator, timeout)
        text = element.text.strip()
        logger.info(f"Extracted text '{text}' from locator {locator}")
        return text

    def is_displayed(self, locator: Tuple[str, str], timeout: int = 3) -> bool:
        """Checks whether an element is displayed within a short timeout."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
            return False

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scrolls the page until the specified element is in view."""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)

    def switch_to_new_tab(self) -> None:
        """Switches execution context to the newly opened browser window/tab."""
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
            logger.info(f"Switched to tab window handle: {handles[-1]}")

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Returns the current page title."""
        return self.driver.title

    def take_screenshot(self, name: str) -> str:
        """Captures screenshot and saves to reports/screenshots directory."""
        file_name = f"{name}_{int(time.time())}.png"
        file_path = os.path.join(Config.SCREENSHOTS_DIR, file_name)
        self.driver.save_screenshot(file_path)
        logger.info(f"Screenshot saved to {file_path}")
        return file_path
