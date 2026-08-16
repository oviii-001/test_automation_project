Feature: Booking.com Hotel Search Functionality
  As a traveler
  I want to search for hotels on Booking.com
  So that I can view available accommodations for my destination and travel dates

  @smoke @regression
  Scenario: Verify Booking.com homepage loads successfully
    Given the user navigates to the Booking.com homepage
    Then the homepage should load successfully with search options displayed

  @search @smoke
  Scenario Outline: Search hotels by destination, travel dates, and guests
    Given the user is on the Booking.com homepage
    When the user enters destination "<destination>"
    And selects check-in date "<checkin_date>" and check-out date "<checkout_date>"
    And selects number of adult guests <adults>
    And clicks the Search button
    Then the search results page should be displayed
    And available hotel properties should be listed for "<destination>"

    Examples:
      | destination | checkin_date | checkout_date | adults |
      | Paris       | 2026-09-10   | 2026-09-15    | 2      |
      | London      | 2026-10-01   | 2026-10-05    | 2      |
