import pandas as pd
from typing import Dict, List

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount with proper symbol."""
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    symbol = currency_symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"

def calculate_market_metrics(df: pd.DataFrame) -> Dict:
    """Calculate key market metrics from the DataFrame."""
    return {
        "total_listings": len(df),
        "avg_price": df["Price per Night"].mean(),
        "median_price": df["Price per Night"].median(),
        "avg_rating": df["Overall Rating"].mean(),
        "superhost_ratio": (df["Superhost"].mean() * 100),
        "avg_reviews": df["Reviews Count"].mean(),
        "most_common_type": df["Room Type"].mode().iloc[0],
        "price_range": {
            "min": df["Price per Night"].min(),
            "max": df["Price per Night"].max()
        }
    }

def prepare_amenities_analysis(amenities_data: List[Dict]) -> pd.DataFrame:
    """Analyze amenities frequency across listings."""
    all_amenities = {}
    for listing_amenities in amenities_data:
        for category in listing_amenities:
            for amenity in category["values"]:
                if amenity["available"]:
                    name = amenity["title"]
                    all_amenities[name] = all_amenities.get(name, 0) + 1
    
    return pd.DataFrame(
        list(all_amenities.items()),
        columns=["Amenity", "Count"]
    ).sort_values("Count", ascending=False)

def calculate_price_ranges(prices: pd.Series) -> List[Dict]:
    """Calculate price ranges for filtering."""
    min_price = prices.min()
    max_price = prices.max()
    
    # Create price ranges with reasonable intervals
    step = (max_price - min_price) / 5
    ranges = []
    
    for i in range(5):
        start = min_price + (step * i)
        end = min_price + (step * (i + 1))
        ranges.append({
            "start": round(start),
            "end": round(end),
            "label": f"${round(start)} - ${round(end)}"
        })
    
    return ranges