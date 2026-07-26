# Tool implementations
from langchain.tools import tool
import requests
from datetime import date

HOTEL_API_URL = "https://hotel-booking-server-1085074390115.us-east4.run.app"


def search_hotels_db(city: str, check_in: str, check_out: str) -> str:
    """Call the hotel booking API to search for available hotels."""
    response = requests.get(
        f"{HOTEL_API_URL}/hotels/search",
        params={"city": city, "check_in": check_in, "check_out": check_out},
    )
    hotels = response.json()

    if not hotels:
        return "No hotels found matching your criteria."

    formatted = []
    for i, hotel in enumerate(hotels, 1):
        formatted.append(
            f"{i}. {hotel['name']} in {hotel['city']}"
            f" - ${hotel['price_per_night']}/night"
            f" - {hotel['rating']} stars"
        )
    return "\n".join(formatted)


@tool
def query_hotels(city: str, check_in: str, check_out: str) -> str:
    """Search for available hotels in a city for given dates.

    Args:
        city: City name to search hotels in
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)

    Returns:
        Formatted list of matching hotels with details
    """
    return search_hotels_db(city, check_in, check_out)


@tool
def calculate_total_cost(
    price_per_night: float, num_nights: int, tax_rate: float = 0.05
) -> str:
    """Calculate total hotel cost including taxes."""
    # Calculate subtotal, tax, and total
    # Format and return breakdown
    # ...
    return f"Cost Breakdown:\n- Rate: ${price_per_night} x {num_nights} nights\n- Tax: ${tax}\n- Total: ${total}"


@tool
def get_weather(city: str, date: str = None) -> str:
    """Get weather information for a city."""
    # Implementation:
    # 1. Call geocoding API to get coordinates
    # 2. Call weather API with coordinates
    # 3. Format and return results
    # ...
    return f"Weather in {city}: Sunny, 25°C"


@tool
def book_room(
    hotel_id: int, room_type: str, check_in_date: date, check_out_date: date
) -> str:
    """Book a room in a hotel using the hotel booking API"""
    # Implementation:
    # 1. Check availability
    # 2. Create reservation
    # 3. Return confirmation
    # ...
    return "Room booked successfully! Reservation ID: 12345"


# Configure provider's built-in web search
claude_websearch = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 3,
}

