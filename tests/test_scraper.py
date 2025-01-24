import pytest
from unittest.mock import Mock, patch
import pandas as pd
from src.scraper import AirbnbScraper

@pytest.fixture
def sample_listing():
    return {
        'id': '12345',
        'title': 'Test Listing',
        'description': 'A test listing',
        'coordinates': {'latitude': 51.5074, 'longitude': -0.1278},
        'roomType': 'Entire home/apt',
        'personCapacity': 4,
        'isSuperHost': True,
        'url': 'https://airbnb.com/rooms/12345',
        'price': {
            'amount': '$100',
            'label': '$100 per night',
            'qualifier': 'night',
            'breakDown': {
                'basePrice': {'price': '$20'},
                'serviceFee': {'price': '$15'}
            }
        },
        'rating': {
            'guestSatisfaction': 4.8,
            'reviewsCount': 100,
            'location': 4.9,
            'cleanliness': 4.7,
            'value': 4.6
        },
        'host': {
            'name': 'Test Host',
            'highlights': ['5 years hosting']
        },
        'amenities': [
            {
                'title': 'Basic',
                'values': [
                    {'title': 'Wifi', 'available': True},
                    {'title': 'Kitchen', 'available': True}
                ]
            }
        ],
        'locationDescriptions': [
            {
                'title': 'Neighborhood highlights',
                'content': 'Great location'
            }
        ]
    }

@pytest.fixture
def mock_scraper():
    with patch.dict('os.environ', {'APIFY_API_TOKEN': 'test_token'}):
        return AirbnbScraper()

def test_scraper_initialization():
    with patch.dict('os.environ', {'APIFY_API_TOKEN': 'test_token'}):
        scraper = AirbnbScraper()
        assert scraper.api_token == 'test_token'

def test_scraper_initialization_error():
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError, match="Apify API token is required"):
            AirbnbScraper()

def test_process_amenities(mock_scraper, sample_listing):
    amenities = sample_listing['amenities']
    processed = mock_scraper.process_amenities(amenities)
    
    assert 'Basic' in processed
    assert 'Wifi' in processed['Basic']
    assert len(processed['Basic']) == 2

def test_extract_highlights(mock_scraper):
    highlights = [
        {'title': 'Test', 'subtitle': 'Test subtitle'}
    ]
    processed = mock_scraper.extract_highlights(highlights)
    
    assert len(processed) == 1
    assert processed[0] == 'Test: Test subtitle'

def test_convert_to_dataframe(mock_scraper, sample_listing):
    df = mock_scraper.convert_to_dataframe([sample_listing])
    
    assert len(df) == 1
    assert df['Title'].iloc[0] == 'Test Listing'
    assert df['Price per Night'].iloc[0] == 100.0
    assert df['Overall Rating'].iloc[0] == 4.8
    assert df['Host Name'].iloc[0] == 'Test Host'

@patch('apify_client.ApifyClient')
@pytest.mark.parametrize("max_results,expected_count", [
    (None, 2),  # Should return all results
    (1, 1),     # Should limit to 1 result
])
def test_scrape_listings(mock_client, mock_scraper, sample_listing, max_results, expected_count):
    # Setup mock
    mock_dataset = Mock()
    # Create two sample listings for testing
    mock_dataset.iterate_items.return_value = [sample_listing, sample_listing.copy()]
    
    mock_run = {'defaultDatasetId': 'test_id'}
    mock_actor = Mock()
    mock_actor.call.return_value = mock_run
    
    mock_client_instance = Mock()
    mock_client_instance.actor.return_value = mock_actor
    mock_client_instance.dataset.return_value = mock_dataset
    
    mock_client.return_value = mock_client_instance
    
    # Test scraping
    results = mock_scraper.scrape_listings('London', max_results=max_results)
    
    assert len(results) == expected_count
    assert results[0]['id'] == '12345'
    mock_client_instance.actor.assert_called_once_with('GsNzxEKzE2vQ5d9HN')