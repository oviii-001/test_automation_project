from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger

class HotelDetailsPage(BasePage):
    """Page Object for Booking.com Hotel Details Page."""

    # Locators
    HOTEL_TITLE = (By.XPATH, "//h2[contains(@class, 'pp-header__title')] | //h2[@id='hp_hotel_name'] | //h2[contains(@class, 'hp__hotel-name')] | //h2")
    HOTEL_ADDRESS = (By.XPATH, "//span[contains(@class, 'hp_address_subtitle')] | //p[@id='showMap2'] | //span[@data-node_tt_id='location_score_tooltip']")
    RESERVE_BTN = (By.XPATH, "//button[@id='hp_book_now_button'] | //a[contains(@href, '#availability')] | //button[contains(@class, 'js-reservation-button')]")
    RATING_BADGE = (By.XPATH, "//div[@data-testid='review-score-component'] | //div[contains(@class, 'bui-review-score')]")

    def is_hotel_details_displayed(self) -> bool:
        """Verifies if hotel details page elements are displayed."""
        logger.info("Verifying Hotel Details page load...")
        try:
            return self.is_displayed(self.HOTEL_TITLE, timeout=10) or self.is_displayed(self.HOTEL_ADDRESS, timeout=10)
        except Exception as e:
            logger.error(f"Failed verifying hotel details page: {e}")
            return False

    def get_hotel_title(self) -> str:
        """Returns the title text of the selected hotel."""
        try:
            title = self.get_text(self.HOTEL_TITLE, timeout=10)
            logger.info(f"Retrieved hotel detail title: '{title}'")
            return title
        except Exception as e:
            logger.warning(f"Could not retrieve hotel title: {e}")
            return ""

    def get_hotel_address(self) -> str:
        """Returns address text of the hotel."""
        try:
            address = self.get_text(self.HOTEL_ADDRESS, timeout=5)
            logger.info(f"Retrieved hotel address: '{address}'")
            return address
        except Exception as e:
            logger.warning(f"Could not retrieve hotel address: {e}")
            return ""

    def is_reserve_button_present(self) -> bool:
        """Checks if reserve / availability button is present."""
        return self.is_displayed(self.RESERVE_BTN, timeout=5)
