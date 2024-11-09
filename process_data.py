
import pandas as pd
import numpy as np
from optimzation import solve_and_print_results

def calculate_optimal_route(trips_data, bus_stop_data):
    bus_stop_data = bus_stop_data
    trips_data = trips_data

# replace the columns name with white space to _
    trips_data.columns = trips_data.columns.str.replace(' ', '_')
    trips_data = trips_data[trips_data["Dropoff_ID"] <= 69]
    trips_data = trips_data[trips_data["Pickup_ID"] <= 69]

    
    trip_matrix = pd.crosstab(trips_data['Pickup_ID'], trips_data['Dropoff_ID'])

    start = trip_matrix.index.to_numpy()
    destination = trip_matrix.columns.to_numpy()
    bus_stop_data = bus_stop_data.set_index("index").to_dict()
    names = bus_stop_data["name"]

    vectorized_func = np.vectorize(lambda x: names.get(x))
    start = vectorized_func(start)
    destination = vectorized_func(destination)
    print(start.shape)
    print(destination.shape)
    print(trip_matrix.to_numpy().shape)
    demands = trip_matrix.to_numpy().flatten().tolist()
    print(trip_matrix.to_numpy().flatten().shape)
    print(demands)

    return solve_and_print_results(start, destination, demands)



bookings_data = pd.read_excel('D:\\FLEXI_trip_data.xls')
            
            # Load stops data - replace with your actual file path
stops_data = pd.read_excel('D:\\FLEXI_bus_stops.xls')
totalBus, routes = calculate_optimal_route(trips_data=bookings_data, bus_stop_data=stops_data)
print(totalBus)
print(routes)