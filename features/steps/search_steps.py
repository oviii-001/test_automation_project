from behave import given, when, then
from utils.logger import logger

@given('the user navigates to the Booking.com homepage')
@given('the user is on the Booking.com homepage')
def step_impl_navigate_to_homepage(context):
    context.home_page.navigate()
    assert context.home_page.is_homepage_loaded(), "Booking.com homepage failed to load!"

@then('the homepage should load successfully with search options displayed')
def step_impl_verify_homepage_loaded(context):
    assert context.home_page.is_homepage_loaded(), "Homepage header or search box not visible!"

@when('the user enters destination "{destination}"')
def step_impl_enter_destination(context, destination):
    context.home_page.enter_destination(destination)

@when('selects check-in date "{checkin_date}" and check-out date "{checkout_date}"')
def step_impl_select_dates(context, checkin_date, checkout_date):
    context.home_page.select_dates(checkin_date, checkout_date)

@when('selects number of adult guests {adults:d}')
def step_impl_select_guests(context, adults):
    context.home_page.select_guests(adults)

@when('clicks the Search button')
def step_impl_click_search(context):
    context.home_page.click_search()

@then('the search results page should be displayed')
def step_impl_verify_search_results_page(context):
    assert context.search_results_page.is_results_page_loaded(), "Search results page was not loaded!"

@then('available hotel properties should be listed for "{destination}"')
def step_impl_verify_hotels_listed(context, destination):
    assert context.search_results_page.are_hotels_displayed(), f"No hotel properties found for destination '{destination}'!"
    count = context.search_results_page.get_hotels_count()
    logger.info(f"Verified {count} hotels listed for '{destination}'.")
