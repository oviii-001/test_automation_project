import os
import sys
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from utils.logger import logger
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.hotel_details_page import HotelDetailsPage

def before_all(context):
    """Executes before all scenarios."""
    logger.info("==================================================")
    logger.info(" Starting Booking.com Behave Test Execution Suite ")
    logger.info("==================================================")
    context.start_time = time.time()

def before_scenario(context, scenario):
    """Executes before each scenario."""
    logger.info(f"--- Starting Scenario: '{scenario.name}' ---")
    context.driver = DriverFactory.get_driver()
    
    # Initialize Page Objects in Behave context
    context.home_page = HomePage(context.driver)
    context.search_results_page = SearchResultsPage(context.driver)
    context.hotel_details_page = HotelDetailsPage(context.driver)

def after_step(context, step):
    """Executes after each step. Captures screenshots on step failures."""
    if step.status == "failed":
        logger.error(f"Step failed: '{step.name}' in scenario '{context.scenario.name}'")
        try:
            screenshot_name = f"FAILED_{context.scenario.name.replace(' ', '_')}"
            file_path = context.home_page.take_screenshot(screenshot_name)
            
            # Attach screenshot to Allure report if allure-behave is active
            if hasattr(context, "embed"):
                with open(file_path, "rb") as image_file:
                    context.embed(image_file.read(), mime_type="image/png", caption="Failure Screenshot")
        except Exception as e:
            logger.error(f"Could not take failure screenshot: {e}")

def after_scenario(context, scenario):
    """Executes after each scenario. Cleans up driver instance."""
    logger.info(f"--- Finished Scenario: '{scenario.name}' [Status: {scenario.status}] ---\n")
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
            logger.info("WebDriver instance closed successfully.")
        except Exception as e:
            logger.warning(f"Error closing WebDriver: {e}")

def after_all(context):
    """Executes after all scenarios complete."""
    duration = round(time.time() - context.start_time, 2)
    logger.info("==================================================")
    logger.info(f" Suite Completed in {duration} seconds ")
    logger.info("==================================================")
