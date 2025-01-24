import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import folium
from streamlit_folium import folium_static
import io
from scraper import AirbnbScraper

# Load environment variables
load_dotenv()

# Initialize session state variables
if 'full_df' not in st.session_state:
    st.session_state.full_df = None
if 'location' not in st.session_state:
    st.session_state.location = None
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# Page config
st.set_page_config(
    page_title="Airbnb Market Analyzer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_price_distribution_plot(df):
    """Create a price distribution plot with enhanced styling."""
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=df["Price per Night"],
        nbinsx=30,
        name="Properties",
        marker_color='#FF385C',
        hovertemplate="Price: $%{x}<br>Count: %{y}<extra></extra>"
    ))
    
    # Calculate statistics
    mean_price = df["Price per Night"].mean()
    median_price = df["Price per Night"].median()
    
    # Add mean and median lines
    fig.add_vline(x=mean_price, line_dash="dash", line_color="#484848",
                 annotation_text=f"Mean: ${mean_price:.0f}")
    fig.add_vline(x=median_price, line_dash="dot", line_color="#484848",
                 annotation_text=f"Median: ${median_price:.0f}")
    
    # Update layout with better styling
    fig.update_layout(
        title={
            'text': "Price Distribution",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Price per Night ($)",
        yaxis_title="Number of Properties",
        showlegend=False,
        margin=dict(l=40, r=40, t=100, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.1
    )
    
    return fig

def create_rating_histogram(df):
    """Create a histogram of ratings distribution with enhanced styling."""
    fig = go.Figure()
    
    # Custom colors for better visibility
    colors = {
        'Overall Rating': '#FF385C',    # Airbnb red
        'Location Rating': '#00A699',    # Teal
        'Cleanliness Rating': '#FC642D', # Orange
        'Value Rating': '#484848'        # Dark gray
    }
    
    # Add each rating type histogram
    for rating_type, color in colors.items():
        if rating_type in df.columns:  # Check if column exists
            fig.add_trace(go.Histogram(
                x=df[rating_type],
                name=rating_type.replace(' Rating', ''),
                nbinsx=20,
                marker_color=color,
                hovertemplate="Rating: %{x}<br>Count: %{y}<extra></extra>"
            ))
    
    # Update layout with better styling
    fig.update_layout(
        title={
            'text': "Rating Distribution by Category",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Rating Score",
        yaxis_title="Number of Properties",
        barmode='overlay',
        bargap=0.1,
        xaxis=dict(range=[3, 5]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        margin=dict(l=40, r=40, t=100, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    # Make histograms semi-transparent
    fig.update_traces(opacity=0.7)
    
    return fig

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply filters from sidebar to the dataframe."""
    if df is None or len(df) == 0:
        return None
        
    st.sidebar.header("🔍 Filters")
    
    # Price Range Filter
    min_price = float(df['Price per Night'].min())
    max_price = float(df['Price per Night'].max())
    price_range = st.sidebar.slider(
        "Price Range ($)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=10.0,
        key='price_filter'
    )
    
    # Rating Filter
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        key='rating_filter'
    )
    
    # Room Type Filter
    room_types = df['Room Type'].unique().tolist()
    selected_room_types = st.sidebar.multiselect(
        "Room Types",
        options=room_types,
        default=room_types,
        key='room_type_filter'
    )
    
    # Superhost Filter if available
    if 'Superhost' in df.columns:
        superhost_only = st.sidebar.checkbox("Superhost Only", key='superhost_filter')
    else:
        superhost_only = False
    
    # Capacity Filter if available
    if 'Capacity' in df.columns:
        max_capacity = int(df['Capacity'].max())
        min_guests = st.sidebar.number_input(
            "Minimum Guests",
            min_value=1,
            max_value=max_capacity,
            value=1,
            key='capacity_filter'
        )
    else:
        min_guests = 1
    
    # Apply filters
    mask = (
        (df['Price per Night'] >= price_range[0]) &
        (df['Price per Night'] <= price_range[1]) &
        (df['Overall Rating'] >= min_rating) &
        (df['Room Type'].isin(selected_room_types))
    )
    
    # Add capacity filter if available
    if 'Capacity' in df.columns:
        mask &= (df['Capacity'] >= min_guests)
    
    # Add superhost filter if available
    if superhost_only and 'Superhost' in df.columns:
        mask &= df['Superhost']
    
    filtered_df = df[mask]
    
    # Additional Stats in Sidebar
    st.sidebar.header("📊 Stats")
    st.sidebar.metric("Listings Found", f"{len(filtered_df)}")
    st.sidebar.metric("Average Price", f"${filtered_df['Price per Night'].mean():.2f}")
    st.sidebar.metric("Average Rating", f"{filtered_df['Overall Rating'].mean():.1f}/5")
    
    # Show capacity stats if available
    if 'Capacity' in filtered_df.columns:
        st.sidebar.metric("Average Capacity", f"{filtered_df['Capacity'].mean():.1f} guests")
    
    return filtered_df
    if df is None or len(df) == 0:
        return None
        
    st.sidebar.header("🔍 Filters")
    
    # Price Range Filter
    min_price = float(df['Price per Night'].min())
    max_price = float(df['Price per Night'].max())
    price_range = st.sidebar.slider(
        "Price Range ($)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=10.0,
        key='price_filter'
    )
    
    # Rating Filter
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        key='rating_filter'
    )
    
    # Room Type Filter
    room_types = df['Room Type'].unique().tolist()
    selected_room_types = st.sidebar.multiselect(
        "Room Types",
        options=room_types,
        default=room_types,
        key='room_type_filter'
    )
    
    # Superhost Filter
    superhost_only = st.sidebar.checkbox("Superhost Only", key='superhost_filter')
    
    # Capacity Filter
    max_capacity = int(df['Capacity'].max())
    min_guests = st.sidebar.number_input(
        "Minimum Guests",
        min_value=1,
        max_value=max_capacity,
        value=1,
        key='capacity_filter'
    )
    
    # Apply filters
    mask = (
        (df['Price per Night'] >= price_range[0]) &
        (df['Price per Night'] <= price_range[1]) &
        (df['Overall Rating'] >= min_rating) &
        (df['Room Type'].isin(selected_room_types)) &
        (df['Capacity'] >= min_guests)
    )
    
    if superhost_only:
        mask &= df['Superhost'] == True
    
    filtered_df = df[mask]
    
    # Additional Stats in Sidebar
    st.sidebar.header("📊 Stats")
    st.sidebar.metric("Listings Found", f"{len(filtered_df)}")
    st.sidebar.metric("Average Price", f"${filtered_df['Price per Night'].mean():.2f}")
    st.sidebar.metric("Average Rating", f"{filtered_df['Overall Rating'].mean():.1f}/5")
    
    return filtered_df

def display_results(df, location):
    """Display all visualizations and data for the filtered results."""
    if df is None or len(df) == 0:
        st.warning("No listings match your filters. Try adjusting the filter criteria.")
        return
    
    with st.container():
        # Summary metrics
        st.subheader("📊 Market Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Average Price", 
                f"${df['Price per Night'].mean():.2f}",
                delta=f"${df['Price per Night'].std():.2f} std"
            )
        with col2:
            st.metric(
                "Average Rating", 
                f"{df['Overall Rating'].mean():.1f}/5",
                delta=f"{(df['Overall Rating'].mean() - 4.5):.2f} from baseline"
            )
        with col3:
            st.metric("Total Listings", str(len(df)))
        with col4:
            st.metric(
                "Superhost Ratio", 
                f"{(df['Superhost'].mean() * 100):.1f}%"
            )

        # Visualizations
        st.subheader("📈 Price and Rating Analysis")
        viz_col1, viz_col2 = st.columns([1, 1])
        
        with viz_col1:
            st.plotly_chart(
                create_price_distribution_plot(df), 
                use_container_width=True,
                config={'displayModeBar': False}
            )
        
        with viz_col2:
            st.plotly_chart(
                create_rating_histogram(df), 
                use_container_width=True,
                config={'displayModeBar': False}
            )

        # Map
        st.subheader("📍 Property Locations")
        m = folium.Map(
            location=[df['Latitude'].mean(), df['Longitude'].mean()],
            zoom_start=13,
            width='100%',
            height='600px'
        )
        
        for _, row in df.iterrows():
            popup_html = f"""
                <div style="width: 300px;">
                    <h4 style="color: #FF385C; margin-bottom: 10px;">{row['Title']}</h4>
                    <p><strong>Price:</strong> ${row['Price per Night']:.2f}/night</p>
                    <p><strong>Rating:</strong> {row['Overall Rating']:.1f}/5 ({row['Reviews Count']} reviews)</p>
                    <p><strong>Type:</strong> {row['Room Type']}</p>
                    <p><strong>Capacity:</strong> {row['Capacity']} guests</p>
                    <a href="{row['URL']}" target="_blank" 
                       style="background-color: #FF385C; color: white; 
                              padding: 5px 10px; text-decoration: none; 
                              border-radius: 4px; display: inline-block;
                              margin-top: 10px;">
                        View on Airbnb
                    </a>
                </div>
            """
            
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"${row['Price per Night']:.0f}/night - {row['Room Type']}",
                icon=folium.Icon(
                    color='red' if row['Superhost'] else 'blue',
                    icon='home' if row['Room Type'] == 'Entire home/apt' else 'bed',
                    prefix='fa'
                )
            ).add_to(m)
        
        folium_static(m, width=1400, height=600)

        # Listings Table
        st.subheader("📋 Detailed Listings")
        st.dataframe(
            df[[
                'Title', 'Room Type', 'Price per Night', 'Overall Rating',
                'Reviews Count', 'Superhost', 'Capacity', 'URL'
            ]],
            use_container_width=True,
            height=400
        )

        # Downloads
        st.subheader("⬇️ Export Data")
        dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])
        
        with dl_col1:
            st.download_button(
                "📥 Download CSV",
                data=df.to_csv(index=False),
                file_name=f"airbnb_{location.lower()}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        
        with dl_col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                "📊 Download Excel",
                data=excel_data,
                file_name=f"airbnb_{location.lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        
        with dl_col3:
            st.download_button(
                "🔍 Download JSON",
                data=df.to_json(orient='records'),
                file_name=f"airbnb_{location.lower()}.json",
                mime="application/json",
                use_container_width=True,
            )

def main():
    st.title("🏠 Airbnb Market Analyzer")
    st.write("Analyze Airbnb listings and market trends in your desired location")
    
    try:
        scraper = AirbnbScraper()
    except ValueError as e:
        st.error(f"Error: {str(e)}")
        st.stop()

    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            location = st.text_input(
                "Enter location",
                placeholder="e.g., London, Paris, New York"
            )
        
        with col2:
            currency = st.selectbox(
                "Currency",
                options=["USD", "EUR", "GBP"],
                index=0
            )
        
        col3, col4 = st.columns(2)
        
        with col3:
            min_reviews = st.number_input(
                "Min Reviews",
                value=10,
                min_value=0,
                help="Minimum number of reviews required"
            )
            
        with col4:
            max_results = st.number_input(
                "Maximum Results",
                value=300,
                min_value=1,
                max_value=1000,
                help="Limit the number of listings to fetch (1-1000)"
            )
        
        submitted = st.form_submit_button("🔍 Search Listings")

    if submitted:
        if not location:
            st.error("Please enter a location")
            return
        
        with st.spinner('Fetching listings...'):
            try:
                listings = scraper.scrape_listings(location, currency, max_results=max_results)
                df = scraper.convert_to_dataframe(listings)
                df = df[df['Reviews Count'] >= min_reviews]
                
                st.session_state.full_df = df
                st.session_state.location = location
                st.session_state.search_performed = True
                
            except Exception as e:
                st.error(f"Error analyzing market data: {str(e)}")
                return

    if st.session_state.search_performed and st.session_state.full_df is not None:
        filtered_df = filter_dataframe(st.session_state.full_df)
        display_results(filtered_df, st.session_state.location)

if __name__ == "__main__":
    main()