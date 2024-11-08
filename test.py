import streamlit as st
import pandas as pd

def main():
    st.title("📍 Coordinate Map Viewer")
    
    # Create two columns for latitude and longitude inputs
    col1, col2 = st.columns(2)
    
    # Input fields for coordinates
    with col1:
        latitude = st.number_input(
            "Enter Latitude:",
            min_value=-90.0,
            max_value=90.0,
            value=40.7128,  # Default to New York City
            step=0.0001,
            format="%.4f"
        )
    
    with col2:
        longitude = st.number_input(
            "Enter Longitude:",
            min_value=-180.0,
            max_value=180.0,
            value=-74.0060,  # Default to New York City
            step=0.0001,
            format="%.4f"
        )
    
    # Display the coordinates
    st.write(f"Selected Location: {latitude}, {longitude}")
    
    # Create a dataframe with the coordinates
    df = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })
    
    # Display the map
    st.map(df)
    
    # Add a link to open the location in Google Maps
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    st.markdown(f"[Open in Google Maps]({google_maps_url})")

if __name__ == "__main__":
    main()