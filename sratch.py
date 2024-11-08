from geopy.geocoders import Nominatim
import folium

# Initialize the geolocator with your app name
geolocator = Nominatim(user_agent="geoapiExercises")

# Geocode an address
location = geolocator.geocode("1600 Pennsylvania Ave NW, Washington, DC")

# Print the location details
print("Address:", location.address)
print("Latitude:", location.latitude)
print("Longitude:", location.longitude)

# Create a map centered around the coordinates
map = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)

# Add a marker for the location
folium.Marker([location.latitude, location.longitude], popup=location.address).add_to(map)

# Save the map to an HTML file
map.save("location_map.html")

# You can open the map in a browser or view it directly in Jupyter Notebook if using it
