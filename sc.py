import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import plugins
# Hide the menu and footer
st.set_page_config(
    page_title="Coordinate Map Viewer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide streamlit style elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker(
            [latitude, longitude],
            popup=f"Lat: {latitude}<br>Lon: {longitude}",
            tooltip="Click for coordinates"
        ).add_to(m)
    
    st_folium(m, width=800, height=600)
    # Add a link to open the location in Google Maps
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    st.markdown(f"[Open in Google Maps]({google_maps_url})")

if __name__ == "__main__":
    main()