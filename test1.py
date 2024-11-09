import openrouteservice
import folium
from streamlit_folium import folium_static
import streamlit as st

def create_route_map(start_coords, end_coords, api_key):
    """
    Create a route map between two points using OpenRouteService.
    
    Args:
        start_coords (list): [latitude, longitude] of start location
        end_coords (list): [latitude, longitude] of end location
        api_key (str): OpenRouteService API key
    """
    try:
        # Initialize the client
        client = openrouteservice.Client(key=api_key)
        
        # Convert coordinates to the format expected by OpenRouteService (lon, lat)
        coords = [[start_coords[1], start_coords[0]], [end_coords[1], end_coords[0]]]
        
        # Get the route
        route = client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson'
        )
        
        # Create a map centered at the midpoint
        center_lat = (start_coords[0] + end_coords[0]) / 2
        center_lon = (start_coords[1] + end_coords[1]) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        # Add the route to the map
        folium.GeoJson(
            route,
            name='route',
            style_function=lambda x: {'color': '#0066cc', 'weight': 4}
        ).add_to(m)
        
        # Add markers for start and end points
        folium.Marker(
            start_coords,
            popup='Start',
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
        
        folium.Marker(
            end_coords,
            popup='End',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m
    
    except Exception as e:
        st.error(f"Error creating route: {str(e)}")
        return None

def main():
    st.title("Route Map Applicationnnnnn")
    
    # API key input (you might want to move this to a config file in production)
    api_key = st.sidebar.text_input(
        "OpenRouteService API Key",
        value="5b3ce3597851110001cf6248fd38c510002b4e1b8f14a3f100d2a117",
        type="password"
    )
    
    # Input fields for coordinates
    st.sidebar.subheader("Start Location")
    start_lat = st.sidebar.number_input("Start Latitude", value=48.992168, format="%.6f")
    start_lon = st.sidebar.number_input("Start Longitude", value=11.377365, format="%.6f")
    
    st.sidebar.subheader("End Location")
    end_lat = st.sidebar.number_input("End Latitude", value=49.005142, format="%.6f")
    end_lon = st.sidebar.number_input("End Longitude", value=11.445253, format="%.6f")
    
    # Transportation mode selector
    transport_mode = st.sidebar.selectbox(
        "Transportation Mode",
        ["driving-car", "cycling-regular", "foot-walking"]
    )
    
    if st.sidebar.button("Generate Route"):
        start_coords = [start_lat, start_lon]
        end_coords = [end_lat, end_lon]
        
        with st.spinner("Generating route..."):
            map_obj = create_route_map(start_coords, end_coords, api_key)
            
            if map_obj:
                st.success("Route generated successfully!")
                folium_static(map_obj, width=800, height=600)
            
if __name__ == "__main__":
    main()