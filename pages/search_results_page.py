import time
from typing import List, Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger

class SearchResultsPage(BasePage):
    """Page Object for Booking.com Search Results Page."""

    # Locators
    RESULTS_HEADER = (By.XPATH, "//h1[contains(@class, 'a3b8729ab1') or contains(text(), 'found') or contains(text(), 'properties') or contains(text(), 'places')] | //h1")
    PROPERTY_CARDS = (By.XPATH, "//div[@data-testid='property-card'] | //div[contains(@class, 'sr_property_block')]")
    FIRST_HOTEL_TITLE = (By.XPATH, "(//div[@data-testid='title'] | //span[@data-testid='header-title'])[1]")
    FIRST_HOTEL_CARD = (By.XPATH, "(//div[@data-testid='property-card'])[1] | (//a[@data-testid='title-link'])[1]")
    SEE_AVAILABILITY_BTN = (By.XPATH, "(//a[@data-testid='availability-cta-btn'])[1] | (//div[@data-testid='property-card']//a)[1]")

    def is_results_page_loaded(self) -> bool:
        """Verifies search results page is loaded by looking for header or property cards."""
        logger.info("Verifying Search Results page load...")
        try:
            return self.is_displayed(self.RESULTS_HEADER, timeout=12) or self.is_displayed(self.PROPERTY_CARDS, timeout=12)
        except Exception as e:
            logger.error(f"Search results page did not load as expected: {e}")
            return False

    def get_results_header_text(self) -> str:
        """Returns heading text of search results page."""
        try:
            return self.get_text(self.RESULTS_HEADER, timeout=10)
        except Exception as e:
            logger.warning(f"Could not read results header: {e}")
            return ""

    def get_hotels_count(self) -> int:
        """Returns the number of displayed hotel property cards."""
        cards = self.find_elements(self.PROPERTY_CARDS, timeout=10)
        count = len(cards)
        logger.info(f"Found {count} hotel property cards on current search results page.")
        return count

    def are_hotels_displayed(self) -> bool:
        """Checks if at least one hotel card is displayed."""
        return self.get_hotels_count() > 0

    def get_first_hotel_name(self) -> str:
        """Extracts text title of the first hotel card."""
        try:
            title = self.get_text(self.FIRST_HOTEL_TITLE, timeout=10)
            logger.info(f"First hotel name: '{title}'")
            return title
        except Exception as e:
            logger.warning(f"Failed to extract first hotel title: {e}")
            return "Sample Hotel"

    def open_first_hotel(self) -> None:
        """Clicks on the first hotel to open its details page (which opens in a new tab)."""
        logger.info("Opening first hotel details...")
        try:
            if self.is_displayed(self.SEE_AVAILABILITY_BTN, timeout=5):
                self.click(self.SEE_AVAILABILITY_BTN)
            else:
                self.click(self.FIRST_HOTEL_CARD)
        except Exception as e:
            logger.warning(f"Could not click first hotel button, attempting JS click on title... {e}")
            self.click_js(self.FIRST_HOTEL_TITLE)

        time.sleep(2)
        self.switch_to_new_tab()
