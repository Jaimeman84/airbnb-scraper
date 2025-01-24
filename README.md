# 🏠 Airbnb Market Analyzer

A powerful Streamlit application for real-time analysis of Airbnb listings using the Apify Airbnb Scraper API.

## ✨ Features
- 🔍 Search listings by location
- 🗺️ Interactive map visualization with property details
- 📊 Advanced analytics for prices and ratings
- ⚡ Real-time data filtering
- 📈 Market trend analysis
- 💾 Export data in multiple formats (CSV, Excel, JSON)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Apify account with API token [(Get it here)](https://console.apify.com/sign-up)
- Access to the Airbnb scraper actor

### 🛠️ Installation
```bash
# Clone the repository
git clone https://github.com/jaimeman84/airbnb-scraper.git
cd airbnb-scraper

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Create a `.env` file in the root directory:
```env
APIFY_API_TOKEN=your_api_token_here
```

2. **Important**: Update the Actor ID in `src/scraper.py`:
```python
# In src/scraper.py, around line 101
# Airbnb Scraper Actor > API > API Client
run = self.client.actor("YOUR_ACTOR_ID").call(run_input=run_input)
```

To get your actor ID:
1. Go to [Apify Console](https://console.apify.com)
2. Navigate to "Actors" tab
3. Find "Airbnb Scraper" or create a new one
4. Copy the actor ID from the actor details

## 🖥️ Usage

Run the application:
```bash
streamlit run src/main.py
```

The app will be available at `http://localhost:8501`

## 📁 Project Structure
```
airbnb_analyzer/
├── src/
│   ├── main.py          # Streamlit app
│   └── scraper.py       # Apify integration
├── tests/
│   └── test_scraper.py  # Unit tests
├── .env                 # Configuration
├── .gitignore
├── README.md
└── requirements.txt
```

## 🧪 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
# Format code
black src/

# Check formatting
black src/ --check
```

### 🔄 Available Data Fields
```python
# Main data fields available in the DataFrame:
- 'ID'                 # Listing ID
- 'Title'             # Property title
- 'Description'       # Property description
- 'Room Type'         # Type of room
- 'URL'               # Airbnb listing URL
- 'Thumbnail'         # Property image URL
- 'Latitude'          # Location latitude
- 'Longitude'         # Location longitude
- 'Price per Night'   # Nightly price
- 'Capacity'          # Guest capacity
- 'Superhost'         # Superhost status
- 'Overall Rating'    # Average rating
- 'Reviews Count'     # Number of reviews
- 'Location Rating'   # Location rating
- 'Cleanliness Rating'# Cleanliness rating
- 'Value Rating'      # Value for money rating
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🚨 Common Issues

1. **Actor ID Error**: Make sure to update the actor ID in `scraper.py` with your own
2. **API Token Error**: Verify your Apify token in the `.env` file
3. **Missing Data**: Check if the selected location has available listings

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.