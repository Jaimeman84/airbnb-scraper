import os
from typing import Dict, List

# Apify configuration
APIFY_ACTOR_ID = "GsNzxEKzE2vQ5d9HN"

# Supported currencies
SUPPORTED_CURRENCIES: Dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£"
}

# Default currency
DEFAULT_CURRENCY = "USD"

# Default minimum number of reviews for filtering
DEFAULT_MIN_REVIEWS = 10

# Room types for filtering
ROOM_TYPES: List[str] = [
    "Entire home/apt",
    "Private room",
    "Shared room",
    "Hotel room"
]

# Price range steps (in percentage)
PRICE_RANGE_STEPS = 5

# Map configuration
DEFAULT_MAP_ZOOM = 13
MAP_STYLE = "OpenStreetMap"

# Data columns configuration
DISPLAY_COLUMNS = [
    "Title",
    "Room Type",
    "Price per Night",
    "Overall Rating",
    "Reviews Count",
    "Superhost",
    "Capacity",
    "URL"
]

EXPORT_COLUMNS = [
    "ID",
    "Title",
    "Description",
    "Room Type",
    "Price per Night",
    "Cleaning Fee",
    "Service Fee",
    "Overall Rating",
    "Location Rating",
    "Cleanliness Rating",
    "Value Rating",
    "Reviews Count",
    "Superhost",
    "Capacity",
    "Host Name",
    "Host Experience",
    "Amenities Count",
    "Location Description",
    "URL",
    "Latitude",
    "Longitude"
]

# Streamlit page configuration
PAGE_CONFIG = {
    "page_title": "Airbnb Market Analyzer",
    "page_icon": "🏠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS styles
CUSTOM_CSS = """
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin-bottom: 1rem;
    }
    .listing-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .st-emotion-cache-16idsys p {
        font-size: 14px;
        margin-bottom: 0.5rem;
    }
    .chart-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin-bottom: 1rem;
    }
    </style>
"""