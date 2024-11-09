import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit_folium import st_folium
from process_data import calculate_optimal_route

class FlexiBusAnalyzer:
    def __init__(self):
        self.bookings_data, self.stops_data = self.get_data()
        self.stop_coordinates = self.create_stop_coordinates()
    
    def create_stop_coordinates(self):
        """Create dictionary of stop coordinates from stops data"""
        return dict(zip(self.stops_data.index, 
                       zip(self.stops_data['latitude'], self.stops_data['longitude'])))
    
    @staticmethod
    @st.cache_data
    def get_data():
        """Load and process the real data from Excel files"""
        try:
            # Load bookings data - replace with your actual file path
            bookings_data = pd.read_excel('D:\\FLEXI_trip_data.xls')
            
            # Load stops data - replace with your actual file path
            stops_data = pd.read_excel('D:\\FLEXI_bus_stops.xls')
            stops_data.set_index('index', inplace=True)
            
            # Process bookings data
            bookings_data['Actual Pickup Time'] = pd.to_datetime(bookings_data['Actual Pickup Time'])
            bookings_data['Actual Dropoff Time'] = pd.to_datetime(bookings_data['Actual Dropoff Time'])
            
            return bookings_data, stops_data
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None, None
    
    @st.cache_data
    def get_filtered_data(_self, start_date, end_date, selected_hours=None):
        """Filter bookings data based on date range and selected hours"""
        filtered_data = _self.bookings_data[
            (_self.bookings_data['Actual Pickup Time'].dt.date >= start_date) &
            (_self.bookings_data['Actual Pickup Time'].dt.date <= end_date) &
            (_self.bookings_data['Status'] == 'Validated')  # Only include completed trips
        ].copy()
        
        if selected_hours:
            filtered_data = filtered_data[
                filtered_data['Actual Pickup Time'].dt.hour.isin(selected_hours)
            ]
        
        return filtered_data

    def create_heatmap(self, filtered_data=None):
        """Create heatmap with actual stop locations"""
        data_to_use = filtered_data if filtered_data is not None else self.bookings_data
        
        # Calculate center point for map
        center_lat = self.stops_data['latitude'].mean()
        center_lon = self.stops_data['longitude'].mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        
        # Add stop markers
        for stop_id, row in self.stops_data.iterrows():
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=f"{row['name']} ({row['district']})",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Create points for heatmap from pickup and dropoff locations
        pickup_points = []
        dropoff_points = []
        
        for _, row in data_to_use.iterrows():
            if row['Status'] == 'Validated':
                if row['Pickup ID'] in self.stops_data.index:
                    pickup_stop = self.stops_data.loc[row['Pickup ID']]
                    pickup_points.append([pickup_stop['latitude'], pickup_stop['longitude']])
                
                if row['Dropoff ID'] in self.stops_data.index:
                    dropoff_stop = self.stops_data.loc[row['Dropoff ID']]
                    dropoff_points.append([dropoff_stop['latitude'], dropoff_stop['longitude']])
        
        if pickup_points or dropoff_points:
            HeatMap(pickup_points + dropoff_points, radius=15).add_to(m)
        
        return m

    def create_performance_metrics(self, filtered_data=None):
        """Calculate key performance metrics from real data"""
        data_to_use = filtered_data if filtered_data is not None else self.bookings_data
        
        # Calculate completion rate
        total_bookings = len(data_to_use)
        completed_trips = len(data_to_use[data_to_use['Status'] == 'Validated'])
        completion_rate = (completed_trips / total_bookings * 100) if total_bookings > 0 else 0
        
        # Calculate average trip duration for completed trips
        completed_data = data_to_use[data_to_use['Status'] == 'Validated']
        avg_duration = (completed_data['Actual Dropoff Time'] - 
                       completed_data['Actual Pickup Time']).mean()
        
        metrics = {
            'total_bookings': total_bookings,
            'completed_trips': completed_trips,
            'total_passengers': completed_data['Passengers'].sum(),
            'avg_passengers': round(completed_data['Passengers'].mean(), 2),
            'completion_rate': round(completion_rate, 2),
            'avg_duration_minutes': round(avg_duration.total_seconds() / 60 if avg_duration else 0, 2)
        }
        
        return metrics
    
    def create_routes(self):
        """Create dictionary of predefined routes and their demand (buses)"""
        # Load bookings data - replace with your actual file path
        bookings_data = pd.read_excel('D:\\FLEXI_trip_data.xls')
            
            # Load stops data - replace with your actual file path
        stops_data = pd.read_excel('D:\\FLEXI_bus_stops.xls')
        totalBus, routes = calculate_optimal_route(trips_data=bookings_data, bus_stop_data=stops_data)
        
        return totalBus, routes
    

def main():
    st.set_page_config(
        page_title="VGI-Flexi Bus Service Analysis",
        page_icon="🚌",
        layout="wide"
    )
    
    st.title('VGI-Flexi Bus Service Analysis Dashboard')
    
    # Initialize analyzer
    analyzer = FlexiBusAnalyzer()
    
    if analyzer.bookings_data is None or analyzer.stops_data is None:
        st.error("Failed to load data. Please check the file paths and data format.")
        return
    
    # Enhanced sidebar filters
    st.sidebar.header('Filters')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input('Start Date', 
                                  min(analyzer.bookings_data['Actual Pickup Time'].dt.date))
    with col2:
        end_date = st.date_input('End Date', 
                                max(analyzer.bookings_data['Actual Pickup Time'].dt.date))
    
    # Multi-select for hours
    hours = st.sidebar.multiselect(
        'Select Hours',
        options=list(range(24)),
        default=list(range(24)),
        format_func=lambda x: f'{x:02d}:00'
    )
    
    # Get filtered data
    filtered_data = analyzer.get_filtered_data(start_date, end_date, hours)
    
    # Performance metrics at the top
    metrics = analyzer.create_performance_metrics(filtered_data)
    
    # Display metrics in a clean layout
    st.markdown("### Key Performance Metrics")
    cols = st.columns(6)
    metrics_display = {
        'Total Bookings': metrics['total_bookings'],
        'Completed Trips': metrics['completed_trips'],
        'Total Passengers': metrics['total_passengers'],
        'Avg. Passengers': metrics['avg_passengers'],
        'Completion Rate': f"{metrics['completion_rate']}%",
        'Avg. Trip Duration': f"{metrics['avg_duration_minutes']}min"
    }
    
    for i, (label, value) in enumerate(metrics_display.items()):
        cols[i].metric(label, value)
    
    # Main content in two columns
    col1, col2 = st.columns([1,1])
    
    with col1:
        with st.container():
            st.markdown("### Hourly Demand Patterns")
            hourly_demand = filtered_data[filtered_data['Status'] == 'Validated'].groupby(
            filtered_data['Actual Pickup Time'].dt.hour)['Passengers'].sum().reset_index()
            hourly_demand.columns = ['Hour', 'Passengers']
            fig = px.line(hourly_demand, x='Hour', y='Passengers',
                     title='Passenger Demand by Hour')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Demand Heatmapp")
            st_folium(analyzer.create_heatmap(filtered_data), width=700, height=400)
    
    with col2:
        st.markdown("### Stop Analysis")
        # Create pickup/dropoff analysis
        pickup_counts = filtered_data[filtered_data['Status'] == 'Validated']['Pickup ID'].map(
            analyzer.stops_data['name']).value_counts().reset_index()
        pickup_counts.columns = ['Stop', 'Count']
        pickup_counts['Type'] = 'Pickups'
        
        dropoff_counts = filtered_data[filtered_data['Status'] == 'Validated']['Dropoff ID'].map(
            analyzer.stops_data['name']).value_counts().reset_index()
        dropoff_counts.columns = ['Stop', 'Count']
        dropoff_counts['Type'] = 'Dropoffs'
        
        stop_analysis = pd.concat([pickup_counts, dropoff_counts])
        
        fig = px.bar(stop_analysis, x='Stop', y='Count', color='Type',
                    title='Pickup and Dropoff Distribution by Stop',
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Add Route Suggestion Feature (New Feature)
        st.markdown("### Suggested Bus Route Based on Demand")
        totalBus, routes = analyzer.create_routes()
        print(routes)
        # Display DataFrame in Streamlit
        st.title("Bus Routes Overview")
        
        st.table(routes)

if __name__ == "__main__":
    main()