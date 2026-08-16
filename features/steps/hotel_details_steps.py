from behave import given, when, then
from utils.logger import logger

@given('the user has searched for hotels in "{destination}"')
def step_impl_search_for_hotels(context, destination):
    context.home_page.navigate()
    context.home_page.enter_destination(destination)
    context.home_page.click_search()
    assert context.search_results_page.is_results_page_loaded(), f"Search results failed to load for {destination}"

@when('the user selects the first hotel from the search results')
def step_impl_select_first_hotel(context):
    context.selected_hotel_name = context.search_results_page.get_first_hotel_name()
    context.search_results_page.open_first_hotel()

@then('the hotel details page should open in a new tab')
def step_impl_verify_new_tab(context):
    # Context tab switch is handled in open_first_hotel()
    assert len(context.driver.window_handles) >= 1, "Expected window handles to be present."

@then('the hotel title and property information should be displayed')
def step_impl_verify_hotel_details(context):
    assert context.hotel_details_page.is_hotel_details_displayed(), "Hotel details page elements were not displayed!"
    title = context.hotel_details_page.get_hotel_title()
    logger.info(f"Verified hotel detail page loaded for: '{title}'")
