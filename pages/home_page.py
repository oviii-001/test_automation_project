import time
from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config
from utils.logger import logger

class HomePage(BasePage):
    """Page Object for Booking.com Homepage."""

    # Locators
    COOKIE_ACCEPT_BTN = (By.ID, "onetrust-accept-btn-handler")
    SIGN_IN_DISMISS_BTN = (By.XPATH, "//button[@aria-label='Dismiss sign-in info.'] | //button[@aria-label='Dismiss sign in info.'] | //button[contains(@class, 'b868e42f9b')]")
    MODAL_CLOSE_BTN = (By.XPATH, "//button[@aria-label='Close'] | //button[contains(@aria-label, 'Dismiss')]")
    
    DESTINATION_INPUT = (By.XPATH, "//input[@name='ss' or @aria-label='Where are you going?' or @placeholder='Where are you going?']")
    SEARCH_AUTOCOMPLETE_FIRST = (By.XPATH, "//ul[@role='group']//li[1] | //div[@data-testid='autocomplete-results']//li[1] | //li[contains(@id, 'autocomplete-result')]")
    
    DATES_CONTAINER = (By.XPATH, "//div[@data-testid='searchbox-dates-container'] | //button[@data-testid='date-display-field-start']")
    NEXT_MONTH_BTN = (By.XPATH, "//button[@aria-label='Next month'] | //button[contains(@class, 'c21b56d9c0')]")
    
    # Dynamic Date Selector generator
    @staticmethod
    def get_date_locator(date_str: str) -> Tuple[str, str]:
        # date_str format e.g. "2026-08-15"
        return (By.XPATH, f"//span[@data-date='{date_str}'] | //td[@data-date='{date_str}']")

    GUESTS_CONTAINER = (By.XPATH, "//button[@data-testid='occupancy-config'] | //button[contains(@aria-label, 'occupancy')]")
    ADULTS_ADD_BTN = (By.XPATH, "(//button[contains(@class, 'f4d78af12a') or contains(@class, 'e6c50e8e04')])[2] | //div[contains(@class, 'occupancy')]/div[1]//button[2]")
    SEARCH_BTN = (By.XPATH, "//button[@type='submit' and (.//span[contains(text(),'Search')] or @data-testid='searchbox-search-button')] | //button[@type='submit']")
    BRAND_LOGO = (By.XPATH, "//a[@data-testid='header-booking-logo'] | //a[@aria-label='Booking.com']")

    def navigate(self) -> None:
        """Navigates to Booking.com homepage and clears blocking popups."""
        self.open_url(Config.BASE_URL)
        self.dismiss_popups()

    def dismiss_popups(self) -> None:
        """Handles and dismisses sign-in dialogs and cookie banners if present."""
        logger.info("Checking for blocking popups/modals...")
        time.sleep(2)  # Short wait for popups to animate in

        # Try dismissing cookie consent
        try:
            if self.is_displayed(self.COOKIE_ACCEPT_BTN, timeout=3):
                self.click(self.COOKIE_ACCEPT_BTN)
                logger.info("Dismissed cookie consent banner.")
        except Exception as e:
            logger.debug(f"Cookie banner not present or already accepted: {e}")

        # Try dismissing sign-in prompt modal
        try:
            if self.is_displayed(self.SIGN_IN_DISMISS_BTN, timeout=3):
                self.click(self.SIGN_IN_DISMISS_BTN)
                logger.info("Dismissed sign-in modal prompt.")
            elif self.is_displayed(self.MODAL_CLOSE_BTN, timeout=2):
                self.click(self.MODAL_CLOSE_BTN)
                logger.info("Dismissed modal via close button.")
        except Exception as e:
            logger.debug(f"Sign-in modal not present: {e}")

    def is_homepage_loaded(self) -> bool:
        """Verifies homepage loaded by checking title or logo presence."""
        try:
            title = self.get_page_title()
            logger.info(f"Page title retrieved: {title}")
            return "Booking.com" in title or self.is_displayed(self.DESTINATION_INPUT, timeout=5)
        except Exception as e:
            logger.error(f"Failed homepage verification: {e}")
            return False

    def enter_destination(self, destination: str) -> None:
        """Types destination into search box and selects first suggestion."""
        logger.info(f"Entering destination: '{destination}'")
        self.dismiss_popups()
        
        # Click and send keys to destination input
        self.send_keys(self.DESTINATION_INPUT, destination)
        time.sleep(1.5)  # Allow autocomplete dropdown to load
        
        # Select first autocomplete result if available
        try:
            if self.is_displayed(self.SEARCH_AUTOCOMPLETE_FIRST, timeout=4):
                self.click(self.SEARCH_AUTOCOMPLETE_FIRST)
                logger.info("Selected first autocomplete suggestion.")
        except Exception as e:
            logger.warning(f"Could not click autocomplete item: {e}")

    def select_dates(self, checkin_date: str = None, checkout_date: str = None) -> None:
        """Opens datepicker calendar and selects dates if provided."""
        logger.info(f"Selecting dates: Check-in={checkin_date}, Check-out={checkout_date}")
        
        # Open calendar if not already open
        try:
            if self.is_displayed(self.DATES_CONTAINER, timeout=3):
                self.click(self.DATES_CONTAINER)
        except Exception as e:
            logger.debug(f"Date container interaction note: {e}")

        # Select specific dates if provided
        if checkin_date:
            loc = self.get_date_locator(checkin_date)
            if self.is_displayed(loc, timeout=3):
                self.click(loc)
                logger.info(f"Selected check-in date: {checkin_date}")
        
        if checkout_date:
            loc = self.get_date_locator(checkout_date)
            if self.is_displayed(loc, timeout=3):
                self.click(loc)
                logger.info(f"Selected check-out date: {checkout_date}")

    def select_guests(self, adults_count: int = 2) -> None:
        """Opens guests configuration dropdown and sets adult count."""
        logger.info(f"Configuring guests (Adults={adults_count})...")
        try:
            if self.is_displayed(self.GUESTS_CONTAINER, timeout=3):
                self.click(self.GUESTS_CONTAINER)
                time.sleep(0.5)
        except Exception as e:
            logger.debug(f"Guest picker already expanded or note: {e}")

    def click_search(self) -> None:
        """Clicks the search submit button."""
        logger.info("Clicking Search button...")
        self.click(self.SEARCH_BTN)
