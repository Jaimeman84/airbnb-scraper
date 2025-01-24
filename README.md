# Airbnb Listing Scraper

A simple Streamlit application that scrapes Airbnb listings data using the Apify API. Extract property details, prices, ratings, and more from any location.

## Features

- Search Airbnb listings by location
- View listing details including prices, ratings, and reviews
- Download data in CSV, Excel, or JSON format
- Basic analytics dashboard
- Support for multiple currencies (USD, EUR, GBP)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/airbnb-scraper.git
cd airbnb-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Apify API token:
```bash
APIFY_API_TOKEN=your_api_token_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/main.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter a location and click "Search Listings"

4. View the results and download the data in your preferred format

## Requirements

- Python 3.8+
- Streamlit
- Apify API Token
- Pandas
- python-dotenv

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 guidelines. Format your code using:
```bash
black src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.