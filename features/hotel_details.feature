Feature: Booking.com Hotel Details Verification
  As a traveler
  I want to view details of a specific hotel from search results
  So that I can verify property information and amenities before booking

  @details @regression
  Scenario: Select a hotel and verify property details page
    Given the user has searched for hotels in "Paris"
    When the user selects the first hotel from the search results
    Then the hotel details page should open in a new tab
    And the hotel title and property information should be displayed
