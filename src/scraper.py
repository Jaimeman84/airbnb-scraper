import os
import time
from typing import Dict, List, Any, Optional
import pandas as pd
from apify_client import ApifyClient

class AirbnbScraper:
    """Handles Airbnb data scraping using Apify."""
    
    def __init__(self, api_token: str = None):
        """Initialize the scraper with API token."""
        self.api_token = api_token or os.getenv("APIFY_API_TOKEN")
        if not self.api_token:
            raise ValueError("Apify API token is required")
        self.client = ApifyClient(self.api_token)

    def extract_price(self, price_data: Dict) -> float:
        """Extract price from the price data."""
        try:
            if not price_data:
                return 0.0
            
            # Get price value from price or label field
            price = price_data.get('price', price_data.get('label', '0'))
            
            # Clean and convert price string to float
            if isinstance(price, str):
                price = price.replace('$', '').replace(',', '').split()[0]
            
            return float(price)
        except (ValueError, AttributeError, IndexError):
            return 0.0

    def extract_capacity(self, listing: Dict) -> int:
        """Extract guest capacity from listing data."""
        try:
            # Try direct capacity field
            if 'personCapacity' in listing:
                return int(listing['personCapacity'])
            
            # Try subDescription items
            sub_desc = listing.get('subDescription', {})
            if sub_desc and 'items' in sub_desc:
                for item in sub_desc['items']:
                    if 'guest' in item.lower():
                        num = ''.join(filter(str.isdigit, item))
                        if num:
                            return int(num)
            
            return 1  # Default capacity
        except (ValueError, TypeError):
            return 1

    def extract_rating(self, rating_data: Optional[Dict]) -> Dict:
        """Extract rating information with defaults."""
        if not rating_data:
            return {
                'guestSatisfaction': 0.0,
                'reviewsCount': 0,
                'location': 0.0,
                'cleanliness': 0.0,
                'value': 0.0,
                'accuracy': 0.0,
                'communication': 0.0
            }
        
        return {
            'guestSatisfaction': float(rating_data.get('guestSatisfaction', 0)),
            'reviewsCount': int(rating_data.get('reviewsCount', 0)),
            'location': float(rating_data.get('location', 0)),
            'cleanliness': float(rating_data.get('cleanliness', 0)),
            'value': float(rating_data.get('value', 0)),
            'accuracy': float(rating_data.get('accuracy', 0)),
            'communication': float(rating_data.get('communication', 0))
        }

    def scrape_listings(self, location: str, currency: str = "USD", max_results: int = None) -> List[Dict]:
        """
        Scrape Airbnb listings for a given location.
        
        Args:
            location: City or area to search
            currency: Currency for prices (default: USD)
            max_results: Maximum number of listings to return (default: None = all)
        
        Returns:
            List of dictionaries containing listing data
        """
        # Prepare the actor input
        run_input = {
            "locationQueries": [location],
            "currency": currency,
            "locale": "en-US",
            "maxListings": max_results or 300,
            "proxyConfiguration": {
                "useApifyProxy": True
            }
        }
        
        # Start the actor and wait for it to finish
        # Airbnb Scraper Actor > API > API Client
        run = self.client.actor("your-actor-id").call(run_input=run_input)

        # Wait for the dataset to be ready (with timeout)
        max_wait_time = 180  # Maximum wait time in seconds
        wait_start = time.time()
        
        while True:
            try:
                dataset = self.client.dataset(run["defaultDatasetId"])
                items = list(dataset.iterate_items())
                if items:
                    break
                
                if time.time() - wait_start > max_wait_time:
                    raise TimeoutError("Dataset retrieval timed out")
                
                time.sleep(5)
                
            except Exception as e:
                if time.time() - wait_start > max_wait_time:
                    raise Exception(f"Failed to retrieve dataset: {str(e)}")
                time.sleep(5)
        
        # Limit results if specified
        if max_results and len(items) > max_results:
            items = items[:max_results]
            
        return items

    def convert_to_dataframe(self, listings: List[Dict]) -> pd.DataFrame:
        """Convert listings data to a pandas DataFrame."""
        if not listings:
            return pd.DataFrame()

        processed_data = []
        
        for listing in listings:
            try:
                # Extract basic listing information
                price = self.extract_price(listing.get('price', {}))
                ratings = self.extract_rating(listing.get('rating'))
                coordinates = listing.get('coordinates', {})
                
                # Skip invalid listings
                if price <= 0:
                    continue

                processed_listing = {
                    'ID': str(listing.get('id', '')),
                    'Title': str(listing.get('title', '')),
                    'Description': str(listing.get('description', '')),
                    'Room Type': str(listing.get('roomType', '')),
                    'URL': str(listing.get('url', '')),
                    'Thumbnail': str(listing.get('thumbnail', '')),
                    'Latitude': float(coordinates.get('latitude', 0)),
                    'Longitude': float(coordinates.get('longitude', 0)),
                    'Price per Night': price,
                    'Capacity': self.extract_capacity(listing),
                    'Superhost': bool(listing.get('isSuperHost', False)),
                    
                    # Rating information
                    'Overall Rating': ratings['guestSatisfaction'],
                    'Reviews Count': ratings['reviewsCount'],
                    'Location Rating': ratings['location'],
                    'Cleanliness Rating': ratings['cleanliness'],
                    'Value Rating': ratings['value'],
                    'Accuracy Rating': ratings['accuracy'],
                    'Communication Rating': ratings['communication']
                }
                
                # Only add listings with valid coordinates
                if processed_listing['Latitude'] != 0 and processed_listing['Longitude'] != 0:
                    processed_data.append(processed_listing)
                
            except Exception as e:
                print(f"Error processing listing {listing.get('id', 'unknown')}: {str(e)}")
                continue
        
        if not processed_data:
            return pd.DataFrame()

        # Create DataFrame and convert columns to appropriate types
        df = pd.DataFrame(processed_data)
        
        # Define column types
        numeric_columns = {
            'Price per Night': 'float64',
            'Overall Rating': 'float64',
            'Reviews Count': 'int64',
            'Location Rating': 'float64',
            'Cleanliness Rating': 'float64',
            'Value Rating': 'float64',
            'Accuracy Rating': 'float64',
            'Communication Rating': 'float64',
            'Capacity': 'int64'
        }
        
        # Convert column types
        for col, dtype in numeric_columns.items():
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    print(f"Error converting column {col}: {str(e)}")
                    continue

        return df.sort_values('Price per Night', ignore_index=True)