import pytest
import pandas as pd
from src.utils import (
    format_currency,
    calculate_market_metrics,
    prepare_amenities_analysis,
    calculate_price_ranges
)

def test_format_currency():
    assert format_currency(100.50, "USD") == "$100.50"
    assert format_currency(100.50, "EUR") == "€100.50"
    assert format_currency(100.50, "GBP") == "£100.50"
    assert format_currency(100.50, "XXX") == "$100.50"  # Default to USD

def test_calculate_market_metrics():
    # Create sample DataFrame
    data = {
        "Price per Night": [100, 200, 300],
        "Overall Rating": [4.5, 4.8, 4.2],
        "Superhost": [True, False, True],
        "Reviews Count": [10, 20, 30],
        "Room Type": ["Entire home", "Private room", "Entire home"]
    }
    df = pd.DataFrame(data)
    
    metrics = calculate_market_metrics(df)
    
    assert metrics["total_listings"] == 3
    assert metrics["avg_price"] == 200.0
    assert metrics["median_price"] == 200.0
    assert metrics["avg_rating"] == 4.5
    assert metrics["superhost_ratio"] == (2/3 * 100)
    assert metrics["avg_reviews"] == 20.0
    assert metrics["most_common_type"] == "Entire home"
    assert metrics["price_range"] == {"min": 100.0, "max": 300.0}

def test_prepare_amenities_analysis():
    amenities_data = [
        [{
            "title": "Test Category",
            "values": [
                {"title": "Wifi", "available": True},
                {"title": "Pool", "available": False}
            ]
        }]
    ]
    
    df = prepare_amenities_analysis(amenities_data)
    assert len(df) == 1
    assert df.iloc[0]["Amenity"] == "Wifi"
    assert df.iloc[0]["Count"] == 1

def test_calculate_price_ranges():
    prices = pd.Series([100, 200, 300, 400, 500])
    ranges = calculate_price_ranges(prices)
    
    assert len(ranges) == 5
    assert ranges[0]["start"] == 100
    assert ranges[0]["end"] == 180
    assert ranges[-1]["start"] == 420
    assert ranges[-1]["end"] == 500