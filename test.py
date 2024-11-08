import streamlit as st
import folium
from geopy.geocoders import Nominatim
from folium import IFrame

# Function to create map
def create_map(latitude, longitude, address=""):
    # Create a folium map centered around the coordinates
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Add a marker at the given coordinates with a popup
    iframe = IFrame(f"<b>{address}</b>", width=200, height=100)
    folium.Marker([latitude, longitude], popup=iframe).add_to(my_map)
    
    return my_map

# Streamlit sidebar for address input
st.title("Google Maps with Streamlit and Folium")
address = st.text_input("Enter an address:", "San Francisco, CA")

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Get coordinates for the entered address
location = geolocator.geocode(address)

if location:
    latitude = location.latitude
    longitude = location.longitude
    st.write(f"Coordinates: Latitude = {latitude}, Longitude = {longitude}")

    # Create and display the map
    folium_map = create_map(latitude, longitude, address)
    # Display the map in Streamlit
    st.markdown(folium_map._repr_html_(), unsafe_allow_html=True)
else:
    st.write("Address not found.")
